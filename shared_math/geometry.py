from __future__ import annotations
from typing import List
from functools import singledispatchmethod
import numpy as np
from shapely.geometry import Point, LineString


class Vec2():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vec2):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other: Vec2):
        return Vec2(self.x - other.x, self.y - other.y)

    def to_tuple(self):
        return self.x, self.y

    def translate(self, other: Vec2):
        self.x = self.x + other.x
        self.y = self.y + other.y

    def transform(self, matrix: np.ndarray):
        vector = np.array([self.x, self.y, 1])
        transformed_vector = vector @ matrix.T

        self.x = transformed_vector[0]
        self.y = transformed_vector[1]


class Rect():
    def __init__(self, minx: float, miny: float, maxx: float, maxy: float) -> None:
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def width(self) -> float:
        return abs(self.maxx - self.minx)

    def width(self) -> float:
        return abs(self.maxy - self.miny)

    def __add__(self, other: Rect) -> Rect:
        minx = min(self.minx, other.minx)
        miny = min(self.miny, other.miny)
        maxx = max(self.maxx, other.maxx)
        maxy = max(self.maxy, other.maxy)
        return Rect(minx, miny, maxx, maxy)

    def translate(self, translation: Vec2) -> None:
        self.minx += translation.x
        self.miny += translation.y
        self.maxx += translation.x
        self.maxy += translation.y

    def transform(self, matrix: np.ndarray) -> None:
        corners = np.array([[self.minx, self.miny, 1], [self.minx, self.maxy, 1], [
                           self.maxx, self.miny, 1], [self.maxx, self.maxy, 1]])
        transformed_corners = corners @ matrix.T
        self.minx = np.min(transformed_corners[:, 0])
        self.miny = np.min(transformed_corners[:, 1])
        self.maxx = np.max(transformed_corners[:, 0])
        self.maxy = np.max(transformed_corners[:, 1])

    @singledispatchmethod
    def contains(self, other: Rect) -> bool:
        return (
            self.minx <= other.minx and
            self.maxx >= other.maxx and
            self.miny <= other.miny and
            self.maxy >= other.maxy
        )

    @contains.register
    def _(self, other: Vec2) -> bool:
        return (
            self.minx <= other.x <= self.maxx and
            self.miny <= other.y <= self.maxy
        )


class BezierPoint:
    def __init__(self, pos: Vec2, control1: Vec2 = None, control2: Vec2 = None):
        self.pos = pos
        self.control1 = control1
        self.control2 = control2

    def translate(self, translation: Vec2):
        self.pos.translate(translation)
        if self.control1:
            self.control1.translate(translation)
        if self.control2:
            self.control2.translate(translation)

    def transform(self, matrix: np.ndarray):
        self.pos.transform(matrix)
        if self.control1:
            self.control1.transform(matrix)
        if self.control2:
            self.control2.transform(matrix)


class BezierContour:
    def __init__(self):
        self.points = []

    def add_point(self, point: BezierPoint):
        self.points.append(point)

    def transform(self, matrix: np.ndarray):
        for point in self.points:
            point.pos.transform(matrix)
            if point.control1:
                point.control1.transform(matrix)
            if point.control2:
                point.control2.transform(matrix)

    def translate(self, translation: Vec2):
        for point in self.points:
            point.pos.translate(translation)
            if point.control1:
                point.control1.translate(translation)
            if point.control2:
                point.control2.translate(translation)

    def contains(self, point: Vec2) -> bool:
        # ray-casting algorithm
        intersections = 0
        y = point.y

        for i in range(len(self.points) - 1):
            start = self.points[i].pos
            end = self.points[i + 1].pos

            if (start.y <= y < end.y) or (start.y >= y > end.y):
                if start.x == end.x and start.y == end.y:
                    continue

                x = (y - start.y) * (end.x - start.x) / \
                    (end.y - start.y) + start.x

                if x == point.x:
                    return True

                if x < point.x:
                    intersections += 1

        return intersections % 2 == 1


class BezierPath:
    def __init__(self):
        self.contours = []

    def add_contour(self, contour: BezierContour):
        self.contours.append(contour)

    def bounds(self) -> Rect:
        minx = float('inf')
        miny = float('inf')
        maxx = float('-inf')
        maxy = float('-inf')

        for contour in self.contours:
            for point in contour.points:
                x0, y0 = point.pos.x, point.pos.y
                x1, y1 = point.control1.x, point.control1.y
                x2, y2 = point.control2.x, point.control2.y
                x3, y3 = point.pos.x, point.pos.y

                a = x3 - 3 * x2 + 3 * x1 - x0
                b = 2 * (x2 - 2 * x1 + x0)
                c = x1 - x0

                # Compute t values where dx/dt = 0
                discriminant = b * b - 4 * a * c
                if discriminant >= 0:
                    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
                    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
                    t_values = [t for t in [t1, t2] if 0 <= t <= 1]
                else:
                    t_values = []

                # Evaluate x-coordinate at t values and update bounds
                for t in t_values:
                    xt = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t ** 2 * x2
                    if xt < minx:
                        minx = xt
                    if xt > maxx:
                        maxx = xt

                # Evaluate y-coordinate at t values and update bounds
                for t in t_values:
                    yt = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t ** 2 * y2
                    if yt < miny:
                        miny = yt
                    if yt > maxy:
                        maxy = yt

        return Rect(minx, miny, maxx, maxy)

    def transform(self, matrix: np.ndarray):
        for contour in self.contours:
            contour.transform(matrix)

    def translate(self, translation: Vec2):
        for contour in self.contours:
            contour.translate(translation)

    def contains(self, point: Vec2) -> bool:
        # Iterate over each contour
        for contour in self.contours:
            # Check if the point is inside the contour using the ray casting algorithm
            if self._is_point_inside_contour(point, contour):
                return True

        return False

    def _is_point_inside_contour(self, point: Vec2, contour: BezierContour) -> bool:
        # Create a horizontal ray extending to the right from the test point
        ray = LineString([point.to_tuple(), (point.x + 1, point.y)])

        # Iterate over each curve segment
        intersections = 0
        for i in range(len(contour.points) - 1):
            start = contour.points[i].pos
            end = contour.points[i + 1].pos
            control1 = contour.points[i].control2
            control2 = contour.points[i + 1].control1

            # Create a cubic bezier curve using Shapely
            curve = LineString(
                [start.to_tuple(), control1.to_tuple(), control2.to_tuple(), end.to_tuple()])

            # Check if the ray intersects with the curve
            if curve.intersects(ray):
                intersections += 1

        # If the number of intersections is odd, the point is inside the contour
        return intersections % 2 == 1


class BezierPathA:
    def __init__(self):
        self.paths = []

    def bounds(self) -> Rect:
        accum = Rect(float('inf'), float('inf'), float('-inf'), float('-inf'))
        for path in self.paths:
            accum += path.bounds()

        return accum

    def scale(self, factor: float):
        scale_matrix = np.array([[factor, 0, 0], [0, factor, 0], [0, 0, 1]])
        for path in self.paths:
            path.transform(scale_matrix)

    def transform(self, matrix: np.ndarray):
        for path in self.paths:
            path.transform(matrix)

    def translate(self, translation: Vec2):
        for path in self.paths:
            path.translate(translation)
