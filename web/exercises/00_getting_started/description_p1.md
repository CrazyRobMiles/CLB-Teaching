# Exercise 00: Getting Started

## What This Exercise Covers

This exercise gets your device ready to run CLB programs. By the end you will have:

- MicroPython installed on your Raspberry Pi Pico
- The CLB framework installed on the device
- A simple test program running and printing output to the console

There is no circuit to build and no code to write. This is purely setup.

---

## What is the Connected Little Box Framework?

The CLB is a MicroPython framework for building small connected devices. Every capability of the device — WiFi, sensors, displays, application logic — is implemented as a self-contained **manager** class. Managers are loaded at boot, configured from a JSON settings file, and updated in a cooperative loop.

You will learn how all of this works in the exercises that follow. For now, the goal is simply to get the framework running.

---

## What You Need

### Hardware

- A Raspberry Pi Pico or Pico W (other RP2040 boards also work)
- A USB cable (micro-USB for Pico, USB-C for Pico W revision 2)
- A computer with a USB port

### Software

- **Chrome or Edge** browser — the Web Serial API used by this page is not available in Firefox or Safari
- No other software installation is required

---

## Steps Overview

| Step | What you will do |
|------|-----------------|
| 1 | Install MicroPython on the Pico |
| 2 | Install the CLB framework via this page |
| 3 | Run the test program and confirm everything works |

If your Pico already has MicroPython installed, skip ahead to **Step 2** on the next page.

> **Not sure if MicroPython is installed?** Plug in your Pico and click **Connect Device** at the top of this page. If the console shows a `>>>` prompt, MicroPython is present and you can go straight to Step 2.
