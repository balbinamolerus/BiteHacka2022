from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)

GPIO.write(14, LOW)

while True:
    if GPIO.input(14):
        print('ruch')