import atexit
import math
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

kit = MotorKit()
in_progress = False
__steps_per_degree: float = 4.77  # tweak for accuracy
__arm_length: int = 190  # total arm length in mm
__upper_home_degree = 90
__lower_home_degree = 180
__upper_stepper = kit.stepper1
__lower_stepper = kit.stepper2
__upper_position: int = round(__upper_home_degree * __steps_per_degree)
__lower_position: int = round(__lower_home_degree * __steps_per_degree)


def get_position_in_angles():
    return {
        "lower": __lower_position / __steps_per_degree,
        "upper": __upper_position / __steps_per_degree
    }


def __step(stepper, direction):
    if direction > 0:
        stepper.onestep(direction=STEPPER.BACKWARD, style=STEPPER.INTERLEAVE)
    if direction < 1:
        stepper.onestep(direction=STEPPER.FORWARD, style=STEPPER.INTERLEAVE)


def __upper_step(direction):
    __step(__upper_stepper, -direction)


def __lower_step(direction):
    __step(__lower_stepper, direction)


def to_arm_angles(angle1: float, angle2: float):
    global in_progress
    global __lower_position
    global __upper_position

    def should_move(relative_steps: int) -> bool:
        return relative_steps != 0 and (tick % relative_steps) == 0

    def get_direction(steps: int):
        return steps / abs(steps)

    in_progress = True
    # convert angles to target step positions for steppers
    target_lower_steps = round(angle1 * __steps_per_degree)
    target_upper_steps = round(angle2 * __steps_per_degree)

    # relative steps needed to get from current position to target
    relative_lower_steps = target_lower_steps - __lower_position
    relative_upper_steps = relative_lower_steps + target_upper_steps - __upper_position

    tick = 0
    target = max(abs(relative_lower_steps), 1) * max(abs(relative_upper_steps), 1)
    while tick <= target:
        upper_should_move = should_move(relative_lower_steps)
        lower_should_move = should_move(relative_upper_steps)
        if upper_should_move:
            direction = get_direction(relative_lower_steps)
            __upper_step(direction)
            __upper_position += direction
        if lower_should_move:
            direction = get_direction(relative_upper_steps)
            __lower_step(direction)
            __lower_position += direction

        tick += 1

    # __lower_position = target_lower_steps
    # __upper_position = target_upper_steps
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
    to_arm_angles(90, 180)


def release():
    __upper_stepper.release()
    __lower_stepper.release()


@atexit.register
def exit():
    release()
