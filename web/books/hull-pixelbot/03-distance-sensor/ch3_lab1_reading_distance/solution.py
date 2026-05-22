import time
import robot

robot.init()

for i in range(30):
    mm = robot.distance()
    print("Distance:", mm, "mm")
    time.sleep(0.5)
