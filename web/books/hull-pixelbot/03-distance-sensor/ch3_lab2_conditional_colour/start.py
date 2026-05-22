import time
import robot

robot.init()

while True:
    mm = robot.distance()

    # TODO: add if/elif/else to set the pixel colour based on distance:
    # - white  if mm < 0 (no reading)
    # - red    if mm < 100
    # - yellow if mm < 300
    # - green  otherwise
