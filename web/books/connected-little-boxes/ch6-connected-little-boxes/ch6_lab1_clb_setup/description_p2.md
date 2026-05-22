# Step 2 — Run Your First CLB Program

The CLB framework is now installed. This page walks you through running a simple test program to confirm everything is working end to end.

---

## What the test program does

The editor on this page has already loaded `App_hello_clb.py` — a minimal CLB manager that:

- Prints a confirmation message when it starts
- Reports its state as `STATE_OK` to the framework
- Prints a heartbeat message every 5 seconds so you can see it is still running

It requires no external hardware — just the Pico and a USB connection.

---

## Run it

1. Make sure you are still connected (the status badge should show **Connected**)
2. Click **Run** in the top bar

The page writes the program to the device and triggers a soft reboot. Watch the console panel.

---

## What to look for

Within a few seconds you should see output like this:

```
CLB framework is running!
Type 'status' to see all manager states.
```

Then every 5 seconds:

```
CLB is alive!
```

If you see these messages, everything is working correctly.

---

## Check manager status

Type `status` into the console input at the bottom of the console panel and press Enter. The CLB framework will list all active managers and their states. You should see:

```
hello_clb: STATE_OK
```

`STATE_OK` means the manager initialised successfully and is running normally. Any other state (like `STATE_ERROR` or `STATE_DISABLED`) indicates a problem — check the console for error messages.

---

## You are ready

The framework is installed, the test program runs, and you understand the basic edit–save–run cycle. Move on to **Button Light** to start building CLB applications with real hardware.
