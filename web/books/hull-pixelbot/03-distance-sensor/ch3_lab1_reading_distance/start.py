import time
import robot

robot.init()

# TODO: complete the loop to take 30 distance readings, one every 0.5 seconds
# Print each reading to the console with print()
for i in range(30):
    mm = robot.distance()
    # TODO: print the distance value
    time.sleep(0.5)
