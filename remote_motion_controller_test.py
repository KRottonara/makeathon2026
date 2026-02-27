import paho.mqtt.client as mqtt
import json
import time

# Variables to store twist data
linear_x = 0.0
angular_z = 0.0

# Callback when we connect to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic for twist messages
    client.subscribe("robot/cmd_vel")

# Callback when a message is received
def on_message(client, userdata, msg):
    global linear_x, angular_z
    
    try:
        data = json.loads(msg.payload.decode())
        
        # Update linear velocities
        linear_x = float(data.get("linear_x", 0.0))
        
        # Update angular velocities
        angular_z = float(data.get("angular_z", 0.0))
        
        print(f"Received - Linear X: {linear_x}, Angular Z: {angular_z}")
    except json.JSONDecodeError:
        print(f"Failed to parse message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the local broker
client.connect("192.168.202.14", 1883, 60)

print("Waiting for twist messages...")
client.loop_start()

while True:
    print(f"Current velocities - Linear: ({linear_x}) | Angular: ({angular_z})")
    time.sleep(1)