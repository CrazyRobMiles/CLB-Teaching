import time
import robot

robot.init()

# Stalker: the robot tries to maintain 200 mm distance from an object.
# Green = moving forward to close the gap
# Blue  = holding distance
# Red   = backing away because object is too close

TARGET_MM    = 200
TOLERANCE_MM = 40
STEP_MM      = 30

robot.colour(robot.BLUE)

while True:
    mm = robot.distance()

    if mm < 0:
        robot.colour(robot.WHITE)   # no reading — stay still
    elif mm < TARGET_MM - TOLERANCE_MM:
        robot.colour(robot.RED)
        robot.move(-STEP_MM)
    elif mm > TARGET_MM + TOLERANCE_MM:
        robot.colour(robot.GREEN)
        robot.move(STEP_MM)
    else:
        robot.colour(robot.BLUE)    # within tolerance — do nothing
