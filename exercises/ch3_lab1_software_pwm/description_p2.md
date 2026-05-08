# Lab 1: The Limits of Software PWM

The skeleton in the editor has the LED and the constants ready. Fill in the three missing calculations and the two lines inside the loop.

---

## Experiment: duty cycle

Once it's running, try different `DUTY` values and observe the LED brightness:

| DUTY | Effect |
|------|--------|
| 10 | Very dim |
| 50 | Half brightness |
| 90 | Nearly full |
| 100 | Full on (no switching) |

---

## Experiment: frequency

Try changing `FREQ`:

- **10 Hz** — you can see the LED flicker. Each cycle takes 100 ms, visible to the eye.
- **50 Hz** — flicker just disappears (the threshold for mains lighting).
- **100 Hz** — smooth. Still feels slightly different to a constant light.
- **1000 Hz** — completely smooth. Now try `DUTY = 5` — very dim but stable.

---

## The problem with software PWM

At 1000 Hz and 50% duty, `on_time` and `off_time` are each 0.5 ms. The CPU must wake up every 0.5 ms and toggle the pin — that is 2000 context switches per second. The processor is doing almost nothing else.

Try adding `print('hello')` inside the loop. At 1000 Hz the output is garbled because the print takes longer than the sleep interval.

Software PWM also has **jitter**: the OS scheduler and other interrupts cause the sleep times to be slightly uneven, so the duty cycle drifts.

In Lab 2 you will see how the Pico's hardware PWM solves both problems — the hardware generates the waveform with no CPU involvement at all.
