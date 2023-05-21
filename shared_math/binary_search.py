import math
from typing import Callable
import pytest

# Define the type for the priority function.
PriorityFn = Callable[[int], float]


def _get_insertion_point_sub(value: float, array_ubound: int, fn: PriorityFn, min_range: int, end_range: int):
    """Recursive helper function for the binary search.

    Parameters:
    - value (float): the value to insert
    - array_ubound (int): the upper bound of the array (array size minus 1)
    - fn (PriorityFn): the priority function that ranks array elements
    - min_range (int): the lower limit for the search range
    - end_range (int): the upper limit for the search range

    Returns:
    - int: the insertion index for the value
    """

    # Base case: when the search range is minimized to a point.
    if min_range == end_range:
        return end_range

    # Calculate the middle index of the current range.
    mid_index = math.floor((min_range + end_range) * 0.5)
    # Calculate the priority of the middle index.
    mid_prio = fn(mid_index)

    # Recursive case: depending on the priority, narrow down the search range and recurse.
    if mid_prio >= value:
        return _get_insertion_point_sub(value, array_ubound, fn, min_range, mid_index)
    else:
        return _get_insertion_point_sub(value, array_ubound, fn, mid_index + 1, end_range)


def get_insertion_point(value: float, array_ubound: int, fn: PriorityFn) -> int:
    """Main function for the binary search. It finds the insertion point for a given value
    in an array sorted by a certain priority function.

    Parameters:
    - value (float): the value to insert
    - array_ubound (int): the upper bound of the array (array size minus 1)
    - fn (PriorityFn): the priority function that ranks array elements

    Returns:
    - int: the insertion index for the value
    """
    return _get_insertion_point_sub(value, array_ubound, fn, 0, array_ubound + 1)
