import paho.mqtt.client as mqtt
import time
import json
from xgolib import XGO
import math
import numpy as np

dog = XGO(port='/dev/ttyAMA0', version="xgomini")


def dog_move_x(dog, speed): # speed in cm/s
    speed_corrected = speed * 0.85
    # Assuming the robot can handle continuous velocity updates
    dog.move('x', speed_corrected)

def dog_turn(dog, speed): # speed in deg/s
    dog.turn(speed)  # Using turn method from XGO library

# Global variables for motion
linear_x = 0.0
angular_z = 0.0

# Callback when we connect to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic "robot/cmd_vel"
    client.subscribe("robot/cmd_vel")

# Callback when a message is received
def on_message(client, userdata, msg):
    global linear_x, angular_z
    try:
        data = json.loads(msg.payload.decode())
        
        # Update velocities from JSON
        linear_x = float(data.get("linear_x", 0.0))
        angular_z = float(data.get("angular_z", 0.0))
        
        print(f"Received - Linear X: {linear_x:.2f}, Angular Z: {angular_z:.2f}")

        # Command the robot
        # Scale values: linear ~20 for 0.5 -> 10 cm/s
        # angular ~20 for 1.0 -> 20 deg/s
        
        dog_move_x(dog, linear_x) 
        dog_turn(dog, angular_z)

    except json.JSONDecodeError:
        print(f"Failed to parse message: {msg.payload.decode()}")
    except Exception as e:
        print(f"Error controlling robot: {e}")

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