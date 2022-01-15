from gpiozero import Servo
from time import sleep

servo = Servo(17)

while True:
    servo.mid()
    print('mid')
    sleep(0.5)
    x = servo.min()
    print('min')
    print(x)
    sleep(1)
    servo.mid()
    print('mid')
    sleep(0.5)
    y = servo.max()
    print('max')
    print(y)