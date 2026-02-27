import paho.mqtt.client as mqtt
import time
import sys
import tty
import termios
from pynput import keyboard

client = mqtt.Client()
client.connect("192.168.202.14", 1883, 60)

# i=1
# while True:
#     # Publish a message to the same topic
#     message = f"Hello from the Publisher! {i}"
#     client.publish("robot/test", message, retain=True)
#     print(f"Sent: {message}")
#     i += 1
#     time.sleep(1)

# client.disconnect()



# Configuration
LINEAR_SPEED = 0.5
ANGULAR_SPEED = 1.0
LINEAR_INCREMENT = 10
ANGULAR_INCREMENT = 10

# Current velocities
linear_x = 0.0
angular_z = 0.0

def get_key_bindings():
    return """
Reading from keyboard:
---------------------------
        w
   a    s    d
   
w/s : increase/decrease linear velocity
a/d : increase/decrease angular velocity
space : stop
q : quit
"""

print(get_key_bindings())

def on_press(key):
    global linear_x, angular_z
    
    try:
        if key.char == 'w':
            linear_x += LINEAR_INCREMENT
        elif key.char == 's':
            linear_x -= LINEAR_INCREMENT
        elif key.char == 'a':
            angular_z += ANGULAR_INCREMENT
        elif key.char == 'd':
            angular_z -= ANGULAR_INCREMENT
        elif key.char == ' ':
            linear_x = 0.0
            angular_z = 0.0
        elif key.char == 'q':
            return False
        else:
            linear_x = 0.0
            angular_z = 0.0
            
        # Publish velocity command as JSON
        message = f'{{"linear_x": {linear_x:.2f}, "angular_z": {angular_z:.2f}}}'
        client.publish("robot/cmd_vel", message, retain=False)
        print(f"Velocities - Linear: {linear_x:.2f}, Angular: {angular_z:.2f}")
        
    except AttributeError:
        # Stop for special keys
        linear_x = 0.0
        angular_z = 0.0
        
        # Publish velocity command as JSON
        message = f'{{"linear_x": {linear_x:.2f}, "angular_z": {angular_z:.2f}}}'
        client.publish("robot/cmd_vel", message, retain=False)
        print(f"Velocities - Linear: {linear_x:.2f}, Angular: {angular_z:.2f}")

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()

client.disconnect()