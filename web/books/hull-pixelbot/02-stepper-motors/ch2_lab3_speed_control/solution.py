import time
import robot

robot.init()

# Full speed forward
robot.colour(robot.GREEN)
robot.move(200)
robot.colour(robot.BLACK)

time.sleep(1)

# Slow return
robot.colour(robot.BLUE)
robot.move(-200, seconds=5)
robot.colour(robot.BLACK)

time.sleep(1)

# Slow turn with flashing pixel
robot.colour(robot.YELLOW)
robot.turn(90, seconds=3, nowait=True)
while robot.moving():
    robot.colour(robot.YELLOW)
    time.sleep(0.2)
    robot.colour(robot.BLACK)
    time.sleep(0.2)
robot.colour(robot.BLACK)
