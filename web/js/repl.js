/**
 * MicroPythonREPL
 *
 * Wraps the Web Serial API and the MicroPython raw-REPL protocol.
 *
 * Raw REPL protocol:
 *   Ctrl-A  → enter raw mode  (device echoes "raw REPL; CTRL-B to exit\r\n>")
 *   <code>  → send Python source
 *   Ctrl-D  → execute          (device responds "OK" + stdout + \x04 + stderr + \x04)
 *   Ctrl-B  → exit raw mode
 *   Ctrl-C  → keyboard interrupt (sent before entering raw mode to clear any running code)
 */

const CTRL_A = '\x01';
const CTRL_B = '\x02';
const CTRL_C = '\x03';
const CTRL_D = '\x04';
const RAW_REPL_PROMPT = 'raw REPL; CTRL-B to exit';

const CHUNK_SIZE = 256;   // bytes per file-write chunk — conservative for MicroPython RAM
const EXEC_TIMEOUT = 8000; // ms to wait for a raw-REPL response

export class MicroPythonREPL {
  constructor() {
    this.port = null;
    this.reader = null;
    this.writer = null;
    this._rxBuf = '';
    this._rxListeners = [];   // callbacks for console passthrough
    this._disconnectListeners = [];
    this._reading = false;
    this._silent = false;     // true while in raw REPL so output isn't echoed
  }

  // ── Connection ────────────────────────────────────────────────────

  async connect() {
    this.port = await navigator.serial.requestPort();
    await this.port.open({ baudRate: 115200 });
    this.writer = this.port.writable.getWriter();
    this._startReadLoop();
    // Give MicroPython a moment to settle, then interrupt any running program.
    await this._sleep(300);
    await this._sendRaw(CTRL_C + CTRL_C);
    await this._sleep(200);
    // Explicitly exit raw REPL in case device was left in it by a previous session.
    await this._sendRaw(CTRL_B);
    await this._sleep(100);
  }

  async disconnect() {
    this._reading = false;
    try { await this.reader?.cancel(); } catch (_) {}  // must await — releases readable lock
    try { this.writer?.releaseLock(); } catch (_) {}
    try { await this.port?.close(); } catch (_) {}
    this.port = this.reader = this.writer = null;
  }

  get connected() {
    return this.port !== null;
  }

  // ── Console passthrough ───────────────────────────────────────────
  // Anything arriving on serial while in friendly-REPL mode goes to
  // registered listeners so the UI console panel can display it.

  onData(callback) {
    this._rxListeners.push(callback);
  }

  offData(callback) {
    this._rxListeners = this._rxListeners.filter(l => l !== callback);
  }

  onDisconnect(callback) {
    this._disconnectListeners.push(callback);
  }

  offDisconnect(callback) {
    this._disconnectListeners = this._disconnectListeners.filter(l => l !== callback);
  }

  // Send a line to the friendly REPL (console input box).
  async sendLine(line) {
    await this._sendRaw(line + '\r\n');
  }

  async interrupt() {
    await this._sendRaw(CTRL_C + CTRL_C);
  }

  // ── High-level operations ─────────────────────────────────────────

  /**
   * Execute a block of Python in raw REPL mode.
   * Returns { stdout, stderr }.
   * Throws on timeout or if stderr is non-empty (caller decides whether to surface).
   */
  async execute(code) {
    try {
      await this._enterRaw();
      await this._sendRaw(code + CTRL_D);
      return await this._readRawResult();
    } finally {
      await this._exitRaw();
    }
  }

