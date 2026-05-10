# Step 2 — Install the CLB Framework

With MicroPython running on the Pico, the next step is to install the CLB framework files. This page does it for you automatically over the USB connection.

---

## 1. Connect the device

If you are not already connected, click **Connect Device** in the top bar. Your browser will show a list of available serial ports — select the one corresponding to your Pico (it is usually labelled **USB Serial Device** or similar).

Once connected, the status badge in the top bar changes to **Connected** and the console panel shows the MicroPython `>>>` prompt.

---

## 2. Install the firmware

Click **Install Firmware** in the top bar.

You will be asked to confirm. Click OK.

A progress bar appears while the installer:

1. Fetches the pinned CLB release from GitHub
2. Writes each framework file to the device over the serial connection
3. Writes `settings.json` and `app_manifest.py`
4. Reboots the device

This takes around 30–60 seconds depending on your connection speed. Do not unplug the device while the progress bar is running.

---

## 3. Wait for the reboot

When installation finishes the device reboots automatically. The console panel will show boot output from the CLB framework — something like:

```
CLB v1.x.x booting...
Loading managers...
All managers ready.
```

The exact output depends on the CLB version. As long as you see boot messages and no `Traceback` errors, the installation was successful.

---

## If something goes wrong

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Progress bar stalls for more than 2 minutes | Serial connection dropped | Disconnect, reconnect, try again |
| `Traceback` in console after reboot | Partial install | Run Install Firmware again |
| Device does not appear in port list | Driver issue | Try a different USB port or cable |

Once the device has booted cleanly, move on to the next page to run your first program.
