/**
 * FirmwareInstaller
 *
 * Fetches the pinned CLB release from GitHub and writes every file to the
 * device via the REPL layer.  Calls onProgress(pct, label) during install.
 *
 * GitHub rate limits unauthenticated API calls to 60/hour.  For classroom
 * use, consider serving firmware files directly from this repo (add as a
 * git subtree or copy on release bump) to avoid the limit.
 */

const FIRMWARE_CONFIG_URL = 'firmware.json';

export class FirmwareInstaller {
  constructor(repl) {
    this.repl = repl;
    this.config = null;
  }

  async loadConfig() {
    if (this.config) return this.config;
    const res = await fetch(FIRMWARE_CONFIG_URL);
    this.config = await res.json();
    return this.config;
  }

  /**
   * Fetch the list of firmware files for the pinned version.
   * In the Electron desktop app, window.electronFirmware is set by the
   * electron-bridge and points to the locally bundled snapshot so the
   * install works with no network access.  Otherwise falls back to GitHub.
   * Returns [{ devicePath, rawUrl }]
   */
  async fetchFileList() {
    const cfg = await this.loadConfig();

    // Electron offline path — use bundled firmware snapshot
    if (window.electronFirmware) {
      const { manifest, fileBase } = window.electronFirmware;
      const res = await fetch(manifest);
      if (!res.ok) throw new Error(`Local firmware manifest error: ${res.status}`);
      const data = await res.json();
      return data.tree
        .filter(item => item.type === 'blob' && item.path.startsWith(cfg.firmware_path + '/'))
        .filter(item => !cfg.exclude.some(ex => item.path.endsWith(ex)))
        .map(item => ({
          devicePath: '/' + item.path.slice(cfg.firmware_path.length + 1),
          rawUrl: `${fileBase}/${item.path.slice(cfg.firmware_path.length + 1)}`,
        }));
    }

    // Browser / online path — fetch from GitHub API
    const url = `https://api.github.com/repos/${cfg.repo}/git/trees/${cfg.version}?recursive=1`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);
    const data = await res.json();

    return data.tree
      .filter(item => item.type === 'blob' && item.path.startsWith(cfg.firmware_path + '/'))
      .filter(item => !cfg.exclude.some(ex => item.path.endsWith(ex)))
      .map(item => ({
        devicePath: '/' + item.path.slice(cfg.firmware_path.length + 1),
        rawUrl: `https://raw.githubusercontent.com/${cfg.repo}/${cfg.version}/${item.path}`,
      }));
  }

  /**
   * Install all firmware files onto the device.
   * onProgress(percent, label) is called throughout.
   */
  async install(onProgress = () => {}) {
    onProgress(0, 'Fetching file list…');
    const files = await this.fetchFileList();

    // Download all files from GitHub in parallel while device setup runs.
    onProgress(5, 'Downloading firmware files…');
    const fetched = await Promise.all(
      files.map(async ({ devicePath, rawUrl }) => {
        const res = await fetch(rawUrl);
        if (!res.ok) throw new Error(`Failed to fetch ${rawUrl}: ${res.status}`);
        return { devicePath, content: await res.text() };
      })
    );

    // Ensure required directories exist on the device.
    await this._ensureDirs(files.map(f => f.devicePath));

    for (let i = 0; i < fetched.length; i++) {
      const { devicePath, content } = fetched[i];
      const pct = Math.round(10 + (i / fetched.length) * 88);
      onProgress(pct, `Writing ${devicePath}`);
      await this.repl.writeFile(devicePath, content);
    }

    // Write a minimal settings.json so the device boots normally after install
    // without entering wait_for_settings mode.  Exercise selection overwrites this.
    await this.repl.writeFile('/settings.json', '{}');

    onProgress(100, 'Firmware installed');
  }

  async _ensureDirs(paths) {
    const dirs = new Set(
      paths
        .map(p => p.split('/').slice(0, -1).join('/'))
        .filter(d => d && d !== '/')
    );
    for (const dir of dirs) {
      await this.repl.execute(
        `import os\ntry:\n os.mkdir('${dir}')\nexcept OSError:\n pass`
      );
    }
  }
}
