import numpy as np
from .geometry import rect, vec2
from .binary_search import get_insertion_point


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


class TestRect:
    def test_contains(self):
        rect1 = rect(0, 0, 5, 5)
        rect2 = rect(1, 1, 4, 4)
        rect3 = rect(6, 6, 10, 10)
        vec = vec2(2, 2)

        assert rect1.contains(rect2) is True
        assert rect1.contains(rect3) is False
        assert rect1.contains(vec) is True

    def test_translate(self):
        rect1 = rect(0, 0, 5, 5)
        translation = vec2(2, 3)
        expected_rect = rect(2, 3, 7, 8)

        rect1.translate(translation)

        assert rect1.minx == expected_rect.minx
        assert rect1.maxx == expected_rect.maxx
        assert rect1.miny == expected_rect.miny
        assert rect1.maxy == expected_rect.maxy

    def test_transform(self):
        rect1 = rect(0, 0, 5, 5)
        transformation = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        expected_rect = rect(0, 0, 10, 10)

        rect1.transform(transformation)

        assert rect1.minx == expected_rect.minx
        assert rect1.maxx == expected_rect.maxx
        assert rect1.miny == expected_rect.miny
        assert rect1.maxy == expected_rect.maxy


class TestVec2:
    def test_add(self):
        v1 = vec2(1, 2)
        v2 = vec2(3, 4)
        expected_result = vec2(4, 6)

        result = v1 + v2

        assert result.x == expected_result.x
        assert result.y == expected_result.y

    def test_subtract(self):
        v1 = vec2(5, 8)
        v2 = vec2(2, 3)
        expected_result = vec2(3, 5)

        result = v1 - v2

        assert result.x == expected_result.x
        assert result.y == expected_result.y

    def test_translate(self):
        vec1 = vec2(2, 3)
        translation = vec2(4, 5)
        expected_vec = vec2(6, 8)

        vec1.translate(translation)

        assert vec1.x == expected_vec.x
        assert vec1.y == expected_vec.y

    def test_transform(self):
        vec1 = vec2(2, 3)
        transformation = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        expected_vec = vec2(4, 6)

        vec1.transform(transformation)

        assert vec1.x == expected_vec.x
        assert vec1.y == expected_vec.y
