# Lab 2: I2C Introduction

**I2C** (Inter-Integrated Circuit, pronounced "I-squared-C") is a serial communication protocol for connecting microcontrollers to peripheral chips — sensors, displays, motor drivers, ADCs, and more. It requires only two wires regardless of how many devices are connected.

---

## The two wires

| Wire | Abbreviation | Purpose |
|------|-------------|---------|
| Serial Data | SDA | Carries data bits |
| Serial Clock | SCL | Paces the transfer |

Both lines are **open-drain** — devices pull them LOW to signal, and pull-up resistors (typically 4.7 kΩ) hold them HIGH when the bus is idle. Most breakout boards include the pull-ups.

---

## Addresses

Every I2C device has a **7-bit address** (0–127). The master (the Pico) sends the address at the start of every transfer, and only the device with that address responds. This is what allows many devices to share the same two wires.

Addresses are usually configured by the manufacturer and printed in the datasheet. Some devices have one or two address pins you can connect to GND or 3.3 V to choose between a small set of addresses — useful when you need two identical chips on the same bus.

Common devices and their default addresses:

| Device | Default address |
|--------|----------------|
| PCA9685 PWM driver | 0x40 |
| SSD1306 OLED display | 0x3C |
| BMP280 pressure sensor | 0x76 |
| MPU6050 accelerometer | 0x68 |

---

## Registers

Inside each I2C device, configuration and data are stored in **registers** — numbered memory locations. A write transaction sends: address → register number → value. A read transaction sends: address → register number, then reads back bytes.

You never need to implement the I2C protocol yourself: the Pico's hardware handles the signalling, and MicroPython's `machine.I2C` provides a clean API.
