/**
 * App
 *
 * Orchestrates the UI: connects device, loads exercises, manages the
 * CodeMirror editor(s), drives the console panel, and handles Save & Run.
 */
import { createProvider, loadLLMConfig, saveLLMConfig } from './llm.js';

export class App {
  constructor({ MicroPythonREPL, FirmwareInstaller, ExerciseLoader }) {
    this.repl = new MicroPythonREPL();
    this.firmware = new FirmwareInstaller(this.repl);
    this.exercises = new ExerciseLoader(this.repl);
    this.fileEditors = [];   // [{ tabId, spec, startCode, solutionCode, editor, element }]
    this.settingsEditor = null;
    this.currentExercise = null;
    this._fontSize = 13;
    this._settingsLoaded = false;
    this._llmProvider = null;
    this._hintMessages = [];
    this._hintBusy = false;
    this._theme = localStorage.getItem('clb-theme') ?? 'dark';
    this._pages = [];
    this._pageIndex = 0;
  }

  async init() {
    this._applyTheme(this._theme);
    this._initSettingsEditor();
    this._initHints();
    this._bindUI();
    await this._populateExerciseList();
  }

  // ── Settings editor ───────────────────────────────────────────────

  _initSettingsEditor() {
    this.settingsEditor = CodeMirror.fromTextArea(document.getElementById('settings-editor'), {
      mode: { name: 'javascript', json: true },
      theme: this._theme === 'dark' ? 'material-darker' : 'default',
      lineNumbers: true,
      lineWrapping: true,
      autofocus: false,
    });
    this.settingsEditor.setSize('100%', '100%');
    this.settingsEditor.setValue('// Connect a device to load settings.json');
  }

  // ── File editor tabs (dynamic) ────────────────────────────────────

