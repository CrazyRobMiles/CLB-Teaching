import time
import robot

robot.init()

# Part A: drive a square with a different colour on each side
colours = [robot.RED, robot.GREEN, robot.BLUE, robot.CYAN]

# TODO: complete the loop — move 200 mm and turn 90 degrees for each colour
for c in colours:
    robot.colour(c)
    # TODO: move forward 200 mm
    # TODO: turn 90 degrees

robot.colour(robot.BLACK)
time.sleep(1)

# Part B: drive an equilateral triangle with 200 mm sides
# TODO: write a loop that drives the triangle (hint: exterior angle = 120 degrees)

time.sleep(1)

# Part C: figure of eight
# TODO: add two arc() calls to trace a figure of eight
