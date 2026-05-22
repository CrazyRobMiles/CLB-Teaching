import time
import robot

GAME_S = 30   # game duration in seconds

robot.init()

# Countdown: 3 red flashes
for _ in range(3):
    robot.colour(robot.RED)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

start = time.time()
robot.colour(robot.RED)

while time.time() - start < GAME_S:
    mm = robot.distance()
    if mm > 0 and mm < 50:
        # Reached the far wall — instant win
        break
    robot.move(100)

robot.colour(robot.BLACK)
