# Prototype for robot state machine
from statemachine import StateChart, State

class LitterPuppySM(StateChart):
    search = State(initial = True)
    close_in = State()
    pick_up = State()
    check_picked_up = State()

    cap_detected = search.to(close_in)
    cap_lost = close_in.to(search)
    cap_reached = close_in.to(pick_up)
    pickup_motion_finished = pick_up.to(check_picked_up)
    pickup_success = check_picked_up.to(search)
    pickup_failed = check_picked_up.to(close_in)
