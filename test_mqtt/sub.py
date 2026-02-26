import paho.mqtt.client as mqtt
import time

# Callback when we connect to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic "robot/test"
    client.subscribe("robot/test")

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} | Message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the local broker
client.connect("192.168.202.14", 1883, 60)

print("Waiting for messages...")
client.loop_start()  # Start the loop to process callbacks

while True:
    print("I am capable of multitasking!")
    time.sleep(1)  # Simulate doing other work while waiting for messages
    pass  # Keep the script running to receive messages