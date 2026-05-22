EXERCISE = {
    "id": "ch3_lab1_reading_distance",
    "title": "Reading Distance",
    "concept": "HC-SR04 ultrasonic distance sensing and the voltage divider requirement",

    "objective": (
        "Wire the HC-SR04 with a voltage divider on the ECHO pin, call robot.distance() "
        "in a loop, print the readings to the console, and understand the meaning of a "
        "-1 return value."
    ),

    "off_limits": [
        "the exact resistor values before the student has identified that a 2:1 ratio is needed",
        "the complete loop solution before the student has attempted to write it",
    ],

    "hints": [
        "robot.distance() sends a 10 µs trigger pulse, waits for the echo pin to go "
        "high then low, and returns the distance in mm. It returns -1 if no echo is "
        "received within 60 ms.",

        "The HC-SR04 ECHO pin outputs 5 V. The Pico GPIO input is rated for 3.3 V maximum. "
        "A voltage divider with a 2:1 resistor ratio (e.g. 1 kΩ and 2 kΩ) reduces 5 V to "
        "about 3.3 V.",

        "TRIGGER_PIN and ECHO_PIN in config.py must match the GPIO pins you have wired. "
        "Check them before assuming the sensor is broken.",

        "A reading of -1 almost always means no echo was received. This can happen because "
        "nothing is in range, the ECHO wiring is wrong, or the voltage divider is missing.",
    ],

    "success_indicators": [
        "readings appear in the console and change when an object is moved in front of the sensor",
        "readings are stable (±10 mm) when the hand is held still",
        "-1 is returned when nothing is in range",
        "student can explain why the ECHO pin needs a voltage divider",
    ],

    "observation_checklist": [
        "Is ECHO connected through a voltage divider, not directly to the Pico?",
        "Is TRIG_PIN in config.py set to the correct GPIO pin?",
        "Is ECHO_PIN in config.py set to the correct GPIO pin?",
        "Is VCC on the HC-SR04 connected to VBUS (5 V), not 3V3?",
        "Does the sensor return anything other than -1?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 1: Reading Distance. The key learning points are
the HC-SR04 wiring (especially the voltage divider on ECHO) and interpreting the
return value of robot.distance().

YOUR ROLE
- Explain the ultrasonic ranging principle (timing a reflected sound pulse).
- Guide the student to work out the voltage divider ratio themselves — ask what
  ratio reduces 5 V to 3.3 V before giving the values.
- Help the student interpret -1 as "no echo" not "distance zero".
- Do NOT reveal the resistor values before the student has identified the ratio.

COMMON PROBLEMS

Always returns -1: most likely the ECHO wiring is wrong or the voltage divider
is missing. A direct connection may appear to work briefly but risks Pico damage.

Readings are erratic: the ECHO pin is connected directly without a divider.
The 5 V signal is exceeding the GPIO input rating.

Config pin numbers wrong: ask the student to check TRIGGER_PIN and ECHO_PIN in
config.py match their physical wiring.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
