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
    this.fileEditors = [];          // [{ tabId, spec, startCode, solutionCode, editor, element }]
    this._deviceFileEditors = [];   // [{ tabId, path, editor, element, tabBtn, loadedContent }]
    this._solutionTabs = [];        // [{ tabId, label, editor, element, tabBtn }]
    this._nextDeviceTabId = 0;
    this._fileBrowserPath = '/';
    this._fileBrowserOpen = false;
    this._imageViewerOpen = false;
    this._activeEditorTab = null;
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
    this._homeDescriptionHTML = document.getElementById('description-content').innerHTML;
    this._applyTheme(this._theme);
    this._initMarked();
    this._initSettingsEditor();
    this._initHints();
    this._bindUI();
    await this._populateExerciseList();
  }

  _initMarked() {
    marked.use({
      renderer: {
        code(text, lang) {
          const tags = lang ? lang.split(/\s+/) : [];
          const wantsCopy = tags.includes('copy');
          const langName = tags[0] && tags[0] !== 'copy' ? tags[0] : '';
          const html = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
          const codeTag = langName
            ? `<code class="language-${langName}">${html}</code>`
            : `<code>${html}</code>`;
          const copyBtn = wantsCopy
            ? '<button class="copy-code-btn">Copy</button>'
            : '';
          return `<pre>${codeTag}${copyBtn}</pre>\n`;
        }
      }
    });
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

  // ── File editor tabs (exercise) ───────────────────────────────────

  _loadExerciseEditors(exercise) {
    this._clearFileEditors();

    const tabBar      = document.getElementById('editor-tabs');
    const insertRef   = document.getElementById('editor-tabs-end');
    const settingsPanel = document.getElementById('editor-tab-settings');
    const noExercise  = document.getElementById('editor-no-exercise');

    exercise.files.forEach(({ spec, startCode, solutionCode }, i) => {
      const tabId   = `file-${i}`;
      const isFirst = i === 0;

      // Tab button — same structure as device file tabs
      const tab = document.createElement('button');
      tab.className = 'editor-tab editor-tab-exercise' + (isFirst ? ' active' : '');
      tab.dataset.editorTab = tabId;
      tab.addEventListener('click', () => this._switchEditorTab(tabId));

      const nameSpan = document.createElement('span');
      nameSpan.className = 'tab-name';
      nameSpan.textContent = spec.label;
      tab.appendChild(nameSpan);

      const closeBtn = document.createElement('button');
      closeBtn.className = 'tab-close-btn';
      closeBtn.title = 'Close tab';
      closeBtn.innerHTML = '&times;';
      closeBtn.addEventListener('click', e => { e.stopPropagation(); this._closeExerciseTab(tabId); });
      tab.appendChild(closeBtn);

      tabBar.insertBefore(tab, insertRef);

      // Content pane — same structure as device file tabs
      const pane = document.createElement('div');
      pane.id = `editor-tab-${tabId}`;
      pane.className = 'editor-tab-content' + (isFirst ? ' active' : '');

      const toolbar = document.createElement('div');
      toolbar.className = 'editor-file-toolbar';

      const pathSpan = document.createElement('span');
      pathSpan.className = 'dim';
      pathSpan.textContent = spec.device_path;
      toolbar.appendChild(pathSpan);

      const statusSpan = document.createElement('span');
      statusSpan.className = 'device-file-status';
      toolbar.appendChild(statusSpan);

      const saveBtn = document.createElement('button');
      saveBtn.className = 'btn btn-tiny';
      saveBtn.textContent = 'Save';
      saveBtn.disabled = !this.repl.connected;
      saveBtn.addEventListener('click', () => this._saveExerciseFile(tabId));
      toolbar.appendChild(saveBtn);

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
      this._addWhitespaceOverlay(editor);

      const entry = { tabId, spec, startCode, solutionCode, editor, element: pane, tabBtn: tab, loadedContent: startCode };
      this.fileEditors.push(entry);
      editor.on('change', () => this._updateExerciseTabLabel(entry));
    });

    if (this.fileEditors.length > 0) {
      noExercise.classList.remove('active');
      document.querySelector('.editor-tab-static').classList.remove('active');
      this._activeEditorTab = this.fileEditors[0].tabId;
      this.fileEditors[0].editor.refresh();
    } else {
      noExercise.classList.add('active', 'console-mode');
    }
  }

  _clearFileEditors() {
    this._solutionTabs.forEach(({ editor, element, tabBtn }) => {
      editor.toTextArea();
      element.remove();
      tabBtn.remove();
    });
    this._solutionTabs = [];

    this.fileEditors.forEach(({ editor, element }) => {
      editor.toTextArea();
      element.remove();
    });
    document.querySelectorAll('.editor-tab-exercise').forEach(t => t.remove());
    this.fileEditors = [];
    const noEx = document.getElementById('editor-no-exercise');
    noEx.classList.add('active');
    noEx.classList.remove('console-mode');
  }

  _refreshAllEditors() {
    this.fileEditors.forEach(({ editor }) => editor.refresh());
    this._deviceFileEditors.forEach(({ editor }) => editor.refresh());
    this._solutionTabs.forEach(({ editor }) => editor.refresh());
    if (this.settingsEditor) this.settingsEditor.refresh();
  }

  // ── UI bindings ───────────────────────────────────────────────────

  _bindUI() {
    document.getElementById('btn-connect').addEventListener('click', () => this._onConnect());
    document.getElementById('btn-save').addEventListener('click', () => this._onSave());
    document.getElementById('btn-run').addEventListener('click', () => this._onRun());
    document.getElementById('btn-stop').addEventListener('click', () => this._onStop());
    document.getElementById('btn-restart').addEventListener('click', () => this._onRestart());
    document.getElementById('btn-show-solution').addEventListener('click', () => this._onShowSolution());
    document.getElementById('btn-install-firmware').addEventListener('click', () => this._onInstallFirmware());
    document.getElementById('btn-console-clear').addEventListener('click', () => this._consoleClear());
    document.getElementById('exercise-select').addEventListener('change', e => this._onExerciseSelected(e.target.value));
    document.getElementById('console-input').addEventListener('keydown', e => {
      if (e.key === 'Enter') this._onConsoleInput();
    });
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => this._switchTab(tab.dataset.tab));
    });
    document.getElementById('btn-page-prev').addEventListener('click', () => this._renderPage(this._pageIndex - 1));
    document.getElementById('btn-page-next').addEventListener('click', () => {
      const btn = document.getElementById('btn-page-next');
      if (btn.dataset.nextExercise) {
        this._navigateToExercise(btn.dataset.nextExercise);
      } else {
        this._renderPage(this._pageIndex + 1);
      }
    });

    document.querySelector('.editor-tab-static').addEventListener('click', () =>
      this._switchEditorTab('settings'));
    document.getElementById('btn-settings-save').addEventListener('click', () => this._saveSettings());
    document.getElementById('btn-settings-reload').addEventListener('click', () => this._loadSettings());

    document.getElementById('btn-browse-files').addEventListener('click', () => this._toggleFileBrowser());
    document.getElementById('btn-file-browser-close').addEventListener('click', () => this._closeFileBrowser());

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

    document.getElementById('description-content').addEventListener('click', e => {
      const btn = e.target.closest('.copy-code-btn');
      if (!btn) return;
      const code = btn.closest('pre')?.querySelector('code');
      const text = (code ?? btn.closest('pre'))?.textContent ?? '';
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      });
    });

    document.getElementById('brand').addEventListener('click', () => this._goHome());
    document.getElementById('btn-image-viewer-close').addEventListener('click', () => this._closeImageViewer());
    document.getElementById('image-viewer-body').addEventListener('click', () => this._closeImageViewer());

    this._initPanelResize();
    this._initConsoleResize();

    this.repl.onData(text => this._consoleAppend(text));
  }

  // ── Exercise list ─────────────────────────────────────────────────

  async _populateExerciseList() {
    try {
      const list = await this.exercises.listExercises();
      const sel = document.getElementById('exercise-select');
      let currentChapter = null;
      let group = null;

      list.forEach(ex => {
        if (ex.chapter !== undefined && ex.chapter !== currentChapter) {
          currentChapter = ex.chapter;
          group = document.createElement('optgroup');
          group.label = ex.chapter_title ?? `Chapter ${ex.chapter}`;
          sel.appendChild(group);
        }
        const opt = document.createElement('option');
        opt.value = ex.id;
        opt.textContent = ex.title;
        (group ?? sel).appendChild(opt);
      });
      sel.disabled = false;
      this._populateLandingPage(list);
    } catch (e) {
      console.error('Could not load exercise list:', e);
    }
  }

  _populateLandingPage(list) {
    const container = document.getElementById('landing-exercise-list');
    if (!container) return;
    let currentChapter = null;

    list.forEach(ex => {
      if (ex.chapter !== undefined && ex.chapter !== currentChapter) {
        currentChapter = ex.chapter;
        const h = document.createElement('h3');
        h.className = 'landing-chapter-heading';
        h.textContent = ex.chapter_title ?? `Chapter ${ex.chapter}`;
        container.appendChild(h);
      }

      const btn = document.createElement('button');
      btn.className = 'landing-exercise-item';
      btn.addEventListener('click', () => this._navigateToExercise(ex.id));

      const title = document.createElement('strong');
      title.textContent = ex.title;
      btn.appendChild(title);

      if (ex.desc) {
        const desc = document.createElement('p');
        desc.textContent = ex.desc;
        btn.appendChild(desc);
      }

      container.appendChild(btn);
    });
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
      document.getElementById('btn-download-notes').href = `pdfs/${exercise.meta.id}.pdf`;
      this._updateRunControls();

      if (this.repl.connected) {
        await this._pushExerciseToDevice(exercise);
      }
    } catch (e) {
      this._consoleAppend(`\nFailed to load exercise: ${e.message}\n`);
    }
  }

  async _pushExerciseToDevice(exercise) {
    const btnSave = document.getElementById('btn-save');
    const btnRun = document.getElementById('btn-run');
    btnSave.disabled = true;
    btnRun.disabled = true;
    btnRun.textContent = 'Setting up…';
    try {
      await this.exercises.setupExercise(exercise);
      await this.repl.softReset();
    } catch (e) {
      this._consoleAppend(`\nDevice setup failed: ${e.message}\n`);
    } finally {
      btnRun.textContent = 'Run';
      this._updateRunControls();
    }
  }

  async _doSaveAll() {
    for (const entry of this.fileEditors) {
      await this.repl.writeFile(entry.spec.device_path, entry.editor.getValue());
      entry.loadedContent = entry.editor.getValue();
      this._updateExerciseTabLabel(entry);
    }
    for (const entry of this._deviceFileEditors) {
      if (entry.editor.getValue() !== entry.loadedContent) {
        await this._saveDeviceFile(entry.tabId);
      }
    }
    if (this.currentExercise) {
      if (this.currentExercise.meta.clb !== false) {
        const manifest = this.exercises._buildManifest(this.currentExercise.meta);
        await this.repl.writeFile('/app_manifest.py', manifest);
      } else if (this.fileEditors.length > 0) {
        const path = this.fileEditors[0].spec.device_path;
        await this.repl.writeFile('/main.py', `exec(open('${path}').read())\n`);
      }
    }
  }

  async _onSave() {
    if (!this.repl.connected) return;
    const btn = document.getElementById('btn-save');
    btn.disabled = true;
    btn.textContent = 'Saving…';
    try {
      await this._doSaveAll();
    } catch (e) {
      this._consoleAppend(`\nSave failed: ${e.message}\n`);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Save';
    }
  }

  async _onRun() {
    if (!this.repl.connected) return;
    const btnSave = document.getElementById('btn-save');
    const btnRun = document.getElementById('btn-run');
    btnSave.disabled = true;
    btnRun.disabled = true;
    btnRun.textContent = 'Saving…';
    try {
      await this._doSaveAll();
      btnRun.textContent = 'Rebooting…';
      await this.repl.softReset();
    } catch (e) {
      this._consoleAppend(`\nRun failed: ${e.message}\n`);
    } finally {
      btnSave.disabled = false;
      btnRun.textContent = 'Run';
      this._updateRunControls();
    }
  }

  _onStop() {
    this.repl.interrupt();
  }

  async _onRestart() {
    await this.repl.softReset();
  }

  _onShowSolution() {
    if (!this.currentExercise) return;
    this.fileEditors.forEach(entry => {
      if (entry.solutionCode) this._openSolutionTab(entry);
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
    if (this._fileBrowserOpen) {
      this._fileBrowserOpen = false;
      document.getElementById('file-browser').classList.remove('active');
    }
    if (this._imageViewerOpen) {
      this._imageViewerOpen = false;
      document.getElementById('image-viewer').classList.remove('active');
      document.getElementById('image-viewer-img').src = '';
    }
    this._activeEditorTab = name;

    document.querySelectorAll('.editor-tab').forEach(t =>
      t.classList.toggle('active', t.dataset.editorTab === name));
    document.querySelectorAll('.editor-tab-content').forEach(c =>
      c.classList.toggle('active', c.id === `editor-tab-${name}`));

    if (name === 'settings') {
      this.settingsEditor.refresh();
      if (this.repl.connected && !this._settingsLoaded) this._loadSettings();
    } else {
      const fe = this.fileEditors.find(e => e.tabId === name);
      if (fe) { fe.editor.refresh(); return; }
      const dfe = this._deviceFileEditors.find(e => e.tabId === name);
      if (dfe) { dfe.editor.refresh(); return; }
      const st = this._solutionTabs.find(e => e.tabId === name);
      if (st) st.editor.refresh();
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

  // ── File browser ──────────────────────────────────────────────────

  _toggleFileBrowser() {
    if (this._fileBrowserOpen) {
      this._closeFileBrowser();
    } else {
      this._openFileBrowser();
    }
  }

  async _openFileBrowser() {
    if (!this.repl.connected) return;
    this._fileBrowserOpen = true;
    document.querySelectorAll('.editor-tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.editor-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('file-browser').classList.add('active');
    await this._browseTo(this._fileBrowserPath);
  }

  _closeFileBrowser() {
    if (!this._fileBrowserOpen) return;
    this._fileBrowserOpen = false;
    document.getElementById('file-browser').classList.remove('active');
    this._switchEditorTab(this._activeEditorTab ?? 'settings');
  }

  async _browseTo(path) {
    this._fileBrowserPath = path;
    const status = document.getElementById('file-browser-status');
    const list   = document.getElementById('file-browser-list');

    this._renderBreadcrumb(path);
    status.textContent = 'Loading…';
    list.innerHTML = '';

    try {
      const entries = await this.repl.listDirDetailed(path);
      status.textContent = '';
      this._renderFileBrowserList(entries, path);
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    }
  }

  _renderBreadcrumb(path) {
    const nav = document.getElementById('file-browser-breadcrumb');
    nav.innerHTML = '';

    const segments = path.split('/').filter(Boolean);

    const rootEl = document.createElement(path === '/' ? 'span' : 'button');
    rootEl.className = path === '/' ? 'breadcrumb-current' : 'breadcrumb-seg';
    rootEl.textContent = '/';
    if (path !== '/') rootEl.addEventListener('click', () => this._browseTo('/'));
    nav.appendChild(rootEl);

    segments.forEach((seg, i) => {
      const sep = document.createElement('span');
      sep.className = 'breadcrumb-sep';
      sep.textContent = ' › ';
      nav.appendChild(sep);

      const segPath = '/' + segments.slice(0, i + 1).join('/');
      const isLast  = i === segments.length - 1;
      const el = document.createElement(isLast ? 'span' : 'button');
      el.className = isLast ? 'breadcrumb-current' : 'breadcrumb-seg';
      el.textContent = seg;
      if (!isLast) el.addEventListener('click', () => this._browseTo(segPath));
      nav.appendChild(el);
    });
  }

  _renderFileBrowserList(entries, path) {
    const list = document.getElementById('file-browser-list');

    if (entries.length === 0) {
      const msg = document.createElement('p');
      msg.className = 'placeholder';
      msg.style.padding = '16px';
      msg.textContent = 'Empty directory';
      list.appendChild(msg);
      return;
    }

    entries.forEach(({ name, isDir }) => {
      const btn = document.createElement('button');
      btn.className = `file-entry ${isDir ? 'file-entry-dir' : 'file-entry-file'}`;

      const icon = document.createElement('span');
      icon.className = 'file-entry-icon';
      icon.textContent = isDir ? '▸' : '·';
      btn.appendChild(icon);

      const label = document.createElement('span');
      label.textContent = isDir ? name + '/' : name;
      btn.appendChild(label);

      const childPath = path === '/' ? `/${name}` : `${path}/${name}`;
      if (isDir) {
        btn.addEventListener('click', () => this._browseTo(childPath));
      } else {
        btn.addEventListener('click', () => this._openDeviceFile(childPath));
      }

      list.appendChild(btn);
    });
  }

  // ── Device file tabs ──────────────────────────────────────────────

  async _openDeviceFile(path) {
    // If already open, just switch to it.
    const existing = this._deviceFileEditors.find(e => e.path === path);
    if (existing) {
      this._closeFileBrowser();
      this._switchEditorTab(existing.tabId);
      return;
    }

    const status = document.getElementById('file-browser-status');
    status.textContent = 'Opening…';
    try {
      const content = await this.repl.readFile(path);
      this._createDeviceFileTab(path, content);
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    }
  }

  _createDeviceFileTab(path, content) {
    const tabId    = `device-${this._nextDeviceTabId++}`;
    const filename = path.split('/').pop();
    const tabBar   = document.getElementById('editor-tabs');
    const insertRef = document.getElementById('editor-tabs-end');

    // Tab button
    const tab = document.createElement('button');
    tab.className = 'editor-tab editor-tab-device';
    tab.dataset.editorTab = tabId;
    tab.addEventListener('click', () => this._switchEditorTab(tabId));

    const nameSpan = document.createElement('span');
    nameSpan.className = 'tab-name';
    nameSpan.textContent = filename;
    tab.appendChild(nameSpan);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'tab-close-btn';
    closeBtn.title = 'Close tab';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', e => { e.stopPropagation(); this._closeDeviceTab(tabId); });
    tab.appendChild(closeBtn);

    tabBar.insertBefore(tab, insertRef);

    // Content pane
    const pane = document.createElement('div');
    pane.id = `editor-tab-${tabId}`;
    pane.className = 'editor-tab-content';

    const toolbar = document.createElement('div');
    toolbar.className = 'editor-file-toolbar';

    const pathSpan = document.createElement('span');
    pathSpan.className = 'dim';
    pathSpan.textContent = path;
    toolbar.appendChild(pathSpan);

    const statusSpan = document.createElement('span');
    statusSpan.className = 'device-file-status';
    toolbar.appendChild(statusSpan);

    const saveBtn = document.createElement('button');
    saveBtn.className = 'btn btn-tiny';
    saveBtn.textContent = 'Save';
    saveBtn.addEventListener('click', () => this._saveDeviceFile(tabId));
    toolbar.appendChild(saveBtn);

    pane.appendChild(toolbar);

    const textarea = document.createElement('textarea');
    pane.appendChild(textarea);

    document.getElementById('editor-tab-settings').parentNode
      .insertBefore(pane, document.getElementById('editor-tab-settings'));

    const editor = CodeMirror.fromTextArea(textarea, {
      mode: this._modeForPath(path),
      theme: this._theme === 'dark' ? 'material-darker' : 'default',
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      lineWrapping: false,
      autofocus: false,
    });
    editor.setSize('100%', '100%');
    editor.setValue(content);
    if (this._modeForPath(path) === 'python') this._addWhitespaceOverlay(editor);

    const entry = { tabId, path, editor, element: pane, tabBtn: tab, loadedContent: content };
    this._deviceFileEditors.push(entry);
    editor.on('change', () => this._updateDeviceTabLabel(entry));

    this._closeFileBrowser();
    this._switchEditorTab(tabId);
  }

  _closeDeviceTab(tabId) {
    const idx = this._deviceFileEditors.findIndex(e => e.tabId === tabId);
    if (idx === -1) return;
    const { editor, element, tabBtn, path, loadedContent } = this._deviceFileEditors[idx];

    if (editor.getValue() !== loadedContent) {
      if (!confirm(`Close ${path.split('/').pop()}?\nUnsaved changes will be lost.`)) return;
    }

    editor.toTextArea();
    element.remove();
    tabBtn.remove();
    this._deviceFileEditors.splice(idx, 1);

    if (this._deviceFileEditors.length > 0) {
      const next = this._deviceFileEditors[Math.min(idx, this._deviceFileEditors.length - 1)];
      this._switchEditorTab(next.tabId);
    } else if (this.fileEditors.length > 0) {
      this._switchEditorTab(this.fileEditors[0].tabId);
    } else {
      this._switchEditorTab('settings');
    }
  }

  async _saveDeviceFile(tabId) {
    const entry = this._deviceFileEditors.find(e => e.tabId === tabId);
    if (!entry) return;

    const statusSpan = entry.element.querySelector('.device-file-status');
    const saveBtn    = entry.element.querySelector('.btn');
    saveBtn.disabled = true;
    statusSpan.textContent = 'Saving…';

    try {
      await this.repl.writeFile(entry.path, entry.editor.getValue());
      entry.loadedContent = entry.editor.getValue();
      this._updateDeviceTabLabel(entry);
      statusSpan.textContent = 'Saved';
      setTimeout(() => { statusSpan.textContent = ''; }, 2000);
    } catch (e) {
      statusSpan.textContent = `Error: ${e.message}`;
    } finally {
      saveBtn.disabled = false;
    }
  }

  _updateDeviceTabLabel(entry) {
    const modified = entry.editor.getValue() !== entry.loadedContent;
    const filename  = entry.path.split('/').pop();
    entry.tabBtn.querySelector('.tab-name').textContent = modified ? `● ${filename}` : filename;
  }

  // ── Exercise file tabs ────────────────────────────────────────────

  _closeExerciseTab(tabId) {
    const idx = this.fileEditors.findIndex(e => e.tabId === tabId);
    if (idx === -1) return;
    const { editor, element, tabBtn, spec, loadedContent } = this.fileEditors[idx];

    if (editor.getValue() !== loadedContent) {
      if (!confirm(`Close ${spec.label}?\nUnsaved changes will be lost.`)) return;
    }

    editor.toTextArea();
    element.remove();
    tabBtn.remove();
    this.fileEditors.splice(idx, 1);

    if (this.fileEditors.length > 0) {
      const next = this.fileEditors[Math.min(idx, this.fileEditors.length - 1)];
      this._switchEditorTab(next.tabId);
    } else if (this._deviceFileEditors.length > 0) {
      this._switchEditorTab(this._deviceFileEditors[0].tabId);
    } else {
      this._switchEditorTab('settings');
    }
  }

  // ── Solution tabs ─────────────────────────────────────────────────

  _openSolutionTab(entry) {
    const label = this.fileEditors.length > 1
      ? entry.spec.label.replace(/\.py$/, '') + '_solution.py'
      : 'solution.py';

    // If already open, just switch to it.
    const existing = this._solutionTabs.find(t => t.label === label);
    if (existing) {
      this._switchEditorTab(existing.tabId);
      return;
    }

    const tabId    = `solution-${this._nextDeviceTabId++}`;
    const tabBar   = document.getElementById('editor-tabs');
    const insertRef = document.getElementById('editor-tabs-end');

    const tab = document.createElement('button');
    tab.className = 'editor-tab editor-tab-solution';
    tab.dataset.editorTab = tabId;
    tab.addEventListener('click', () => this._switchEditorTab(tabId));

    const nameSpan = document.createElement('span');
    nameSpan.className = 'tab-name';
    nameSpan.textContent = label;
    tab.appendChild(nameSpan);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'tab-close-btn';
    closeBtn.title = 'Close tab';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', e => { e.stopPropagation(); this._closeSolutionTab(tabId); });
    tab.appendChild(closeBtn);

    tabBar.insertBefore(tab, insertRef);

    const pane = document.createElement('div');
    pane.id = `editor-tab-${tabId}`;
    pane.className = 'editor-tab-content';

    const toolbar = document.createElement('div');
    toolbar.className = 'editor-file-toolbar';

    const pathSpan = document.createElement('span');
    pathSpan.className = 'dim';
    pathSpan.textContent = label;
    toolbar.appendChild(pathSpan);

    const roSpan = document.createElement('span');
    roSpan.className = 'device-file-status';
    roSpan.textContent = 'read-only';
    toolbar.appendChild(roSpan);

    pane.appendChild(toolbar);

    const textarea = document.createElement('textarea');
    pane.appendChild(textarea);

    document.getElementById('editor-tab-settings').parentNode
      .insertBefore(pane, document.getElementById('editor-tab-settings'));

    const editor = CodeMirror.fromTextArea(textarea, {
      mode: 'python',
      theme: this._theme === 'dark' ? 'material-darker' : 'default',
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      readOnly: true,
      lineWrapping: false,
      autofocus: false,
    });
    editor.setSize('100%', '100%');
    editor.setValue(entry.solutionCode);
    this._addWhitespaceOverlay(editor);

    const solutionEntry = { tabId, label, editor, element: pane, tabBtn: tab };
    this._solutionTabs.push(solutionEntry);

    this._switchEditorTab(tabId);
  }

  _closeSolutionTab(tabId) {
    const idx = this._solutionTabs.findIndex(t => t.tabId === tabId);
    if (idx === -1) return;
    const { editor, element, tabBtn } = this._solutionTabs[idx];

    editor.toTextArea();
    element.remove();
    tabBtn.remove();
    this._solutionTabs.splice(idx, 1);

    if (this.fileEditors.length > 0) {
      this._switchEditorTab(this.fileEditors[0].tabId);
    } else if (this._deviceFileEditors.length > 0) {
      this._switchEditorTab(this._deviceFileEditors[0].tabId);
    } else {
      this._switchEditorTab('settings');
    }
  }

  async _saveExerciseFile(tabId) {
    const entry = this.fileEditors.find(e => e.tabId === tabId);
    if (!entry || !this.repl.connected) return;

    const statusSpan = entry.element.querySelector('.device-file-status');
    const saveBtn    = entry.element.querySelector('.btn');
    saveBtn.disabled = true;
    statusSpan.textContent = 'Saving…';

    try {
      await this.repl.writeFile(entry.spec.device_path, entry.editor.getValue());
      entry.loadedContent = entry.editor.getValue();
      this._updateExerciseTabLabel(entry);
      statusSpan.textContent = 'Saved';
      setTimeout(() => { statusSpan.textContent = ''; }, 2000);
    } catch (e) {
      statusSpan.textContent = `Error: ${e.message}`;
    } finally {
      saveBtn.disabled = false;
    }
  }

  _updateExerciseTabLabel(entry) {
    const modified = entry.editor.getValue() !== entry.loadedContent;
    entry.tabBtn.querySelector('.tab-name').textContent =
      modified ? `● ${entry.spec.label}` : entry.spec.label;
  }

  _modeForPath(path) {
    const ext = path.split('.').pop().toLowerCase();
    if (ext === 'py')   return 'python';
    if (ext === 'json') return { name: 'javascript', json: true };
    return null;
  }

  // ── Theme ─────────────────────────────────────────────────────────

  _applyTheme(theme) {
    this._theme = theme;
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('clb-theme', theme);
    document.getElementById('btn-theme').textContent = theme === 'dark' ? '☀' : '☾';

    const cmTheme = theme === 'dark' ? 'material-darker' : 'default';
    this.fileEditors.forEach(({ editor }) => editor.setOption('theme', cmTheme));
    this._deviceFileEditors.forEach(({ editor }) => editor.setOption('theme', cmTheme));
    this._solutionTabs.forEach(({ editor }) => editor.setOption('theme', cmTheme));
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
    const firmware = document.getElementById('btn-install-firmware');

    const hasSerial = 'serial' in navigator;
    badge.textContent = connected ? 'Connected' : hasSerial ? 'Disconnected' : 'Use Chrome or Edge';
    badge.className = `status-badge ${connected ? 'status-connected' : 'status-disconnected'}`;
    btn.textContent = connected ? 'Disconnect' : hasSerial ? 'Connect Device' : 'Serial not supported';
    btn.disabled = !hasSerial && !connected;
    input.disabled = !connected;
    firmware.disabled = !connected;

    document.getElementById('btn-browse-files').disabled = !connected;
    document.getElementById('btn-settings-save').disabled = !connected;
    document.getElementById('btn-settings-reload').disabled = !connected;
    this.fileEditors.forEach(entry => {
      const saveBtn = entry.element?.querySelector('.btn');
      if (saveBtn) saveBtn.disabled = !connected;
    });

    if (!connected) {
      this._closeFileBrowser();
      this._settingsLoaded = false;
      this.settingsEditor.setValue('// Connect a device to load settings.json');
      document.getElementById('settings-status').textContent = '';
    }

    this._updateRunControls();
  }

  _updateRunControls() {
    const connected = this.repl.connected;
    const hasFiles = this.currentExercise && this.currentExercise.files.length > 0;
    document.getElementById('btn-save').disabled = !connected;
    document.getElementById('btn-run').disabled = !connected || !hasFiles;
    document.getElementById('btn-stop').disabled = !connected;
    document.getElementById('btn-restart').disabled = !connected;
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
    const prev  = document.getElementById('btn-page-prev');
    const next  = document.getElementById('btn-page-next');
    const indicator = document.getElementById('page-indicator');

    nav.classList.remove('hidden');

    const multiPage  = total > 1;
    const isLastPage = index === total - 1;
    const nextExId   = this._getNextExerciseId();

    prev.classList.toggle('hidden', !multiPage);
    indicator.classList.toggle('hidden', !multiPage);

    if (multiPage) {
      indicator.textContent = `${index + 1} / ${total}`;
      prev.disabled = index === 0;
    }

    if (isLastPage && nextExId) {
      next.classList.remove('hidden');
      next.disabled = false;
      next.textContent = 'Next Exercise →';
      next.dataset.nextExercise = nextExId;
    } else {
      next.classList.toggle('hidden', !multiPage);
      next.textContent = 'Next →';
      next.disabled = isLastPage;
      delete next.dataset.nextExercise;
    }

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
    const content = document.getElementById('description-content');
    content.innerHTML = scratch.innerHTML;
    content.querySelectorAll('img').forEach(img => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => this._showImageViewer(img.src));
    });
  }

  _showImageViewer(src) {
    if (this._fileBrowserOpen) {
      this._fileBrowserOpen = false;
      document.getElementById('file-browser').classList.remove('active');
    }
    this._imageViewerOpen = true;
    const filename = src.split('/').pop().split('?')[0];
    document.getElementById('image-viewer-title').textContent = filename;
    document.getElementById('image-viewer-img').src = src;
    document.getElementById('image-viewer-img').alt = filename;
    document.querySelectorAll('.editor-tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.editor-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('image-viewer').classList.add('active');
  }

  _closeImageViewer() {
    if (!this._imageViewerOpen) return;
    this._imageViewerOpen = false;
    document.getElementById('image-viewer').classList.remove('active');
    document.getElementById('image-viewer-img').src = '';
    if (this._activeEditorTab) {
      this._switchEditorTab(this._activeEditorTab);
    } else {
      document.getElementById('editor-no-exercise').classList.add('active');
    }
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
        ph.innerHTML = `
          <div class="hints-intro">
            <h3>AI Tutor</h3>
            <p>Each exercise has a built-in AI tutor that can answer questions and give
            hints as you work through it. The tutor won't give you the answer directly —
            it uses a Socratic approach, asking questions and nudging you toward the
            solution so that you do the thinking.</p>
            <h4>How to use it</h4>
            <ul>
              <li>Ask what a concept means or how something works</li>
              <li>Describe what you tried and what happened — the more specific, the better</li>
              <li>Ask for a hint when you're stuck</li>
            </ul>
            <h4>How hints work</h4>
            <p>Each exercise has an ordered hint ladder from vague to specific. The tutor
            gives one level at a time — ask again to go deeper. The final hints point
            directly at the answer, so try to get there with fewer hints.</p>
            <p class="hints-intro-action">To get started, click <strong>⚙</strong> above
            and configure an AI provider (Google Gemini, Groq, or a local Ollama server).</p>
          </div>`;
      } else if (!this.currentExercise?.tutor) {
        ph.innerHTML = `
          <div class="hints-intro">
            <h3>AI Tutor ready</h3>
            <p>Select an exercise from the dropdown above and the tutor will load its
            knowledge of that exercise — the learning objective, what you need to discover
            yourself, and the hint ladder for when you're stuck.</p>
          </div>`;
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
      const system = this.currentExercise.tutor;
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

  // ── Home navigation ───────────────────────────────────────────────

  _goHome() {
    document.getElementById('exercise-select').value = '';
    this.currentExercise = null;
    this._pages = [];
    this._pageIndex = 0;

    document.getElementById('description-content').innerHTML = this._homeDescriptionHTML;
    document.getElementById('description-nav').classList.add('hidden');

    this._clearFileEditors();
    document.querySelectorAll('.editor-tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.editor-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('editor-no-exercise').classList.add('active');

    this._hintMessages = [];
    document.getElementById('hints-messages').innerHTML = '';
    this._updateHintsReadyState();
    document.getElementById('btn-show-solution').disabled = true;
    this._updateRunControls();
  }

  // ── Exercise navigation ───────────────────────────────────────────

  _getNextExerciseId() {
    if (!this.currentExercise) return null;
    const sel = document.getElementById('exercise-select');
    const options = [...sel.options].filter(o => o.value);
    const idx = options.findIndex(o => o.value === this.currentExercise.meta.id);
    return idx >= 0 && idx < options.length - 1 ? options[idx + 1].value : null;
  }

  async _navigateToExercise(id) {
    document.getElementById('exercise-select').value = id;
    await this._onExerciseSelected(id);
  }

  // ── Whitespace overlay ────────────────────────────────────────────

  _addWhitespaceOverlay(editor) {
    editor.addOverlay({
      token(stream) {
        const ch = stream.peek();
        if (ch === ' ')  { stream.next(); return 'ws-space'; }
        if (ch === '\t') { stream.next(); return 'ws-tab'; }
        while (stream.next() != null && stream.peek() !== ' ' && stream.peek() !== '\t') {}
        return null;
      }
    });
  }
}
