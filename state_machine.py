# Prototype for robot state machine
from xgolib import XGO
import time
import math
from enum import Enum


class PuppyState(Enum):
    SEARCH = 1
    CLOSE_IN = 2
    PICK_UP = 3
    CHECK_PICKED_UP = 4


def search_callback():
    return


def close_in_callback():
    return


def pick_up_callback():
    return


def check_picked_up_callback():
    return


dog = XGO(port='/dev/ttyAMA0',version="xgomini")
dog_type='M'
currentState = PuppyState.SEARCH

while True:
    # Send frame from video camera

    # Get information from MQTT

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





