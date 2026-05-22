'use strict';

const fs   = require('fs');
const path = require('path');

const BOOKS_DIR = path.join(__dirname, '..', 'web', 'books');
const OUTPUT    = path.join(BOOKS_DIR, 'index.json');

function main() {
  const entries = fs.readdirSync(BOOKS_DIR, { withFileTypes: true })
    .filter(e => e.isDirectory())
    .map(e => {
      const indexPath = path.join(BOOKS_DIR, e.name, 'index.json');
      if (!fs.existsSync(indexPath)) return null;
      const book = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
      const labCount = (book.chapters ?? []).reduce((n, ch) => n + (ch.labs ?? []).length, 0);
      const entry = {
        _order:      book.order ?? 999,
        id:          book.id,
        title:       book.title,
        description: book.description ?? '',
        chapters:    (book.chapters ?? []).length,
        labs:        labCount,
      };
      if (book.code_resources?.length) {
        entry.code_resources = book.code_resources;
      }
      return entry;
    })
    .filter(Boolean)
    .sort((a, b) => {
      const ao = a._order ?? 999;
      const bo = b._order ?? 999;
      return ao !== bo ? ao - bo : a.id.localeCompare(b.id);
    })
    .map(({ _order, ...rest }) => rest); // strip internal _order field

  fs.writeFileSync(OUTPUT, JSON.stringify({ books: entries }, null, 2) + '\n', 'utf-8');
  console.log(`Built books/index.json — ${entries.length} book(s): ${entries.map(b => b.id).join(', ')}`);
}

main();
