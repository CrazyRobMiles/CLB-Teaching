import time
import robot

robot.init()

# Quarter-circle arc right
robot.colour(robot.CYAN)
robot.arc(150, 90)
robot.colour(robot.BLACK)

time.sleep(1)

# Quarter-circle arc left to undo
robot.colour(robot.MAGENTA)
robot.arc(-150, 90)
robot.colour(robot.BLACK)

time.sleep(1)

# Full circle
robot.colour(robot.GREEN)
robot.arc(200, 360)
robot.colour(robot.BLACK)

time.sleep(1)

# arc(0, 360) rotates on the spot — same as turn(360)
robot.colour(robot.YELLOW)
robot.arc(0, 360)
robot.colour(robot.BLACK)
