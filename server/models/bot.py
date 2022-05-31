import math
from time import sleep
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

# Hardware configuration
_ARM_GEAR_TEETH = 60
_STEPPER_GEAR_TEETH = 14
_DEGREES_PER_STEP = 1.8

_steps_per_degree: float = _ARM_GEAR_TEETH / _STEPPER_GEAR_TEETH / _DEGREES_PER_STEP * 2
_kit = MotorKit()
_stepper_upper = _kit.stepper1
_stepper_lower = _kit.stepper2
_steps_upper: int = 0
_steps_lower: int = 0
_step_delay: int = 0
_force_stop: bool = False
in_progress: bool = False


def set_speed(speed: int):
    global _step_delay
    _step_delay = 100 - speed


def stop():
    global _force_stop
    if in_progress:
        _force_stop = True


def set_home():
    global _steps_upper
    global _steps_lower
    _steps_upper = 0
    _steps_lower = 0


def _step_once(stepper, direction):
    if direction > 0:
        stepper.onestep(direction=STEPPER.BACKWARD, style=STEPPER.INTERLEAVE)
    if direction < 0:
        stepper.onestep(direction=STEPPER.FORWARD, style=STEPPER.INTERLEAVE)


def _step_once_upper(direction):
    global _steps_upper
    _step_once(_stepper_upper, -direction)
    _steps_upper += direction


def _step_once_lower(direction):
    global _steps_lower
    _step_once(_stepper_lower, direction)
    _steps_lower += direction


def to_arm_angles(angle1: float, angle2: float):
    global in_progress
    global _steps_lower
    global _steps_upper
    global _force_stop
    global _step_delay

    def get_direction(steps: int):
        if steps == 0:
            return 0
        return steps // abs(steps)

    if in_progress:
        return

    # convert angles to target step positions for steppers
    target_steps_lower = round(angle1 * _steps_per_degree)
    target_steps_upper = round(angle2 * _steps_per_degree) + target_steps_lower

    # relative steps needed to get from current position to target
    relative_steps_lower = target_steps_lower - _steps_lower
    relative_steps_upper = target_steps_upper - _steps_upper

    if relative_steps_lower == 0 and relative_steps_upper == 0:
        # already at target position
        return

    is_lower_arm_faster = abs(relative_steps_lower) > abs(relative_steps_upper)

    if is_lower_arm_faster:
        faster_steps = relative_steps_lower
        slower_steps = relative_steps_upper
        faster_step_once = _step_once_lower
        slower_step_once = _step_once_upper
    else:
        faster_steps = relative_steps_upper
        slower_steps = relative_steps_lower
        faster_step_once = _step_once_upper
        slower_step_once = _step_once_lower

    faster_direction = get_direction(faster_steps)
    slower_direction = get_direction(slower_steps)
    abs_faster_steps = abs(faster_steps)
    abs_slower_steps = abs(slower_steps)
    speed_ratio = abs_slower_steps / abs_faster_steps

    in_progress = True

    # Since we can only move one stepper at a time, we'll need to interpolate steps
    slower_creep = 0
    for i in range(abs_faster_steps):
        # handle stop command
        if _force_stop:
            _force_stop = False
            break

        faster_step_once(faster_direction)
        slower_creep += speed_ratio
        while slower_creep >= 1:
            slower_step_once(slower_direction)
            slower_creep -= 1

        if _step_delay > 0:
            sleep(_step_delay / 1000)

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


def release():
    stop()
    _stepper_upper.release()
    _stepper_lower.release()
