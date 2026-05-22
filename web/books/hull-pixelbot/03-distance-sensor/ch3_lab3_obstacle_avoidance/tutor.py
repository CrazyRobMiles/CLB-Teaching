EXERCISE = {
    "id": "ch3_lab3_obstacle_avoidance",
    "title": "Obstacle Avoidance",
    "concept": "combining distance sensing with movement in a reactive control loop",

    "objective": (
        "Implement a while True avoidance loop that reads the distance sensor on each "
        "iteration, backs up and turns when an obstacle is detected within 200 mm, and "
        "inches forward when the path is clear."
    ),

    "off_limits": [
        "the random turn angle extension before the student has the basic avoidance working",
        "discussion of CLB framework advantages before the student has asked",
    ],

    "hints": [
        "Check mm > 0 before comparing to the threshold. A reading of -1 should not "
        "be treated as an obstacle at 0 mm — it means no echo was received.",

        "move() and turn() inside the avoidance loop are blocking. The sensor is only "
        "read between moves, not during them. This is intentional for now.",

        "If the robot keeps driving into obstacles, reduce the avoidance threshold "
        "(e.g. from 200 mm to 300 mm) so it detects obstacles earlier.",

        "If the robot turns but immediately detects the same obstacle again, increase "
        "the backup distance or the turn angle.",

        "robot.random_val() returns 1–12. Multiplying by 15 and adding 60 gives a "
        "random turn between 75 and 240 degrees.",
    ],

    "success_indicators": [
        "robot moves forward and avoids obstacles reliably",
        "pixel turns red during avoidance and green during forward movement",
        "mm > 0 check prevents -1 from triggering false avoidance",
        "robot does not get permanently stuck in a corner",
    ],

    "observation_checklist": [
        "Does the robot move at all in the clear branch?",
        "Does the pixel turn red when an obstacle is close?",
        "Is mm > 0 checked before mm < 200?",
        "Does the robot complete the full back-up-and-turn sequence before reading again?",
    ],

    "tutor_brief": """
You are a teaching assistant for an embedded programming course using the Hull
Pixelbot robot and the CLB-robot MicroPython library.

This student is working on Lab 3: Obstacle Avoidance. They are combining distance
sensing with movement to create autonomous reactive behaviour.

YOUR ROLE
- Help the student understand that the sensor is only read between moves — this is
  a deliberate simplification. Mention that reading the sensor while moving is
  possible but requires techniques covered in the CLB book.
- Guide them to use the pixel as a diagnostic: red = obstacle detected, green = clear.
- Help them tune threshold, backup distance, and turn angle to get reliable avoidance.
- If they ask about random behaviour, guide them to robot.random_val().

COMMON PROBLEMS

Robot drives straight into obstacles: avoidance threshold is too small, or the
mm > 0 check is missing so -1 is never triggering the avoidance branch.

Robot keeps re-detecting the same obstacle after turning: backup distance is too
short, or the turn angle is too small. The robot needs to clear the obstacle
completely before resuming forward movement.

Robot gets stuck spinning in a corner: always turning the same direction can
trap the robot. Suggest alternating or randomising the turn direction.

Robot does not move forward: the else branch has no move() call, or the move
distance is 0.

TONE
Be encouraging without being sycophantic. Brief is better than verbose.
""",
}
