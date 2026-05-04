# Step 1 — Install MicroPython

Follow these steps to put MicroPython on a bare Pico for the first time. If MicroPython is already installed, skip to the next page.

---

## 1. Download the MicroPython firmware

Go to the official MicroPython downloads page and grab the correct file for your board:

- **Raspberry Pi Pico** — [micropython.org/download/rp2-pico](https://micropython.org/download/rp2-pico/)
- **Raspberry Pi Pico W** (with wireless) — [micropython.org/download/rp2-pico-w](https://micropython.org/download/rp2-pico-w/)

Download the latest stable release. The file will have a `.uf2` extension.

> **Pico or Pico W?** Look at the top of the board. If it has a silver radio module (a small metal rectangle) next to the USB port, it is a Pico W.

---

## 2. Put the Pico into bootloader mode

1. **Hold down the BOOTSEL button** on the Pico — it is the small white button on the top of the board
2. **While holding BOOTSEL**, plug the USB cable into your computer
3. **Release BOOTSEL** once the cable is connected

The Pico will appear as a USB drive named **RPI-RP2**. If it does not appear, unplug, wait a few seconds, and try again.

---

## 3. Copy the firmware

Drag and drop the `.uf2` file you downloaded onto the **RPI-RP2** drive, exactly as you would copy a file to a USB stick.

The Pico will automatically reboot as soon as the copy finishes. The RPI-RP2 drive will disappear — that is expected. The Pico is now running MicroPython.

---

## Confirm it worked

Plug the Pico back in (if it disconnected) and click **Connect Device** at the top of this page. Select the serial port when prompted. You should see a `>>>` prompt appear in the console panel — that is the MicroPython REPL confirming the installation was successful.

Once you see `>>>`, move on to the next page.
