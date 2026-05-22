# Connected Little Box — Teaching Framework

A browser-based teaching environment for learning MicroPython on the Raspberry Pi Pico. Two courses are included:

- **Introduction to Python on the Pico** — LEDs, buttons, NeoPixels, DC motors, servo motors
- **Connected Little Boxes** — the [CLB framework](https://github.com/CrazyRobMiles/MicroPython-Connected-Little-Box) for event-driven embedded systems

Students visit a static web page, connect their device via the browser's Web Serial API, and work through guided exercises. Progress is saved in browser localStorage.

---

## Two-Project Architecture (Connected Little Boxes book only)

The CLB book and the CLB platform repository are intentionally separate.

| | [MicroPython-Connected-Little-Box](https://github.com/CrazyRobMiles/MicroPython-Connected-Little-Box) | This repository |
|---|---|---|
| **Contains** | Device managers, base framework, hardware drivers | Web app, exercises, circuit diagrams, AI tutor definitions |
| **Knows about** | Its own managers and settings system | CLB version number; exercise file format; REPL protocol |
| **Does not know** | That a teaching layer exists | CLB internals |
| **Versioned by** | GitHub releases / tags | `web/firmware.json` pins a CLB release |

**The contract:** CLB publishes versioned releases containing the firmware files. This repo pins one release in `web/firmware.json`. The web app fetches that release and pushes it to the student's device. Beyond version number and file paths, neither project knows about the other.

When CLB releases a new version, update `web/firmware.json` and verify the exercises still work. No CLB changes are needed.

---

## Repository Layout

```
CLB-Teaching/
│
├── scripts/                       ← build tools (PDF generation, index helpers)
│
└── web/                           ← self-contained static site
    ├── index.html                 ← single-page app shell
    ├── firmware.json              ← pins the CLB release to install
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── app.js                 ← UI logic and orchestration
    │   ├── exercises.js           ← exercise loading and device setup
    │   ├── repl.js                ← MicroPython REPL communication
    │   ├── firmware.js            ← firmware fetch and install
    │   └── llm.js                 ← AI tutor / LLM provider
    ├── pdfs/                      ← pre-generated printable PDFs (one per lab)
    └── books/
        ├── index.json             ← catalogue of all books
        ├── python-intro/
        │   ├── index.json         ← book metadata, chapters, and lab list
        │   ├── 01-hardware-basics/
        │   │   ├── ch1_lab1_getting_started/
        │   │   │   ├── exercise.json
        │   │   │   ├── description_p1.md
        │   │   │   ├── description_p2.md
        │   │   │   └── start.py
        │   │   └── ch1_lab2_led_test/  …
        │   └── 02-micropython-hardware/  …
        └── connected-little-boxes/
            ├── index.json
            ├── 01-clb-setup/      ← chapter with no lab subfolder
            │   ├── exercise.json
            │   ├── description_p1.md
            │   └── start.py
            └── 02-button-light/  …
```

Exercise paths have the form `books/{bookId}/{chapterId}/{labId}` (three levels) or `books/{bookId}/{chapterId}` when the chapter is itself the exercise (no labs).

---

## How the Web App Works

### Prerequisites

- Chrome or Edge (Web Serial API is not available in Firefox or Safari)
- Device running MicroPython (Raspberry Pi Pico or compatible RP2040 board)
- USB cable connected to the student's computer

### Student Flow

1. **Visit the page** — hosted on GitHub Pages (or any static host over HTTPS); no software installation needed beyond Chrome or Edge
2. **Choose a book** — a picker shows all available books; selecting one opens its chapter/lab list; progress is remembered in localStorage
3. **Click Connect** — browser shows a serial port picker; student selects their device
4. **Install firmware** (CLB book, first time) — web app fetches the pinned CLB release from GitHub and writes each file to the device via REPL; takes ~30 seconds
5. **Select a lab** — the exercise description appears in the left panel; the files listed in `edit_files` are loaded into editor tabs and pushed to the device
6. **Edit, save, run** — student edits files in the browser editor; "Run" writes all changed files to the device and triggers a soft reboot; output appears in the console panel
7. **Navigate pages** — multi-page labs use Prev/Next buttons; the browser back/forward buttons also work and restore scroll position
8. **Ask for help** — if AI assistance is configured, hints are available in the Hints tab with the exercise context pre-loaded

### Technical Architecture

```
Browser
  │
  ├── Web Serial API ──► USB/serial ──► MicroPython REPL on device
  │       │
  │   repl.js         Handles raw REPL protocol, file writes,
  │                   soft reset, console I/O
  │
  ├── firmware.js     Fetches CLB release from GitHub,
  │                   iterates files, calls repl.writeFile()
  │
  ├── exercises.js    Fetches exercise content from this repo,
  │                   renders description, pushes start files,
  │                   writes app_manifest.py, calls select-app
  │
  ├── llm.js          LLM provider abstraction for the AI tutor
  │
  └── app.js          Manages UI state, editor tabs, console panel,
                      book/exercise navigation, progress tracking
```

### REPL Communication

MicroPython exposes a REPL over the serial connection. The web app uses two modes:

**Friendly REPL** — normal interactive mode. Used for the console panel; student can type commands directly.

**Raw REPL** — programmatic mode entered with `Ctrl-A`. Accepts a block of Python code, executes it on `Ctrl-D`, returns stdout and stderr. Used for all automated operations (writing files, running commands). The app enters raw mode for each operation and exits immediately after (`Ctrl-B`).

File writes are chunked at 256 bytes to avoid exhausting MicroPython's RAM. Content is passed through `JSON.stringify` for automatic escaping of quotes and newlines.

---

## Exercise Package Format

Each lab is a folder under `web/books/{bookId}/{chapterId}/{labId}/` containing these files:

### `exercise.json`

```json
{
  "id": "ch1_lab1_getting_started",
  "title": "Getting Started",
  "phase": 0,
  "concept": "setup and testing",
  "hardware": [],
  "pages": [
    "description_p1.md",
    "description_p2.md"
  ],
  "edit_files": [
    {
      "label": "main.py",
      "source": "start.py",
      "solution": "solution.py",
      "device_path": "/main.py"
    }
  ]
}
```

`edit_files` controls which files appear as editor tabs when the lab loads. Each entry has:
- `label` — the tab name shown in the UI
- `source` — filename in this lab folder to load as starting code
- `solution` — (optional) filename to load when the student clicks "Show Solution"
- `device_path` — where the file is written on the device

Multiple entries produce multiple editor tabs; all are saved to the device on Run/Save. If `pages` is absent, the loader looks for a single `description.md`.

The CLB book exercises also include CLB-specific fields:
- `start_file` — name of the CLB manager app to activate
- `default_settings` — `settings.json` content written to the device at exercise start

### Description pages

Student-facing content in Markdown, rendered in the browser's left panel. A single-page lab uses `description.md`; multi-page labs list files under `pages` in `exercise.json` (e.g. `description_p1.md`, `description_p2.md`). No special syntax is required — standard headings, code blocks, and lists all work. Images are resolved relative to the exercise folder.

### `circuit.svg`

Wiring diagram. Embed in a description page with `![Circuit Diagram](circuit.svg)`. Design for clarity at ~600 px width; use labels rather than relying on component colours alone.

### Source files (e.g. `start.py`, `solution.py`)

Each file listed under `edit_files[].source` is loaded into its own editor tab when the lab starts. The corresponding `solution` file (if present) is loaded when the student clicks "Show Solution". Files are written to `device_path` on the device.

### `tutor.py` / `tutor.json`

Exercise definition for the AI assistant. Contains: objective, off-limits items, ordered hint ladder, observation checklist, and a `tutor_brief` string injected into the LLM system prompt.

See `web/books/connected-little-boxes/02-button-light/tutor.py` for a reference example.

---

## Adding a New Lab

1. Decide which book and chapter the lab belongs to, e.g. `web/books/python-intro/03-neopixels/`
2. Create a subfolder for the lab: `ch3_lab6_my_new_lab/`
3. Add `exercise.json`, description page(s), and `start.py` following the format above
4. Add an entry to the chapter's `labs` array in the book's `index.json`
5. Verify `start.py` loads cleanly on the device

No web app code changes are needed for a new lab.

To add a new book, create `web/books/{bookId}/` with its own `index.json`, then add a summary entry to `web/books/index.json`.

---

## Hosting

The `web/` folder is a self-contained static site. Host it anywhere that serves HTTPS — Web Serial requires a secure context.

**GitHub Pages** (recommended):
1. Push to `main`
2. Enable GitHub Pages in repo settings, source: `web/` folder
3. Students visit `https://<org>.github.io/CLB-Teaching/`

**Local development:**
```
cd web
python -m http.server 8080
```
Then visit `http://localhost:8080` — localhost is treated as a secure context by browsers.

---

## CLB Version Management

`web/firmware.json` specifies which CLB release to fetch:

```json
{
  "repo": "CrazyRobMiles/MicroPython-Connected-Little-Box",
  "version": "1.0.0",
  "firmware_path": "firmware",
  "exclude": ["settings.json", "app_manifest.py"]
}
```

`exclude` lists files the installer should never overwrite — `settings.json` is managed by `select-app`; `app_manifest.py` is written by the exercise loader with only the current exercise's entry.

To update CLB: change `version`, verify exercises, commit.
