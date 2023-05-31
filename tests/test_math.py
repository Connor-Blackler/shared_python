from shared_python.shared_math.binary_search import get_insertion_point


def test_get_insertion_point():
    array = list(range(1, 11))  # Define a test array.
    def priority_fn(x): return array[x]  # Define a test priority function.

    # Check the correct position for an existing element.
    assert get_insertion_point(5, len(array)-1, priority_fn) == 4

    # Check the correct position for a non-existing element.
    assert get_insertion_point(5.5, len(array)-1, priority_fn) == 5

    # Check the correct position for a smaller element than all existing ones.
    assert get_insertion_point(0, len(array)-1, priority_fn) == 0

    # Check the correct position for a larger element than all existing ones.
    assert get_insertion_point(20, len(array)-1, priority_fn) == len(array)
