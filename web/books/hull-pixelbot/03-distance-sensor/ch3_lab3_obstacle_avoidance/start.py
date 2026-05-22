import time
import robot

robot.init()

robot.colour(robot.GREEN)

while True:
    mm = robot.distance()

    if mm > 0 and mm < 200:
        # Obstacle detected
        # TODO: set pixel red
        # TODO: move backward 100 mm
        # TODO: turn 90 degrees
        # TODO: set pixel green again
        pass
    else:
        # Path clear — inch forward
        # TODO: move forward 50 mm
        pass
