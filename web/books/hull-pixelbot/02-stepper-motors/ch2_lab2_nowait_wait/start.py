import time
import robot

robot.init()

# Part A: observe blocking — run this first and watch when the pixel changes
robot.colour(robot.GREEN)
robot.move(300)     # blocking — pixel stays green until move finishes
robot.colour(robot.RED)
time.sleep(1)
robot.colour(robot.BLACK)

time.sleep(1)

# Part B: add nowait=True to the move below, add a colour change after it,
# and add robot.wait() before the next move
robot.colour(robot.GREEN)
robot.move(300)     # TODO: add nowait=True here
# TODO: add a line here that sets the pixel to a different colour
# TODO: add robot.wait() here before the turn
robot.turn(180)
robot.colour(robot.BLACK)
