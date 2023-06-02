import numpy as np
from .geometry import Rect, Vec2, BezierContour, BezierPath, BezierPoint
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


class TestVec2:
    def test_add(self):
        vec1 = Vec2(1, 2)
        v2 = Vec2(3, 4)
        result = vec1 + v2
        assert result.x == 4
        assert result.y == 6

    def test_sub(self):
        vec1 = Vec2(1, 2)
        v2 = Vec2(3, 4)
        result = vec1 - v2
        assert result.x == -2
        assert result.y == -2

    def test_translate(self):
        vec = Vec2(1, 2)
        translation = Vec2(2, 3)
        vec.translate(translation)
        assert vec.x == 3
        assert vec.y == 5

    def test_transform(self):
        vec = Vec2(1, 2)
        matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        vec.transform(matrix)
        assert vec.x == 2
        assert vec.y == 4


class TestRect:
    def test_translate(self):
        r1 = Rect(0, 0, 2, 2)
        translation = Vec2(1, 1)
        r1.translate(translation)
        assert r1.minx == 1
        assert r1.maxx == 3
        assert r1.miny == 1
        assert r1.maxy == 3

    def test_transform(self):
        r1 = Rect(0, 0, 2, 2)
        matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        r1.transform(matrix)
        assert r1.minx == 0
        assert r1.maxx == 4
        assert r1.miny == 0
        assert r1.maxy == 4

    def test_bounds(self):
        r1 = Rect(0, 0, 2, 2)
        bounds = r1.bounds()
        assert bounds.minx == 0
        assert bounds.maxx == 2
        assert bounds.miny == 0
        assert bounds.maxy == 2


class TestBezierPoint:
    def test_translate(self):
        point = BezierPoint(Vec2(0, 0), Vec2(1, 1), Vec2(2, 2))
        translation = Vec2(1, 1)
        point.translate(translation)
        assert point.pos.x == 1
        assert point.pos.y == 1
        assert point.control1.x == 2
        assert point.control1.y == 2
        assert point.control2.x == 3
        assert point.control2.y == 3

    def test_transform(self):
        point = BezierPoint(Vec2(1, 2), Vec2(2, 3), Vec2(3, 4))
        matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        point.transform(matrix)
        assert point.pos.x == 2
        assert point.pos.y == 4
        assert point.control1.x == 4
        assert point.control1.y == 6
        assert point.control2.x == 6
        assert point.control2.y == 8


class TestBezierContour:
    def test_translate(self):
        contour = BezierContour()
        point = BezierPoint(Vec2(0, 0), Vec2(1, 1), Vec2(2, 2))
        contour.add_point(point)
        translation = Vec2(1, 1)
        contour.translate(translation)
        assert contour.points[0].pos.x == 1
        assert contour.points[0].pos.y == 1
        assert contour.points[0].control1.x == 2
        assert contour.points[0].control1.y == 2
        assert contour.points[0].control2.x == 3
        assert contour.points[0].control2.y == 3

    def test_transform(self):
        contour = BezierContour()
        point = BezierPoint(Vec2(1, 2), Vec2(2, 3), Vec2(3, 4))
        contour.add_point(point)
        matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        contour.transform(matrix)
        assert contour.points[0].pos.x == 2
        assert contour.points[0].pos.y == 4
        assert contour.points[0].control1.x == 4
        assert contour.points[0].control1.y == 6
        assert contour.points[0].control2.x == 6
        assert contour.points[0].control2.y == 8


class TestBezierPath:
    def test_translate(self):
        path = BezierPath()
        contour = BezierContour()
        point = BezierPoint(Vec2(0, 0), Vec2(1, 1), Vec2(2, 2))
        contour.add_point(point)
        path.add_contour(contour)
        translation = Vec2(1, 1)
        path.translate(translation)
        assert path.contours[0].points[0].pos.x == 1
        assert path.contours[0].points[0].pos.y == 1
        assert path.contours[0].points[0].control1.x == 2
        assert path.contours[0].points[0].control1.y == 2
        assert path.contours[0].points[0].control2.x == 3
        assert path.contours[0].points[0].control2.y == 3

    def test_transform(self):
        path = BezierPath()
        contour = BezierContour()
        point = BezierPoint(Vec2(1, 2), Vec2(2, 3), Vec2(3, 4))
        contour.add_point(point)
        path.add_contour(contour)
        matrix = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
        path.transform(matrix)
        assert path.contours[0].points[0].pos.x == 2
        assert path.contours[0].points[0].pos.y == 4
        assert path.contours[0].points[0].control1.x == 4
        assert path.contours[0].points[0].control1.y == 6
        assert path.contours[0].points[0].control2.x == 6
        assert path.contours[0].points[0].control2.y == 8

    def test_contains(self):
        path = BezierPath()
        contour = BezierContour()
        point1 = BezierPoint(Vec2(0, 0), Vec2(1, 1), Vec2(2, 2))
        point2 = BezierPoint(Vec2(3, 3), Vec2(4, 4), Vec2(5, 5))
        contour.add_point(point1)
        contour.add_point(point2)
        path.add_contour(contour)
        assert path.contains(Vec2(1, 1))
        assert path.contains(Vec2(3, 3))
        assert not path.contains(Vec2(6, 6))

    def test_contains_advance(self):
        path = BezierPath()
        contour = BezierContour()
        point1 = BezierPoint(Vec2(0, 0), Vec2(1, 1), Vec2(2, 2))
        point2 = BezierPoint(Vec2(3, 3), Vec2(4, 4), Vec2(5, 5))
        point3 = BezierPoint(Vec2(6, 4), Vec2(5.5, 1), Vec2(4, 2))
        point4 = BezierPoint(Vec2(2, 3), Vec2(1.5, 3.5), Vec2(1, 4))
        contour.add_point(point1)
        contour.add_point(point2)
        contour.add_point(point3)
        contour.add_point(point4)
        path.add_contour(contour)
        assert path.contains(Vec2(1, 1))
        assert path.contains(Vec2(2.99, 2.99))
        assert not path.contains(Vec2(6, 6))
