import time
import robot

robot.init()

# Part A: square
colours = [robot.RED, robot.GREEN, robot.BLUE, robot.CYAN]

for c in colours:
    robot.colour(c)
    robot.move(200)
    robot.turn(90)

robot.colour(robot.BLACK)
time.sleep(1)

# Part B: equilateral triangle
robot.colour(robot.YELLOW)
for _ in range(3):
    robot.move(200)
    robot.turn(120)

robot.colour(robot.BLACK)
time.sleep(1)

# Part C: figure of eight
robot.colour(robot.MAGENTA)
robot.arc(150, 360)
robot.arc(-150, 360)
robot.colour(robot.BLACK)
