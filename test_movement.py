from xgolib import XGO
import time
import math
import numpy as np

dog = XGO(port='/dev/ttyAMA0',version="xgomini")
dog_type='M'


def actually_turn_by(dog, deg, turn_speed, turn_acc=1):
    current_yaw = dog.read_yaw()
    target_yaw = current_yaw + deg

    delta = 5
    k_speed = 1
    min_speed = 10
    speed = 0
    acc = turn_acc
    loop_time = 0.01

    while abs(current_yaw - target_yaw) >= delta:
        current_yaw = dog.read_yaw()
        pos_error = target_yaw-current_yaw
        # print("P: ", pos_error)
        target_speed = k_speed * pos_error
        speed_error = target_speed-speed
        speed = speed + math.copysign(acc, speed_error)

        if speed > abs(turn_speed):
            speed = abs(turn_speed)
        elif speed < -abs(turn_speed):
            speed = -abs(turn_speed)
        elif abs(speed) < min_speed:
            speed = math.copysign(min_speed, speed)

        # print("V: ", speed)
        dog.turn(speed)

        time.sleep(loop_time)

    dog.turn(0)

def move_forward_cm(dog, speed, dist_cm):
    speed_corrected = speed * 0.85
    dog.move('x', speed_corrected)
    time.sleep(dist_cm / speed)
    dog.move('x', 0)

print("Battery: ", dog.read_battery())

# Everything other than trot is trash
dog.gait_type("trot")

dog.translation('z', 100)
dog.attitude('p', 0)
time.sleep(0.5)

move_forward_cm(dog, 20.0, 100.0)
# actually_turn_by(dog, 180, 50)

dog.stop()

movement_test_copy.py
2 KB
