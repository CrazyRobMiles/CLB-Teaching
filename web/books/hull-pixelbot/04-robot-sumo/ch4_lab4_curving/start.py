import time
import robot

GAME_S     = 30    # game duration in seconds
ARC_RADIUS = 300   # mm — larger = gentler curve
ARC_ANGLE  = 40    # degrees per arc segment

robot.init()

# Countdown: 3 blue flashes
for _ in range(3):
    robot.colour(robot.BLUE)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

start = time.time()
robot.colour(robot.BLUE)

direction = 1   # start curving right

while time.time() - start < GAME_S:
    mm = robot.distance()

    if mm > 0 and mm < 150:
        # TODO: opponent very close — charge straight through
        pass
    else:
        # TODO: curve across the arena, alternating direction
        pass

robot.colour(robot.BLACK)
