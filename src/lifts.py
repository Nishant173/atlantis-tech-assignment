"""
Assumptions:
    - There are 5 lifts.
    - There are 20 floors numbered 1-20. There is a ground floor numbered 0.
    - We cannot go down from floor 0
    - We cannot go up from floor 20
"""

import random
from typing import List, Tuple

import numpy as np

from errors import InvalidLiftRequestError


def raise_exception_if_invalid_lift_request(lift_request: str) -> None:
    if lift_request in ['0D', '20U']:
        raise InvalidLiftRequestError("Cannot go down from floor 0; and cannot go up from floor 20")
    if lift_request[-1] not in ['D', 'U']:
        raise InvalidLiftRequestError("Expected last character of `lift_request` to be in ['D', 'U']")
    try:
        destination_floor = int(lift_request[:-1])
    except ValueError:
        raise InvalidLiftRequestError("All characters until the last character must be an integer from 0-20 (to indicate the destination floor)")
    if destination_floor not in range(0, 20+1):
        raise InvalidLiftRequestError("Floor range is 0-20")
    return None


def get_floor_and_direction(lift: str) -> Tuple[int, str]:
    """
    Returns tuple of (floor, direction).
    >>> get_floor_and_direction(lift='5U') # Returns (5, 'U')
    >>> get_floor_and_direction(lift='12D') # Returns (12, 'D')
    >>> get_floor_and_direction(lift='19') # Returns (19, '')
    """
    if lift[-1] not in ['D', 'U']:
        return (int(lift), '')
    return (int(lift[:-1]), lift[-1])


def generate_random_lift_position() -> str:
    floor = random.randint(0, 20)
    if floor == 0:
        direction = random.choice(['', 'U'])
    elif floor == 20:
        direction = random.choice(['', 'D'])
    else:
        direction = random.choice(['', 'U', 'D'])
    return f"{floor}{direction}"


def generate_random_lift_positions(how_many: int) -> List[str]:
    return [generate_random_lift_position() for _ in range(how_many)]


def compute_waiting_time_units(lift_request: str, lift_position: str) -> int:
    """Returns number of units of time the user has to wait for the requested lift"""
    current_position, direction = get_floor_and_direction(lift=lift_position)
    dest_position, dest_direction = get_floor_and_direction(lift=lift_request)
    
    # Lift is stagnant
    if direction == '':
        return abs(current_position - dest_position)

    # Lift coming towards user
    if direction == 'U' and current_position < dest_position:
        return dest_position - current_position
    elif direction == 'D' and current_position > dest_position:
        return current_position - dest_position

    # Lift going away from user
    basement_floor, last_floor = 0, 20
    if direction == 'U' and current_position > dest_position:
        time_to_get_to_top = last_floor - current_position
        time_from_top_to_destination = last_floor - dest_position
        return time_to_get_to_top + time_from_top_to_destination
    elif direction == 'D' and current_position < dest_position:
        time_to_get_to_bottom = current_position - basement_floor
        time_from_bottom_to_destination = dest_position
        return time_to_get_to_bottom + time_from_bottom_to_destination
    raise Exception("What just happened?")


if __name__ == "__main__":
    LIFT_POSITIONS = generate_random_lift_positions(how_many=5) # ['0', '1D', '12', '4U', '19D']
    LIFT_REQUEST = '17D' # 17D 10D 5U

    raise_exception_if_invalid_lift_request(lift_request=LIFT_REQUEST)

    waiting_times = []
    for lift_pos in LIFT_POSITIONS:
        waiting_time = compute_waiting_time_units(
            lift_position=lift_pos,
            lift_request=LIFT_REQUEST,
        )
        waiting_times.append(waiting_time)
    
    # closest_lift, _ = get_floor_and_direction(lift=LIFT_POSITIONS[np.argmin(waiting_times)])
    closest_lift = int(np.argmin(waiting_times)) + 1

    print(
        f"Lift positions: {LIFT_POSITIONS}",
        f"Lift request: {LIFT_REQUEST}",
        f"Waiting times: {waiting_times}",
        f"Closest lift: #{closest_lift}",
        sep="\n",
    )