  /**
   * Write content to a file on the device in a single raw-REPL round trip.
   * All chunks are sent as one Python script so we only pay the enter/exit
   * raw overhead once per file instead of once per 256-byte chunk.
   */
  async writeFile(path, content) {
    const chunks = this._chunk(content, CHUNK_SIZE);
    const escapedPath = path.replace(/'/g, "\\'");
    const lines = [`_f=open('${escapedPath}','w')`];
    for (const chunk of chunks) lines.push(`_f.write(${this._pyStr(chunk)})`);
    lines.push(`_f.close()`);
    await this.execute(lines.join('\n'));
  }

  /**
   * Read a file from the device.  Returns its contents as a string.
   */
  async readFile(path) {
    const escapedPath = path.replace(/'/g, "\\'");
    const { stdout } = await this.execute(
      `_f=open('${escapedPath}','r')\nprint(_f.read())\n_f.close()`
    );
    return stdout.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  }

  /**
   * Soft-reset the device (equivalent to pressing the reset button in REPL).
   * This causes MicroPython to re-run boot.py / main.py.
   */
  async softReset() {
    await this._exitRaw();   // ensure we are in friendly REPL first
    await this._sendRaw(CTRL_D);
    await this._sleep(1500); // wait for boot sequence
  }

  /**
   * List files in a directory.  Returns an array of filenames.
   */
  async listDir(path = '/') {
    const escapedPath = path.replace(/'/g, "\\'");
    const { stdout } = await this.execute(`import os\nprint(os.listdir('${escapedPath}'))`);
    try {
      // MicroPython prints a Python list literal — parse it safely.
      return JSON.parse(stdout.trim().replace(/'/g, '"'));
    } catch {
      return [];
    }
  }

  /**
   * List a directory with type info.
   * Returns [{name, isDir}] sorted directories first, then files alphabetically.
   */
  async listDirDetailed(path = '/') {
    const base = path.endsWith('/') ? path : path + '/';
    const ep   = path.replace(/'/g, "\\'");
    const eb   = base.replace(/'/g, "\\'");
    const { stdout } = await this.execute(
      `import os,json;print(json.dumps([[n,bool(os.stat('${eb}'+n)[0]&0x4000)]for n in sorted(os.listdir('${ep}'))]))`
    );
    try {
      const raw   = JSON.parse(stdout.trim());
      const dirs  = raw.filter(e => e[1]).map(e => ({ name: e[0], isDir: true  }));
      const files = raw.filter(e => !e[1]).map(e => ({ name: e[0], isDir: false }));
      return [...dirs, ...files];
    } catch {
      return [];
    }
  }

  // ── Raw REPL internals ────────────────────────────────────────────

  async _enterRaw() {
    this._silent = true;
    await this._sendRaw(CTRL_C + CTRL_C);
    await this._sleep(50);
    this._rxBuf = '';
    await this._sendRaw(CTRL_A);
    await this._waitFor(RAW_REPL_PROMPT, 3000);
    this._rxBuf = '';
  }

  async _exitRaw() {
    this._rxBuf = '';                              // drop raw-REPL residue (the trailing '>')
    try { await this._sendRaw(CTRL_B); } catch (_) {}
    this._silent = false;                          // un-mute BEFORE sleeping so >>> reaches UI
    await this._sleep(100);
  }

  async _readRawResult() {
    // Raw REPL response format after Ctrl-D execution:
    //   "OK" + stdout + \x04 + stderr + \x04
    await this._waitFor('OK', EXEC_TIMEOUT);
    this._rxBuf = this._rxBuf.slice(this._rxBuf.indexOf('OK') + 2);

    const stdout = await this._readUntil(CTRL_D, EXEC_TIMEOUT);
    const stderr = await this._readUntil(CTRL_D, EXEC_TIMEOUT);

    return { stdout: stdout.trimEnd(), stderr: stderr.trimEnd() };
  }

  // ── Serial read loop ──────────────────────────────────────────────

  _startReadLoop() {
    this._reading = true;
    const decoder = new TextDecoder();

    const loop = async () => {
      try {
        this.reader = this.port.readable.getReader();
        while (this._reading) {
          const { value, done } = await this.reader.read();
          if (done) break;
          const text = decoder.decode(value);
          this._rxBuf += text;
          // Notify console listeners (friendly REPL output).
          if (!this._silent) {
            for (const cb of this._rxListeners) cb(text);
          }
        }
      } catch (e) {
        if (this._reading) console.warn('Serial read error:', e);
      } finally {
        try { this.reader?.releaseLock(); } catch (_) {}
        // If _reading is still true the loop ended due to device removal, not a
        // deliberate disconnect() call — clean up and notify listeners.
        if (this._reading) {
          this._reading = false;
          try { this.writer?.releaseLock(); } catch (_) {}
          try { await this.port?.close(); } catch (_) {}
          this.port = this.reader = this.writer = null;
          for (const cb of this._disconnectListeners) cb();
        }
      }
    };

    loop();
  }

  // ── Buffer helpers ────────────────────────────────────────────────

  async _waitFor(pattern, timeout) {
    const deadline = Date.now() + timeout;
    while (!this._rxBuf.includes(pattern)) {
      if (Date.now() > deadline) throw new Error(`Timeout waiting for: ${JSON.stringify(pattern)}`);
      await this._sleep(20);
    }
  }

  async _readUntil(terminator, timeout) {
    const deadline = Date.now() + timeout;
    while (true) {
      const idx = this._rxBuf.indexOf(terminator);
      if (idx !== -1) {
        const result = this._rxBuf.slice(0, idx);
        this._rxBuf = this._rxBuf.slice(idx + terminator.length);
        return result;
      }
      if (Date.now() > deadline) throw new Error(`Timeout waiting for terminator`);
      await this._sleep(20);
    }
  }

  // ── Low-level send ────────────────────────────────────────────────

  async _sendRaw(text) {
    const encoded = new TextEncoder().encode(text);
    await this.writer.write(encoded);
  }

  // ── Utilities ─────────────────────────────────────────────────────

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  _chunk(str, size) {
    const chunks = [];
    for (let i = 0; i < str.length; i += size) chunks.push(str.slice(i, i + size));
    return chunks;
  }

  // Produce a Python string literal from a JS string.
  // JSON.stringify handles all escaping: backslashes, quotes, newlines, etc.
  _pyStr(s) {
    return JSON.stringify(s);
  }
}
