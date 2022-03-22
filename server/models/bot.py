import atexit
import math
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

kit = MotorKit()
in_progress = False
__steps_per_degree: float = 4.77  # tweak for accuracy
__arm_length: int = 190  # total arm length in mm
__stepper_upper = kit.stepper1
__stepper_lower = kit.stepper2
__steps_upper: int = 0
__steps_lower: int = 0


def get_position_in_angles():
    return {
        "lower": __steps_lower / __steps_per_degree,
        "upper": __steps_upper / __steps_per_degree
    }


def __step_once(stepper, direction):
    if direction > 0:
        stepper.onestep(direction=STEPPER.BACKWARD, style=STEPPER.INTERLEAVE)
    if direction < 0:
        stepper.onestep(direction=STEPPER.FORWARD, style=STEPPER.INTERLEAVE)


def __step_once_upper(direction):
    __step_once(__stepper_upper, -direction)
    __steps_upper += direction


def __step_once_lower(direction):
    __step_once(__stepper_lower, direction)
    __steps_lower += direction


def to_arm_angles(angle1: float, angle2: float):
    global in_progress
    global __steps_lower
    global __steps_upper

    def should_move(relative_steps: int) -> bool:
        return relative_steps != 0 and (tick % relative_steps) == 0

    def get_direction(steps: int):
        return steps / abs(steps)

    if in_progress:
        return

    in_progress = True
    # convert angles to target step positions for steppers
    target_steps_lower = round(angle1 * __steps_per_degree)
    target_steps_upper = round(angle2 * __steps_per_degree)

    # relative steps needed to get from current position to target
    relative_steps_lower = target_steps_lower - __steps_lower
    relative_steps_upper = relative_steps_lower + target_steps_upper - __steps_upper

    tick = 0
    target = max(abs(relative_steps_lower), 1) * max(abs(relative_steps_upper), 1)
    while tick <= target:
        upper_should_move = should_move(relative_steps_upper)
        lower_should_move = should_move(relative_steps_lower)
        if upper_should_move:
            direction = get_direction(relative_steps_upper)
            __step_once_upper(direction)
        if lower_should_move:
            direction = get_direction(relative_steps_lower)
            __step_once_lower(direction)

        tick += 1

    in_progress = False


def to_theta_rho(theta: float, rho: float):
    half_length = __arm_length / 2
    rho_dist = __arm_length * rho
    theta_degrees = math.degrees(theta)
    upper_angle = 180 - math.degrees(
        math.acos((((half_length ** 2) * 2) - (rho_dist ** 2)) / (2 * half_length * half_length)))
    lower_angle_offset = upper_angle / 2
    lower_angle = theta_degrees - lower_angle_offset

    to_arm_angles(lower_angle, upper_angle)


def to_home():
    to_arm_angles(0, 0)


@atexit.register
def release():
    __stepper_upper.release()
    __stepper_lower.release()
