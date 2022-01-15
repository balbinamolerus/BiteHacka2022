import RPi.GPIO as GPIO
import time
#GPIO SETUP
channel = 17
channel_pir = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel_pir, GPIO.IN) 
def callback(channel):
        if GPIO.input(channel):
                print ('Sound Detected!')
        else:
                print ('Sound Detected!')

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
# infinite loop
j=0
while True:
    i=GPIO.input(channel_pir)
    if i==0:                 #When output from motion sensor is LOW
        z=z+1
        print(j)
        time.sleep(0.1)
        if z==2:
            j=0
            print ("No Intruder detected")
    elif i==1: 
        z=0
        j=j+1
        if j >=20:
            print ("Intruder detected")
        time.sleep(0.1)
