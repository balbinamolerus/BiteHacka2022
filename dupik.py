
from time import sleep
from gpiozero import MotionSensor
pir = MotionSensor(4)

while True:
  x=0
  t=0
  while t<50:
    if pir.wait_for_motion()==True:
      x=x+1
    sleep(0.1)
    if x>20:
      print('alarm')
      x=0
    t=t+1