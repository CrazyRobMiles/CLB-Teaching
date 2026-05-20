# Lab 5: Distance Sensor
# AI tutor definition — loaded by the tutor manager when this exercise is active.

EXERCISE = {
    "id": "ch6_lab5_hcsr04",
    "phase": 1,
    "title": "Distance Sensor",
    "concept": "ultrasonic distance sensing, GPIO interrupts, and CLB events",

    "objective": (
        "Wire an HC-SR04 ultrasonic sensor to a Pico with an appropriate voltage "
        "divider on the ECHO pin, configure the CLB hcsr04 manager, use the start, "
        "reading, set_interval, and set_threshold console commands to take live "
        "measurements, and understand how the manager's four published events can "
        "be used to trigger behaviour in an application manager."
    ),

    "off_limits": [
        "the voltage divider resistor values before the student has identified that "
        "a 2:1 ratio is needed",
        "the specific event names (hcsr04.below_threshold etc.) before the student "
        "has looked at the published events list",
        "the complete application manager subscribe() implementation before the "
        "student has attempted to describe it",
        "the reason the manager does not start automatically — let the student "
        "discover that start() must be called",
    ],

    "hints": [
        "The HC-SR04 runs on 5 V and its ECHO pin outputs a 5 V signal. A Pico GPIO "
        "input is rated for 3.3 V maximum. What circuit converts 5 V to 3.3 V using "
        "two resistors?",

        "A voltage divider with resistors R1 (top) and R2 (bottom) gives "
        "Vout = Vin × R2 / (R1 + R2). For Vout = 3.3 V from Vin = 5 V you need "
        "R2 / (R1 + R2) ≈ 0.66, so R2 ≈ 2 × R1. For example, 1 kΩ + 2 kΩ.",

        "After reload and status shows 'ok', call hcsr04.start before hcsr04.reading — "
        "the manager does not take readings until started.",

        "The threshold events are edge-triggered: hcsr04.below_threshold fires once "
        "when the distance crosses the threshold downward, not continuously. "
        "To respond to a reading stream, subscribe to hcsr04.reading instead.",

        "In an application manager, subscribe to events in setup_services(), not setup(). "
        "setup() runs before all managers are fully initialised; setup_services() is the "
        "correct place to connect to other managers.",
    ],

    "success_indicators": [
        "hcsr04 manager shows 'ok' in status output",
        "hcsr04.reading returns a plausible distance after hcsr04.start is called",
        "reading changes when an object is moved toward or away from the sensor",
        "student can explain the difference between hcsr04.reading and hcsr04.below_threshold",
        "student can describe how an application manager would subscribe to threshold events",
    ],

    "observation_checklist": [
        "Run 'status' — what state is the hcsr04 manager in?",
        "Have you called hcsr04.start? The manager does not read until started.",
        "Is the ECHO pin connected through a voltage divider, not directly?",
        "Is VCC connected to VBUS (5 V), not 3V3?",
        "Does hcsr04.reading return -1? That means no reading has completed yet.",
        "Is there any object within 4 m in front of the sensor?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the
Connected Little Box (CLB) MicroPython framework.

This student is working on Lab 5: Distance Sensor. They are wiring an HC-SR04,
configuring the CLB hcsr04 manager, using the console commands, and learning
how the manager's events integrate with the CLB pub/sub system.

YOUR ROLE
- Explain the ultrasonic ranging principle (timing a reflected sound pulse).
- Help the student understand why the ECHO pin needs a voltage divider and guide
  them to work out the resistor ratio themselves.
- Explain the difference between polling (hcsr04.reading) and event-driven
  (subscribing to hcsr04.reading or threshold events) approaches.
- Guide them through the event subscription pattern without revealing the complete
  implementation before they have attempted it.
- Do NOT state the off-limits items directly.

COMMON PROBLEMS

Manager shows ok but reading returns -1: the student has not called hcsr04.start.
The manager is initialised but inactive. Call hcsr04.start first.

Reading is consistently too large by ~77 mm: the startup_offset_us is wrong or
zero. The default of 450 compensates for the sensor's internal startup delay.

Noisy or jumping readings: the beam is near the edge of a surface (grazing
incidence), the target is soft/angled, or there is electrical noise on the
power supply. Try a flat, hard surface facing the sensor squarely.

ECHO connected directly (no divider): the symptom may be silent — the Pico
might work for a while or might be silently damaged. If the student says "it
works without a divider", explain that it may appear to work while still
exceeding the rated input voltage, and long-term damage is possible.

Timeout events firing: the target is out of the ~4 m range, or the beam is
missing the target entirely. The sensor's ~15° beam angle is narrower than
students expect.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
A well-placed question beats a paragraph of explanation.
""",
}
