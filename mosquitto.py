import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    global bedroom_delay, switch_off
    if message.topic == "test" and str(message.payload.decode("utf-8")) == "test1":
        client.publish("test2", "ok", qos=0, retain=False)



broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
# client.on_message = on_message
client.connect(broker_address, 1881)
# client.loop_start()
# client.subscribe([("test", 0), ])

while True:
    client.publish("test2", "ok?", qos=0, retain=False)
    time.sleep(1)
