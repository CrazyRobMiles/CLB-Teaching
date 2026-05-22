import time
import robot

robot.init()

# TODO: drive a quarter-circle arc of 150 mm radius, turning right
robot.colour(robot.CYAN)
# robot.arc(???, ???)
robot.colour(robot.BLACK)

time.sleep(1)

# TODO: drive a quarter-circle arc of 150 mm radius, turning left
robot.colour(robot.MAGENTA)
# robot.arc(???, ???)
robot.colour(robot.BLACK)

time.sleep(1)

# TODO: drive a full circle of 200 mm radius
robot.colour(robot.GREEN)
# robot.arc(???, ???)
robot.colour(robot.BLACK)

time.sleep(1)

# TODO: what does arc(0, 360) do?
robot.colour(robot.YELLOW)
robot.arc(0, 360)
robot.colour(robot.BLACK)
