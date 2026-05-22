import time
import robot

robot.init()

while True:
    for i in range(8):
        robot.colour(robot.BLACK)
        robot._pixels.set(i, robot.GREEN)
        time.sleep(0.1)

    for i in range(7, -1, -1):
        robot.colour(robot.BLACK)
        robot._pixels.set(i, robot.GREEN)
        time.sleep(0.1)
