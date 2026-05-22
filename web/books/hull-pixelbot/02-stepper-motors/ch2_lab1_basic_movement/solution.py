import time
import robot

robot.init()

robot.colour(robot.GREEN)
robot.move(300)
robot.colour(robot.BLACK)

time.sleep(0.5)

robot.colour(robot.BLUE)
robot.move(-300)
robot.colour(robot.BLACK)

time.sleep(0.5)

robot.colour(robot.YELLOW)
robot.turn(90)
robot.colour(robot.BLACK)

time.sleep(0.5)

robot.colour(robot.MAGENTA)
robot.turn(-90)
robot.colour(robot.BLACK)
