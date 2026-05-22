import time
import robot

robot.init()

# Part A: blocking move
robot.colour(robot.GREEN)
robot.move(300)
robot.colour(robot.RED)
time.sleep(1)
robot.colour(robot.BLACK)

time.sleep(1)

# Part B: nowait with wait()
robot.colour(robot.GREEN)
robot.move(300, nowait=True)
robot.colour(robot.BLUE)      # runs while motors are moving
robot.wait()                  # block until move finishes
robot.colour(robot.BLACK)

time.sleep(1)

# Part C: flashing pixel using moving()
robot.move(400, nowait=True)
while robot.moving():
    robot.colour(robot.YELLOW)
    time.sleep(0.1)
    robot.colour(robot.BLACK)
    time.sleep(0.1)
robot.colour(robot.RED)
time.sleep(0.5)
robot.colour(robot.BLACK)
