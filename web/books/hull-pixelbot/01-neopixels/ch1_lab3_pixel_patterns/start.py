import time
import robot

robot.init()

# TODO: complete the chasing loop
# It should light one green pixel at a time, moving from index 0 to 7
while True:
    for i in range(8):
        robot.colour(robot.BLACK)
        # TODO: light pixel i green using robot._pixels.set(i, robot.GREEN)
        time.sleep(0.1)

    # TODO: add a second loop that chases back from index 7 to 0
