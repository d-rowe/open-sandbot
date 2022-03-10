import time
import atexit
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

kit = MotorKit()
upper_stepper = kit.stepper1
lower_stepper = kit.stepper2

def pause():
    time.sleep(0.0015)

@atexit.register
def release():
    kit.stepper1.release()
    kit.stepper2.release()

def move_forward(stepper):
    stepper.onestep(direction=STEPPER.FORWARD, style=STEPPER.INTERLEAVE)

def move_backward(stepper):
    stepper.onestep(direction=STEPPER.BACKWARD, style=STEPPER.INTERLEAVE)

def step(lower_dir, upper_dir):
    if lower_dir > 0:
        move_forward(lower_stepper)
    if lower_dir < 1:
        move_backward(lower_stepper)
    if upper_dir > 0:
        move_forward(upper_stepper)
    if upper_dir < 1:
        move_backward(upper_stepper)
    pause()
