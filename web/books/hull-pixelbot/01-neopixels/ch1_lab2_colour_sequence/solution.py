import time
import robot

robot.init()

colours = [
    robot.RED,
    robot.GREEN,
    robot.BLUE,
    robot.CYAN,
    robot.MAGENTA,
    robot.YELLOW,
    robot.WHITE,
    robot.BLACK,
]

while True:
    for c in colours:
        robot.colour(c)
        time.sleep(0.5)
