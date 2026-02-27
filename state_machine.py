# Prototype for robot state machine
# from xgolib import XGO
import puppylib as pl
import time
import math
from enum import Enum
import paho.mqtt.client as mqtt
import ast
from dataclasses import dataclass


class PuppyState(Enum):
    SEARCH = 1
    CLOSE_IN = 2
    PICK_UP = 3
    CHECK_PICKED_UP = 4


class SearchState(Enum):
    STOP = 0
    MOVE_FORWARD = 1
    LOOK_LEFT = 2
    LOOK_RIGHT = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5


@dataclass
class SearchParams:
    search_timer: float
    next_state_on_stop: SearchState

    MOVE_FORWARD_CM = 20.0
    MOVE_FORWARD_VEL_CMPS = 10.0
    LOOK_LEFT_TIME = 0.5
    LOOK_LEFT_ANGLE = 16
    LOOK_RIGHT_TIME = 0.5
    LOOK_RIGHT_ANGLE = -16
    TURN_LEFT_ANGLE = 45
    TURN_RIGHT_ANGLE = -45
    TURN_LEFT_SPEED = 50
    TURN_RIGHT_SPEED = 50


@dataclass
class DetectionResult:
    x1: float
    y1: float
    x2: float
    y2: float
    conf: float
    cls: int


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()

    try:
        data_dict = ast.literal_eval(payload_str)
        detection = DetectionResult(
            x1=data_dict.get('x1', 0.0),
            y1=data_dict.get('y1', 0.0),
            x2=data_dict.get('x2', 0.0),
            y2=data_dict.get('y2', 0.0),
            conf=data_dict.get('conf', 0.0),
            cls=data_dict.get('cls', -1)
        )
        if (detection.x1 != 0) and (detection.x2 != 0) and (detection.y1 != 0) and (detection.y2 != 0):
            currently_detected = True
            print(".")  # ,end='')
        else:
            currently_detected = False

    except (ValueError, SyntaxError) as e:
        print(f"Failed to decode message: {payload_str}")
        print(f"Error: {e}")


def search_callback():
    # Move around in some fixed pattern
    return


def close_in_callback():
    return


def pick_up_callback():
    # Routine for picking up a bottle cap
    return


def check_picked_up_callback():
    # Routine for checking if the bottle cap is successfully picked up
    return


MQTT_BROKER = "puppy1"
MQTT_PORT = 1883
MQTT_TOPIC = "yolo/bbox"

currently_detected = False
detection = None

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

dog = pl.XGO(port='/dev/ttyAMA0', version="xgomini")
dog_type = 'M'
currentState = PuppyState.SEARCH

while True:

    match currentState:
        case PuppyState.SEARCH:
            search_callback()
        case PuppyState.CLOSE_IN:
            close_in_callback()
        case PuppyState.PICK_UP:
            pick_up_callback()
        case PuppyState.CHECK_PICKED_UP:
            check_picked_up_callback()
        case _:
            print("Something went terribly wrong")