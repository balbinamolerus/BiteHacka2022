import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
from gpiozero import Servo
import time

direction = 0
pir = MotionSensor(4)
servo = Servo(17)
servo.detach()


def on_message(client, userdata, message):
    global direction
    if message.topic == "position":
        # client.publish("test2", "ok", qos=0, retain=False)
        direction = int(message.payload.decode("utf-8"))
        print(direction)


broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("position", 0), ])

print("aaaa")

while True:
    print(direction)
    motion = 0
    if direction == 1:
        print(direction)
        servo.max()
        time.sleep(0.02)
        servo.detach()
        direction = 0
    elif direction == -1:
        print(dir)
        servo.min()
        time.sleep(0.02)
        servo.detach()
        direction = 0
    for i in range(30):
        if pir.motion_detected:
            motion += 1
        time.sleep(0.01)
        if motion > 10:
            print('alarm')
            client.publish("alarm", "pir", qos=0, retain=False)
            time.sleep(2)
            break
