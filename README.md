# Connected Little Box — Teaching Framework

A browser-based teaching environment for the [Connected Little Box](https://github.com/CrazyRobMiles/MicroPython-Connected-Little-Box) MicroPython framework.

Students visit a static web page, connect their device via the browser's Web Serial API, and work through guided exercises that teach embedded systems concepts using CLB as the platform.

---

## Two-Project Architecture

This repository and the CLB platform repository are intentionally separate.

| | [MicroPython-Connected-Little-Box](https://github.com/CrazyRobMiles/MicroPython-Connected-Little-Box) | This repository |
|---|---|---|
| **Contains** | Device managers, base framework, hardware drivers | Web app, exercises, circuit diagrams, AI tutor definitions |
| **Knows about** | Its own managers and settings system | CLB version number; exercise file format; REPL protocol |
| **Does not know** | That a teaching layer exists | CLB internals |
| **Versioned by** | GitHub releases / tags | `firmware.json` pins a CLB release |

**The contract:** CLB publishes versioned releases containing the firmware files. This repo pins one release in `firmware.json`. The web app fetches that release and pushes it to the student's device. Beyond version number and file paths, neither project knows about the other.

When CLB releases a new version, update `firmware.json` and verify the exercises still work. No CLB changes are needed.

---

## Repository Layout

```
CLB-Teaching/
│
├── firmware.json              ← pins the CLB release to install
│
├── exercises/
│   ├── index.json             ← ordered list of all exercises
│   ├── 00_getting_started/
│   │   ├── exercise.json
│   │   ├── description_p1.md  ← multi-page descriptions
│   │   ├── description_p2.md
│   │   ├── description_p3.md
│   │   ├── description_p4.md
│   │   └── start.py
│   └── 01_button_light/
│       ├── exercise.json      ← metadata: title, hardware, phase, pages, edit_files
│       ├── description.md     ← student-facing exercise document (or description_pN.md for multi-page)
│       ├── circuit.svg        ← wiring diagram (embed in description.md with ![](circuit.svg))
│       ├── start.py           ← App_ file pushed to device at exercise start
│       ├── solution.py        ← complete solution (loadable on request)
│       ├── tutor.json         ← AI tutor configuration (tutor_brief, hints, etc.)
│       └── tutor.py           ← AI assistant exercise definition (device-side)
│
└── web/
    ├── index.html             ← single-page app shell
    ├── css/
    │   └── style.css
    └── js/
        ├── repl.js            ← MicroPython REPL communication
        ├── firmware.js        ← firmware fetch and install
        ├── exercises.js       ← exercise loading and device setup
        └── app.js             ← UI logic and orchestration
```

---

## How the Web App Works

### Prerequisites

- Chrome or Edge (Web Serial API is not available in Firefox or Safari)
- Device running MicroPython (Raspberry Pi Pico or compatible RP2040 board)
- USB cable connected to the student's computer

### Student Flow

1. **Visit the page** — hosted on GitHub Pages (or any static host over HTTPS); no software installation needed beyond Chrome or Edge
2. **Click Connect** — browser shows a serial port picker; student selects their device
3. **Install firmware** (first time) — web app fetches the pinned CLB release from GitHub and writes each file to the device via REPL; takes ~30 seconds
4. **Select exercise** — the exercise description and circuit diagram appear in the left panel; the files listed in `edit_files` are loaded into the built-in code editor tabs and pushed to the device; `settings.json` is written and the device reboots
5. **Edit, save, run** — student edits files directly in the browser editor (no external tools needed); "Save & Run" writes all changed files to the device and triggers a soft reboot; output appears in the console panel below the editor
6. **View settings** — the `settings.json` tab next to the code tabs lets students read and edit the device configuration file directly, with JSON validation before saving
7. **Ask for help** — if AI assistance is configured, `ask <question>` in the console reaches the tutor with the exercise context

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
  │                   renders description, pushes start.py,
  │                   writes app_manifest.py, calls select-app
  │
  └── app.js          Manages UI state, editor, console panel
```

### REPL Communication

MicroPython exposes a REPL over the serial connection. The web app uses two modes:

**Friendly REPL** — normal interactive mode. Used for the console panel; student can type commands directly.

**Raw REPL** — programmatic mode entered with `Ctrl-A`. Accepts a block of Python code, executes it on `Ctrl-D`, returns stdout and stderr. Used for all automated operations (writing files, running commands). The app enters raw mode for each operation and exits immediately after (`Ctrl-B`).

File writes are chunked at 256 bytes to avoid exhausting MicroPython's RAM. Content is passed through `JSON.stringify` for automatic escaping of quotes and newlines.

---

## Exercise Package Format

Each exercise is a folder under `exercises/` containing these files:

### `exercise.json`

```json
{
  "id": "01_button_light",
  "title": "Button Light",
  "phase": 1,
  "concept": "services and events",
  "clb_min_version": "1.0.0",
  "hardware": ["neopixel_strip", "tactile_button"],
  "edit_files": [
    {
      "label": "App_button_light_start.py",
      "source": "start.py",
      "solution": "solution.py",
      "device_path": "/managers/App_button_light_start_manager.py"
    }
  ],
  "start_file": "App_button_light_start",
  "circuit_description": "8 NeoPixels on GPIO 18, button between GPIO 14 and GND",
  "default_settings": { "App_button_light_start": { "enabled": true, "dependencies": [] } }
}
```

`edit_files` controls which files appear as editor tabs when the exercise loads. Each entry has:
- `label` — the tab name shown in the UI
- `source` — filename in this exercise folder to load as starting code
- `solution` — (optional) filename to load when the student clicks "Show Solution"
- `device_path` — where the file is written on the device

Multiple entries produce multiple editor tabs; all are saved to the device when "Save & Run" is clicked. If `edit_files` is absent the loader falls back to `start_file`/`solution_file` for backwards compatibility.

`hardware` is a list of identifiers. Currently illustrative — the SVG is the authoritative circuit description.

### `description.md`

Student-facing exercise document in Markdown. Rendered in the browser's left panel. No special syntax required — use standard headings, code blocks, and lists.

### `circuit.svg`

Wiring diagram. Displayed alongside the description. Design for clarity at ~600px width; use labels rather than relying on component colours alone.

### Source files (e.g. `start.py`, `solution.py`)

Each file listed under `edit_files[].source` is loaded into its own editor tab when the exercise starts. The corresponding `edit_files[].solution` file (if present) is loaded when the student clicks "Show Solution". Files are written to the device path given by `edit_files[].device_path`.

An exercise with a single editable file needs only `start.py` and `solution.py`. An exercise with multiple files adds more entries to `edit_files` and supplies a source file for each.

### `tutor.py`

Exercise definition for the AI assistant. Contains: objective, off-limits items (never revealed directly), ordered hint ladder, observation checklist, and a `tutor_brief` string injected verbatim into the LLM system prompt.

See `exercises/01_button_light/tutor.py` for the reference format.

---

## Adding a New Exercise

1. Create `exercises/NN_name/` following the format above
2. Add an entry to `exercises/index.json`
3. Write description content — either a single `description.md` or multiple pages listed under `pages` in `exercise.json`
4. Verify `start.py` loads cleanly and the device reaches `STATE_OK`
5. Verify `solution.py` (if present) produces the correct behaviour
6. Embed the circuit diagram in the description with `![Circuit Diagram](circuit.svg)` rather than relying on a separate tab

That is all. No web app code changes are needed for a new exercise.

---

## Hosting

The `web/` folder is a self-contained static site. Host it anywhere that serves HTTPS — Web Serial requires a secure context.

**GitHub Pages** (recommended for development):
1. Push to `main`
2. Enable GitHub Pages in repo settings, source: `web/` folder or root
3. Students visit `https://<org>.github.io/CLB-Teaching/`

**Local development:**
Any local HTTPS server works. With Python:
```
cd web
python -m http.server 8080
```
Then visit `http://localhost:8080` — localhost is treated as a secure context by browsers.

---

## Upgrade Path: Adding Progress Tracking

The static version gives you everything except persistence. When you need it:

1. Add a `tracking.js` module that POSTs events (exercise started, hint requested, exercise completed) to an endpoint
2. The endpoint can be a serverless function (Netlify, Vercel, Cloudflare Workers) that appends to a log
3. A teacher dashboard is a separate read-only view over that log

No existing files need to change. `tracking.js` is purely additive — imported in `app.js` and called at the events that matter. The exercise format, REPL layer, and firmware installer are unaffected.

---

## CLB Version Management

`firmware.json` specifies which CLB release to fetch:

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
