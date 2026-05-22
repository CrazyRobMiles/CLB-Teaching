'use strict';

const puppeteer = require('puppeteer');
const { marked }  = require('marked');
const fs   = require('fs');
const path = require('path');

const BOOKS_INDEX = path.join(__dirname, '..', 'web', 'books', 'index.json');
const BOOKS_DIR   = path.join(__dirname, '..', 'web', 'books');
const OUTPUT_DIR  = path.join(__dirname, '..', 'web', 'pdfs');

// ── Embedded CSS ─────────────────────────────────────────────────────────────

const CSS = `
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #111;
  margin: 0;
  padding: 0;
}
.cover {
  padding: 32pt 0 24pt;
  border-bottom: 2px solid #222;
  margin-bottom: 24pt;
}
.cover .chapter { font-size: 10pt; color: #666; margin-bottom: 6pt; letter-spacing: 0.02em; }
.cover h1 { font-size: 22pt; margin: 0; font-weight: 700; }
h1 { font-size: 17pt; border-bottom: 1.5px solid #333; padding-bottom: 4pt; margin-top: 24pt; }
h2 { font-size: 13pt; margin-top: 18pt; color: #222; }
h3 { font-size: 11.5pt; margin-top: 14pt; }
p  { margin: 0 0 8pt; }
ul, ol { margin: 0 0 8pt; padding-left: 20pt; }
li { margin-bottom: 3pt; }
code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 9.5pt;
  background: #f3f3f3;
  padding: 1px 4px;
  border-radius: 2px;
}
pre {
  background: #f3f3f3;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10pt 12pt;
  page-break-inside: avoid;
  margin: 8pt 0;
  overflow-x: auto;
}
pre code { background: none; padding: 0; font-size: 9pt; line-height: 1.45; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 10pt 0;
  page-break-inside: avoid;
  font-size: 10pt;
}
th, td { border: 1px solid #ccc; padding: 5pt 8pt; text-align: left; vertical-align: top; }
th { background: #ececec; font-weight: 600; }
tr:nth-child(even) td { background: #f9f9f9; }
blockquote {
  border-left: 3px solid #aaa;
  margin: 0 0 8pt;
  padding: 4pt 0 4pt 14pt;
  color: #444;
}
hr { border: none; border-top: 1px solid #ddd; margin: 18pt 0; }
strong { font-weight: 600; }
img { max-width: 100%; height: auto; }
.page-sep { margin-top: 24pt; }
`;

const FOOTER_TEMPLATE = `
  <div style="font-size:8pt;color:#aaa;width:100%;text-align:center;padding-top:4mm;">
    <span class="pageNumber"></span> / <span class="totalPages"></span>
  </div>`;

// ── HTML builder ──────────────────────────────────────────────────────────────

function buildHtml(title, chapterTitle, pages) {
  const body = pages
    .map((md, i) => `<div class="${i > 0 ? 'page-sep' : ''}">${marked.parse(md)}</div>`)
    .join('\n');

  const chapterLine = chapterTitle
    ? `<div class="chapter">${chapterTitle}</div>`
    : '';

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>${CSS}</style>
</head>
<body>
<div class="cover">
  ${chapterLine}
  <h1>${title}</h1>
</div>
${body}
</body>
</html>`;
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const { books: bookList } = JSON.parse(fs.readFileSync(BOOKS_INDEX, 'utf-8'));

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  let count = 0;

  for (const bookMeta of bookList) {
    const bookIndexPath = path.join(BOOKS_DIR, bookMeta.id, 'index.json');
    if (!fs.existsSync(bookIndexPath)) {
      console.warn(`  skip book  ${bookMeta.id}  (no index.json)`);
      continue;
    }
    const book = JSON.parse(fs.readFileSync(bookIndexPath, 'utf-8'));

    for (const ch of book.chapters ?? []) {
      for (const lab of ch.labs ?? []) {
        const labDir = path.join(BOOKS_DIR, bookMeta.id, ch.id, lab.id);

        if (!fs.existsSync(labDir)) {
          console.warn(`  skip  ${lab.id}  (directory not found)`);
          continue;
        }

        const metaPath = path.join(labDir, 'exercise.json');
        if (!fs.existsSync(metaPath)) {
          console.warn(`  skip  ${lab.id}  (no exercise.json)`);
          continue;
        }

        const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        const pageFiles = meta.pages ?? ['description.md'];

        const pages = [];
        for (const f of pageFiles) {
          const filePath = path.join(labDir, f);
          if (fs.existsSync(filePath)) {
            pages.push(fs.readFileSync(filePath, 'utf-8'));
          } else {
            console.warn(`  warn  ${lab.id}  missing ${f}`);
          }
        }

        if (pages.length === 0) {
          console.warn(`  skip  ${lab.id}  (no description pages found)`);
          continue;
        }

        const html = buildHtml(lab.title, ch.title, pages);
        const outputPath = path.join(OUTPUT_DIR, `${lab.id}.pdf`);
        const tmpPath    = path.join(labDir, '_pdf_tmp.html');

        fs.writeFileSync(tmpPath, html, 'utf-8');
        const page = await browser.newPage();
        try {
          await page.goto('file:///' + tmpPath.replace(/\\/g, '/'), { waitUntil: 'load' });
          await page.pdf({
            path: outputPath,
            format: 'A4',
            margin: { top: '22mm', right: '20mm', bottom: '22mm', left: '20mm' },
            printBackground: true,
            displayHeaderFooter: true,
            headerTemplate: '<div></div>',
            footerTemplate: FOOTER_TEMPLATE,
          });
        } finally {
          await page.close();
          fs.unlinkSync(tmpPath);
        }

        console.log(`  ok    ${lab.id}.pdf`);
        count++;
      }
    }
  }

  await browser.close();
  console.log(`\nGenerated ${count} PDF${count !== 1 ? 's' : ''} → web/pdfs/`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
