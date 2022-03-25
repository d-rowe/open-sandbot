import atexit
import math
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

kit = MotorKit()
in_progress = False
__steps_per_degree: float = 4.9  # tweak for accuracy
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
    global __steps_upper
    __step_once(__stepper_upper, -direction)
    __steps_upper += direction


def __step_once_lower(direction):
    global __steps_lower
    __step_once(__stepper_lower, direction)
    __steps_lower += direction


def to_arm_angles(angle1: float, angle2: float):
    global in_progress
    global __steps_lower
    global __steps_upper

    def get_direction(steps: int):
        if steps == 0:
            return 0
        return steps / abs(steps)

    if in_progress:
        return

    in_progress = True
    # convert angles to target step positions for steppers
    target_steps_lower = round(angle1 * __steps_per_degree)
    target_steps_upper = round(angle2 * __steps_per_degree) + target_steps_lower

    # relative steps needed to get from current position to target
    # relative_steps_lower = target_steps_lower - __steps_lower
    # relative_steps_upper = target_steps_upper - __steps_upper
    relative_steps_lower = target_steps_lower
    relative_steps_upper = target_steps_upper

    if relative_steps_lower == 0 and relative_steps_upper == 0:
        # already at target position
        return

    print('Relative steps planned: {}, {}'
          .format(relative_steps_lower, relative_steps_upper))

    is_lower_arm_faster = abs(relative_steps_lower) > abs(relative_steps_upper)
    faster_steps = relative_steps_lower if is_lower_arm_faster else relative_steps_upper
    slower_steps = relative_steps_upper if is_lower_arm_faster else relative_steps_lower
    faster_direction = get_direction(faster_steps)
    slower_direction = get_direction(slower_steps)
    abs_faster_steps = abs(faster_steps)
    abs_slower_steps = abs(slower_steps)
    speed_ratio = abs_slower_steps / abs_faster_steps
    faster_step_once = __step_once_lower if is_lower_arm_faster else __step_once_upper
    slower_step_once = __step_once_upper if is_lower_arm_faster else __step_once_lower

    # Since we can only move one stepper at a time, we'll need to interpolate steps
    slower_creep = 0
    for i in range(abs_faster_steps):
        faster_step_once(faster_direction)
        slower_creep += speed_ratio
        while slower_creep >= 1:
            slower_step_once(slower_direction)
            slower_creep -= 1

    in_progress = False


def to_theta_rho(theta: float, rho: float):
    theta_degrees = math.degrees(theta)
    upper_angle = 180 - math.degrees(
        math.acos((((0.5 ** 2) * 2) - (rho ** 2)) / 0.5))
    lower_angle_offset = upper_angle / 2
    lower_angle = theta_degrees - lower_angle_offset

    to_arm_angles(lower_angle, upper_angle)


def to_home():
    to_arm_angles(0, 0)


@atexit.register
def release():
    __stepper_upper.release()
    __stepper_lower.release()
