import time
import robot

robot.init()

robot.colour(robot.GREEN)

while True:
    mm = robot.distance()

    if mm > 0 and mm < 200:
        robot.colour(robot.RED)
        robot.move(-100)
        robot.turn(90)
        robot.colour(robot.GREEN)
    else:
        robot.move(50)