  _loadExerciseEditors(exercise) {
    this._clearFileEditors();

    const tabBar = document.getElementById('editor-tabs');
    const staticTab = tabBar.querySelector('.editor-tab-static');
    const settingsPanel = document.getElementById('editor-tab-settings');
    const noExercise = document.getElementById('editor-no-exercise');

    exercise.files.forEach(({ spec, startCode, solutionCode }, i) => {
      const tabId = `file-${i}`;
      const isFirst = i === 0;

      // Tab button
      const tab = document.createElement('button');
      tab.className = 'editor-tab' + (isFirst ? ' active' : '');
      tab.dataset.editorTab = tabId;
      tab.textContent = spec.label;
      tab.addEventListener('click', () => this._switchEditorTab(tabId));
      tabBar.insertBefore(tab, staticTab);

      // Content pane
      const pane = document.createElement('div');
      pane.id = `editor-tab-${tabId}`;
      pane.className = 'editor-tab-content' + (isFirst ? ' active' : '');

      const toolbar = document.createElement('div');
      toolbar.className = 'editor-file-toolbar';
      toolbar.innerHTML = `<span class="dim">${spec.device_path}</span>`;
      pane.appendChild(toolbar);

      const textarea = document.createElement('textarea');
      pane.appendChild(textarea);

      settingsPanel.parentNode.insertBefore(pane, settingsPanel);

      const editor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        theme: this._theme === 'dark' ? 'material-darker' : 'default',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: false,
        autofocus: false,
      });
      editor.setSize('100%', '100%');
      editor.setValue(startCode);

      this.fileEditors.push({ tabId, spec, startCode, solutionCode, editor, element: pane });
    });

    // Hide placeholder, deactivate settings tab
    noExercise.classList.remove('active');
    staticTab.classList.remove('active');

    if (this.fileEditors.length > 0) {
      this.fileEditors[0].editor.refresh();
    }
  }

  _clearFileEditors() {
    this.fileEditors.forEach(({ editor, element }) => {
      editor.toTextArea();
      element.remove();
    });
    document.querySelectorAll('.editor-tab:not(.editor-tab-static)').forEach(t => t.remove());
    this.fileEditors = [];

    document.getElementById('editor-no-exercise').classList.add('active');
  }

  _refreshAllEditors() {
    this.fileEditors.forEach(({ editor }) => editor.refresh());
    if (this.settingsEditor) this.settingsEditor.refresh();
  }

  // ── UI bindings ───────────────────────────────────────────────────

  _bindUI() {
    document.getElementById('btn-connect').addEventListener('click', () => this._onConnect());
    document.getElementById('btn-save-run').addEventListener('click', () => this._onSaveRun());
    document.getElementById('btn-show-solution').addEventListener('click', () => this._onShowSolution());
    document.getElementById('btn-install-firmware').addEventListener('click', () => this._onInstallFirmware());
    document.getElementById('btn-console-clear').addEventListener('click', () => this._consoleClear());
    document.getElementById('btn-console-interrupt').addEventListener('click', () => this.repl.interrupt());
    document.getElementById('exercise-select').addEventListener('change', e => this._onExerciseSelected(e.target.value));
    document.getElementById('console-input').addEventListener('keydown', e => {
      if (e.key === 'Enter') this._onConsoleInput();
    });
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => this._switchTab(tab.dataset.tab));
    });
    document.getElementById('btn-page-prev').addEventListener('click', () => this._renderPage(this._pageIndex - 1));
    document.getElementById('btn-page-next').addEventListener('click', () => this._renderPage(this._pageIndex + 1));

    document.querySelector('.editor-tab-static').addEventListener('click', () =>
      this._switchEditorTab('settings'));
    document.getElementById('btn-settings-save').addEventListener('click', () => this._saveSettings());
    document.getElementById('btn-settings-reload').addEventListener('click', () => this._loadSettings());

    document.getElementById('btn-theme').addEventListener('click', () => {
      this._applyTheme(this._theme === 'dark' ? 'light' : 'dark');
    });

    document.getElementById('btn-font-decrease').addEventListener('click', () => this._adjustFontSize(-1));
    document.getElementById('btn-font-increase').addEventListener('click', () => this._adjustFontSize(1));
    document.addEventListener('keydown', e => {
      if (e.ctrlKey && (e.key === '=' || e.key === '+')) { e.preventDefault(); this._adjustFontSize(1); }
      if (e.ctrlKey && e.key === '-')  { e.preventDefault(); this._adjustFontSize(-1); }
      if (e.ctrlKey && e.key === '0')  { e.preventDefault(); this._setFontSize(13); }
    });

    this._initPanelResize();
    this._initConsoleResize();

    // Wire serial output to the console panel.
    this.repl.onData(text => this._consoleAppend(text));
  }

  // ── Exercise list ─────────────────────────────────────────────────

  async _populateExerciseList() {
    try {
      const list = await this.exercises.listExercises();
      const sel = document.getElementById('exercise-select');
      list.forEach(ex => {
        const opt = document.createElement('option');
        opt.value = ex.id;
        opt.textContent = `${ex.id.split('_')[0]}. ${ex.title}`;
        sel.appendChild(opt);
      });
    } catch (e) {
      console.error('Could not load exercise list:', e);
    }
  }

  // ── Event handlers ────────────────────────────────────────────────

  async _onConnect() {
    const btn = document.getElementById('btn-connect');
    if (this.repl.connected) {
      await this.repl.disconnect();
      this._setConnected(false);
      return;
    }
    try {
      btn.disabled = true;
      btn.textContent = 'Connecting…';
      await this.repl.connect();
      this._setConnected(true);
      // If an exercise was already selected before connecting, configure the device now.
      if (this.currentExercise) {
        await this._pushExerciseToDevice(this.currentExercise);
      }
    } catch (e) {
      this._setConnected(false);
      this._consoleAppend(`\nConnection failed: ${e.message}\n`);
    }
  }

  async _onExerciseSelected(id) {
    if (!id) return;
    try {
      const exercise = await this.exercises.loadExercise(id);
      this.currentExercise = exercise;
      this._pages = exercise.pages;
      this._renderPage(0);
      this._loadExerciseEditors(exercise);
      this._hintMessages = [];
      document.getElementById('hints-messages').innerHTML = '';
      this._updateHintsReadyState();
      const hasSolution = exercise.files.some(f => f.solutionCode);
      document.getElementById('btn-show-solution').disabled = !hasSolution;

      if (this.repl.connected) {
        await this._pushExerciseToDevice(exercise);
      }
    } catch (e) {
      this._consoleAppend(`\nFailed to load exercise: ${e.message}\n`);
    }
  }

  async _pushExerciseToDevice(exercise) {
    const btn = document.getElementById('btn-save-run');
    btn.disabled = true;
    btn.textContent = 'Setting up…';
    try {
      await this.exercises.setupExercise(exercise);
      await this.repl.softReset();
    } catch (e) {
      this._consoleAppend(`\nDevice setup failed: ${e.message}\n`);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Save & Run';
    }
  }

  async _onSaveRun() {
    if (!this.repl.connected || !this.currentExercise) return;
    const btn = document.getElementById('btn-save-run');
    btn.disabled = true;
    btn.textContent = 'Saving…';
    try {
      for (const { spec, editor } of this.fileEditors) {
        await this.repl.writeFile(spec.device_path, editor.getValue());
      }

      // Always keep app_manifest.py in sync so the device knows which app to run.
      const manifest = this.exercises._buildManifest(this.currentExercise.meta);
      await this.repl.writeFile('/app_manifest.py', manifest);

      btn.textContent = 'Rebooting…';
      await this.repl.softReset();
    } catch (e) {
      this._consoleAppend(`\nSave failed: ${e.message}\n`);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Save & Run';
    }
  }

  _onShowSolution() {
    if (!this.currentExercise) return;
    const confirmed = confirm(
      'Replace the editor with the complete solution?\n' +
      'Your current code will be lost unless you copy it first.'
    );
    if (!confirmed) return;
    this.fileEditors.forEach(({ solutionCode, editor }) => {
      if (solutionCode) editor.setValue(solutionCode);
    });
  }

  async _onInstallFirmware() {
    if (!this.repl.connected) return;
    const confirmed = confirm(
      'This will install the CLB firmware onto your device.\n' +
      'Any existing files will be overwritten (except settings.json).\n\nContinue?'
    );
    if (!confirmed) return;

    const container = document.getElementById('progress-bar-container');
    const fill = document.getElementById('progress-bar-fill');
    const label = document.getElementById('progress-bar-label');
    container.classList.remove('hidden');

    try {
      await this.firmware.install((pct, msg) => {
        fill.style.width = `${pct}%`;
        label.textContent = msg;
      });
      await this.repl.softReset();
    } catch (e) {
      this._consoleAppend(`\nFirmware install failed: ${e.message}\n`);
    } finally {
      container.classList.add('hidden');
    }
  }

  _onConsoleInput() {
    const input = document.getElementById('console-input');
    const line = input.value;
    input.value = '';
    this._consoleAppend(line + '\n');
    this.repl.sendLine(line);
  }

  // ── Editor tab switching ──────────────────────────────────────────

  _switchEditorTab(name) {
    document.querySelectorAll('.editor-tab').forEach(t =>
      t.classList.toggle('active', t.dataset.editorTab === name));
    document.querySelectorAll('.editor-tab-content').forEach(c =>
      c.classList.toggle('active', c.id === `editor-tab-${name}`));

    if (name === 'settings') {
      this.settingsEditor.refresh();
      if (this.repl.connected && !this._settingsLoaded) this._loadSettings();
    } else {
      const fe = this.fileEditors.find(e => e.tabId === name);
      if (fe) fe.editor.refresh();
    }
  }

  // ── Settings file ─────────────────────────────────────────────────

  async _loadSettings() {
    const status = document.getElementById('settings-status');
    status.textContent = 'Loading…';
    try {
      const content = await this.repl.readFile('/settings.json');
      this.settingsEditor.setValue(content);
      this._settingsLoaded = true;
      status.textContent = '';
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    }
  }

  async _saveSettings() {
    const status = document.getElementById('settings-status');
    const btn = document.getElementById('btn-settings-save');
    try {
      JSON.parse(this.settingsEditor.getValue());
    } catch (e) {
      status.textContent = `Invalid JSON: ${e.message}`;
      return;
    }
    btn.disabled = true;
    status.textContent = 'Saving…';
    try {
      await this.repl.writeFile('/settings.json', this.settingsEditor.getValue());
      status.textContent = 'Saved';
      setTimeout(() => { status.textContent = ''; }, 2000);
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    } finally {
      btn.disabled = false;
    }
  }

  // ── Theme ─────────────────────────────────────────────────────────

  _applyTheme(theme) {
    this._theme = theme;
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('clb-theme', theme);
    document.getElementById('btn-theme').textContent = theme === 'dark' ? '☀' : '☾';

    const cmTheme = theme === 'dark' ? 'material-darker' : 'default';
    this.fileEditors.forEach(({ editor }) => editor.setOption('theme', cmTheme));
    if (this.settingsEditor) this.settingsEditor.setOption('theme', cmTheme);
  }

  // ── Font size ─────────────────────────────────────────────────────

  _adjustFontSize(delta) {
    this._setFontSize(Math.max(10, Math.min(24, this._fontSize + delta)));
  }

  _setFontSize(size) {
    this._fontSize = size;
    document.documentElement.style.setProperty('--base-size', size + 'px');
    this._refreshAllEditors();
  }

  // ── Panel resize ──────────────────────────────────────────────────

  _initPanelResize() {
    const divider = document.getElementById('panel-divider');
    const panelLeft = document.getElementById('panel-left');
    let dragging = false;
    let startX, startWidth;

    divider.addEventListener('mousedown', e => {
      dragging = true;
      startX = e.clientX;
      startWidth = panelLeft.offsetWidth;
      divider.classList.add('dragging');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });

    document.addEventListener('mousemove', e => {
      if (!dragging) return;
      const maxWidth = window.innerWidth - 300;
      const newWidth = Math.max(200, Math.min(maxWidth, startWidth + (e.clientX - startX)));
      panelLeft.style.width = newWidth + 'px';
    });

    document.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      divider.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      this._refreshAllEditors();
    });
  }

  _initConsoleResize() {
    const divider = document.getElementById('console-divider');
    const consolePane = document.getElementById('console-pane');
    let dragging = false;
    let startY, startHeight;

    divider.addEventListener('mousedown', e => {
      dragging = true;
      startY = e.clientY;
      startHeight = consolePane.offsetHeight;
      divider.classList.add('dragging');
      document.body.style.cursor = 'row-resize';
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });

    document.addEventListener('mousemove', e => {
      if (!dragging) return;
      const panelRight = document.getElementById('panel-right');
      const maxHeight = panelRight.offsetHeight - 80;
      const newHeight = Math.max(60, Math.min(maxHeight, startHeight - (e.clientY - startY)));
      consolePane.style.height = newHeight + 'px';
    });

    document.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      divider.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      this._refreshAllEditors();
    });
  }

  // ── State helpers ─────────────────────────────────────────────────

  _setConnected(connected) {
    const badge = document.getElementById('device-status');
    const btn = document.getElementById('btn-connect');
    const input = document.getElementById('console-input');
    const interrupt = document.getElementById('btn-console-interrupt');
    const firmware = document.getElementById('btn-install-firmware');
    const exerciseSelect = document.getElementById('exercise-select');

    badge.textContent = connected ? 'Connected' : 'Disconnected';
    badge.className = `status-badge ${connected ? 'status-connected' : 'status-disconnected'}`;
    btn.textContent = connected ? 'Disconnect' : 'Connect Device';
    btn.disabled = false;
    input.disabled = !connected;
    interrupt.disabled = !connected;
    firmware.disabled = !connected;
    exerciseSelect.disabled = false;

    document.getElementById('btn-settings-save').disabled = !connected;
    document.getElementById('btn-settings-reload').disabled = !connected;
    if (!connected) {
      this._settingsLoaded = false;
      this.settingsEditor.setValue('// Connect a device to load settings.json');
      document.getElementById('settings-status').textContent = '';
    }

    if (connected && this.currentExercise) {
      document.getElementById('btn-save-run').disabled = false;
    }
  }

  // ── Console ───────────────────────────────────────────────────────

  _stripAnsi(text) {
    return text.replace(/\x1b(\[[0-9;]*[A-Za-z]|O[A-Za-z]|.)/g, '');
  }

  _consoleAppend(text) {
    const output = document.getElementById('console-output');
    const atBottom = output.scrollHeight - output.scrollTop <= output.clientHeight + 4;
    const span = document.createElement('span');
    span.textContent = this._stripAnsi(text);
    output.appendChild(span);
    if (atBottom) output.scrollTop = output.scrollHeight;
  }

  _consoleClear() {
    document.getElementById('console-output').innerHTML = '';
  }

  // ── Rendering ─────────────────────────────────────────────────────

  _renderPage(index) {
    this._pageIndex = index;
    this._renderDescription(this._pages[index], this.currentExercise.base);

    const nav   = document.getElementById('description-nav');
    const total = this._pages.length;
    if (total <= 1) { nav.classList.add('hidden'); return; }

    nav.classList.remove('hidden');
    document.getElementById('page-indicator').textContent = `${index + 1} / ${total}`;
    document.getElementById('btn-page-prev').disabled = index === 0;
    document.getElementById('btn-page-next').disabled = index === total - 1;
    document.getElementById('description-content').scrollTop = 0;
  }

  _renderDescription(markdown, base) {
    const scratch = document.createElement('div');
    scratch.innerHTML = marked.parse(markdown);
    if (base) {
      scratch.querySelectorAll('img').forEach(img => {
        const src = img.getAttribute('src');
        if (src && !/^https?:/.test(src)) {
          img.src = `${base}/${src}`;
        }
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
      });
    }
    document.getElementById('description-content').innerHTML = scratch.innerHTML;
  }

  // ── Hints / AI tutor ─────────────────────────────────────────────

  _initHints() {
    const cfg = loadLLMConfig();
    this._llmProvider = createProvider(cfg);
    this._populateHintsConfig(cfg);

    document.getElementById('btn-hints-config').addEventListener('click', () =>
      document.getElementById('hints-config').classList.toggle('hidden'));

    document.getElementById('hints-provider').addEventListener('change', e =>
      this._onHintsProviderChange(e.target.value));

    document.getElementById('btn-hints-save').addEventListener('click', () =>
      this._saveHintsConfig());

    const input = document.getElementById('hints-input');
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._sendHint(); }
    });
    document.getElementById('btn-hints-send').addEventListener('click', () => this._sendHint());

    this._updateHintsReadyState();
  }

  _populateHintsConfig(cfg) {
    document.getElementById('hints-provider').value = cfg.provider ?? '';
    this._onHintsProviderChange(cfg.provider ?? '');
    if (cfg.gemini) {
      document.getElementById('hints-gemini-key').value   = cfg.gemini.apiKey ?? '';
      document.getElementById('hints-gemini-model').value = cfg.gemini.model ?? '';
    }
    if (cfg.groq) {
      document.getElementById('hints-groq-key').value   = cfg.groq.apiKey ?? '';
      document.getElementById('hints-groq-model').value = cfg.groq.model ?? '';
    }
    if (cfg.ollama) {
      document.getElementById('hints-ollama-url').value   = cfg.ollama.baseUrl ?? '';
      document.getElementById('hints-ollama-model').value = cfg.ollama.model ?? '';
    }
  }

  _onHintsProviderChange(provider) {
    document.getElementById('hints-config-gemini').classList.toggle('hidden', provider !== 'gemini');
    document.getElementById('hints-config-groq').classList.toggle('hidden', provider !== 'groq');
    document.getElementById('hints-config-ollama').classList.toggle('hidden', provider !== 'ollama');
  }

  _saveHintsConfig() {
    const provider = document.getElementById('hints-provider').value;
    const cfg = {
      provider,
      gemini: {
        apiKey: document.getElementById('hints-gemini-key').value.trim(),
        model:  document.getElementById('hints-gemini-model').value.trim() || 'gemini-2.0-flash',
      },
      groq: {
        apiKey: document.getElementById('hints-groq-key').value.trim(),
        model:  document.getElementById('hints-groq-model').value.trim() || 'llama-3.1-8b-instant',
      },
      ollama: {
        baseUrl: document.getElementById('hints-ollama-url').value.trim() || 'http://localhost:11434',
        model:   document.getElementById('hints-ollama-model').value.trim() || 'llama3.2',
      },
    };
    saveLLMConfig(cfg);
    this._llmProvider = createProvider(cfg);
    document.getElementById('hints-config').classList.add('hidden');
    this._updateHintsReadyState();
  }

  _updateHintsReadyState() {
    const ready = this._llmProvider !== null && this.currentExercise?.tutor != null && !this._hintBusy;
    document.getElementById('hints-input').disabled    = !ready;
    document.getElementById('btn-hints-send').disabled = !ready;

    const ph = document.getElementById('hints-placeholder');
    if (ph) {
      if (!this._llmProvider) {
        ph.textContent = 'Configure an AI provider (⚙) to ask for hints.';
      } else if (!this.currentExercise?.tutor) {
        ph.textContent = 'Select an exercise to use the AI tutor.';
      } else {
        ph.style.display = 'none';
        return;
      }
      ph.style.display = '';
    }
  }

  async _sendHint() {
    if (this._hintBusy || !this._llmProvider || !this.currentExercise?.tutor) return;
    const input = document.getElementById('hints-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    this._hintMessages.push({ role: 'user', content: text });
    this._appendHintMsg('user', text);

    this._hintBusy = true;
    this._updateHintsReadyState();

    const msgEl  = this._appendHintMsg('assistant', '');
    const textEl = msgEl.querySelector('.hint-msg-text');
    textEl.classList.add('hint-msg-thinking');
    textEl.textContent = '…';

    let response = '';
    try {
      const system = this.currentExercise.tutor.tutor_brief;
      for await (const chunk of this._llmProvider.chat(this._hintMessages, system)) {
        if (!response) {
          textEl.classList.remove('hint-msg-thinking');
          textEl.textContent = '';
        }
        response += chunk;
        textEl.textContent = response;
        const msgs = document.getElementById('hints-messages');
        msgs.scrollTop = msgs.scrollHeight;
      }
      this._hintMessages.push({ role: 'assistant', content: response });
    } catch (e) {
      textEl.classList.add('hint-msg-thinking');
      textEl.textContent = `Error: ${e.message}`;
    } finally {
      this._hintBusy = false;
      this._updateHintsReadyState();
    }
  }

  _appendHintMsg(role, text) {
    const msgs = document.getElementById('hints-messages');

    const div     = document.createElement('div');
    div.className = `hint-msg hint-msg-${role}`;

    const roleEl      = document.createElement('span');
    roleEl.className  = 'hint-msg-role';
    roleEl.textContent = role === 'user' ? 'You' : 'Tutor';

    const textEl      = document.createElement('span');
    textEl.className  = 'hint-msg-text';
    textEl.textContent = text;

    div.appendChild(roleEl);
    div.appendChild(textEl);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  _switchTab(name) {
    document.querySelectorAll('.tab').forEach(t =>
      t.classList.toggle('active', t.dataset.tab === name));
    document.querySelectorAll('.tab-content').forEach(c =>
      c.classList.toggle('active', c.id === `tab-${name}`));
  }
}
