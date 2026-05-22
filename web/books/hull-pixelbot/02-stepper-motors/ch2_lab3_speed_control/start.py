import time
import robot

robot.init()

# Move forward 200 mm at full speed
robot.colour(robot.GREEN)
robot.move(200)
robot.colour(robot.BLACK)

time.sleep(1)

# TODO: move backward 200 mm over 5 seconds (add seconds=5)
robot.colour(robot.BLUE)
robot.move(-200)    # TODO: add seconds=5
robot.colour(robot.BLACK)

time.sleep(1)

# TODO: turn 90 degrees over 3 seconds
robot.colour(robot.YELLOW)
robot.turn(90)      # TODO: add seconds=3
robot.colour(robot.BLACK)

# TODO: add nowait=True to the turn above and use a while robot.moving() loop
# to flash the pixel between yellow and black while the robot turns
