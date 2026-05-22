import time
import robot

GAME_S      = 30    # game duration in seconds
DODGE_MM    = 250   # dodge when opponent is closer than this
DODGE_ANGLE = 40    # degrees to turn sideways
DODGE_STEP  = 150   # mm to travel while turned

robot.init()

# Countdown: 3 yellow flashes
for _ in range(3):
    robot.colour(robot.YELLOW)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

start = time.time()
robot.colour(robot.GREEN)

while time.time() - start < GAME_S:
    mm = robot.distance()

    if mm > 0 and mm < DODGE_MM:
        # TODO: dodge sideways past the opponent
        pass
    else:
        # TODO: advance toward the opponent
        pass

robot.colour(robot.BLACK)
