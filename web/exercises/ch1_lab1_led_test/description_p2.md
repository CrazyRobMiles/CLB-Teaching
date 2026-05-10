# Lab 1: Building the Circuit

## Why a resistor?

The Pico's 3.3 V supply can push more current through an LED than it can safely handle. A 220 Ω resistor limits the current to about 15 mA — enough to make the LED bright without burning it out.

The formula is: **R = V / I** → 3.3 V ÷ 0.015 A ≈ 220 Ω

---

## Circuit

```
Pico pin 36 (3V3) ── resistor ── LED anode (+) ── LED cathode (−) ── Pico pin 38 (GND)
```

| Pico pin | Label | Purpose |
|----------|-------|---------|
| 36 | 3V3(OUT) | 3.3 V supply |
| 38 | GND | Ground |

---

## Step by step

1. Place the Pico on the breadboard so it straddles the centre gap.
2. Insert the 220 Ω resistor. One leg goes into the same row as Pico physical pin 36 (3V3); the other leg goes into a free row nearby.
3. Insert the LED. Anode (long leg) into the free row from step 2; cathode (short leg) into another free row.
4. Add a jumper wire from the LED cathode row to the GND rail.
5. Add a jumper wire from the GND rail to Pico physical pin 38 (GND).

![Completed circuit](images/lab1_circuit.jpg)

*Photo: A Pico on a breadboard. A 220 Ω resistor runs from the 3V3 pin row to an intermediate row; an LED anode connects to that row and the cathode connects via a wire to GND.*

---

## Test it

Plug the USB cable into the Pico and your computer. **The LED should light up immediately** — no code needed.

### If it doesn't light up

- Check the LED is the right way around (longer leg toward the resistor / 3V3 side).
- Check each breadboard connection — both legs of every component must be fully pushed in.
- Swap the LED for another one (LEDs can be dead).
- Try a different resistor value (470 Ω is also fine — the LED will be dimmer but should still glow).

Once the LED lights up, you've confirmed the hardware works. Move on to Lab 2 to take control of it with code.
