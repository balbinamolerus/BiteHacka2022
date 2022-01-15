from time import sleep
from gpiozero import MotionSensor

pir = MotionSensor(4)

while True:
    motion = 0
    for i in range(30):
        if pir.wait_for_motion() == True:
            motion += 1
        sleep(0.01)
        if motion > 10:
            print('alarm')
            sleep(2)
            break