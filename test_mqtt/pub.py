import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("192.168.202.14", 1883, 60)

i=1
while True:
    # Publish a message to the same topic
    message = f"Hello from the Publisher! {i}"
    client.publish("robot/test", message, retain=True)
    print(f"Sent: {message}")
    i += 1
    time.sleep(1)

client.disconnect()