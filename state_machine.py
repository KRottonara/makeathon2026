# Prototype for robot state machine
from statemachine import StateChart, State

class LitterPuppySM(StateChart):
    search = State(initial = True)
    close_in = State()
    pick_up = State()
    check_picked_up = State()
