import time
import robot

GAME_S = 30   # game duration in seconds

robot.init()

# Countdown: 3 flashes before the game starts
for _ in range(3):
    robot.colour(robot.RED)
    time.sleep(0.5)
    robot.colour(robot.BLACK)
    time.sleep(0.5)

# Game loop
start = time.time()

while time.time() - start < GAME_S:
    # TODO: move the robot forward
    pass

# Game over
robot.colour(robot.BLACK)
