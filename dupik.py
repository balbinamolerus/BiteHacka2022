from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
from gpiozero import Servo
import time
dir = 0
pir = MotionSensor(4)
servo = Servo(17)
servo.detach()
def on_message(client, userdata, message):
    global dir

    if message.topic == "position":
        # client.publish("test2", "ok", qos=0, retain=False)
        dir = int(message.payload.decode("utf-8"))
        print(dir)


broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("position", 0), ])


while True:
    motion = 0
    if dir == 1:
        print(dir)
        servo.max()
        time.sleep(1)
        servo.detach()
        dir = 0
    elif dir == -1:
        print(dir)
        servo.min()
        time.sleep(1)
        servo.detach()
        dir = 0
    for i in range(30):
        if pir.wait_for_motion() == True:
            motion += 1
        sleep(0.01)
        if motion > 10:
            # print('alarm')
            client.publish("alarm", "pir", qos=0, retain=False)
            sleep(2)
            break