import time
import robot

robot.init()

while True:
    mm = robot.distance()

    if mm < 0:
        robot.colour(robot.WHITE)
    elif mm < 100:
        robot.colour(robot.RED)
    elif mm < 300:
        robot.colour(robot.YELLOW)
    else:
        robot.colour(robot.GREEN)
