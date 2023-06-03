from __future__ import annotations
import numpy as np
from shapely.geometry import Point, LineString


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Vec2):
        x = self.x + other.x
        y = self.y + other.y
        return Vec2(x, y)

    def __sub__(self, other: Vec2):
        x = self.x - other.x
        y = self.y - other.y
        return Vec2(x, y)

    def to_tuple(self):
        return self.x, self.y

    def translate(self, other: Vec2):
        self.x += other.x
        self.y += other.y

    def l2_norm(self) -> float:
        """||X||2
        Measures simple distance from origin (Euclidean length)"""
        return (self.x**2 + self.y**2)**(1/2)

    def l2_norm_squared(self) -> float:
        """||X||2/2
        computationally cheaper then l2_norm
        """
        return (self.x**2 + self.y**2)

    def l1_norm(self) -> float:
        """L1 Norm"""
        return (abs(self.x) + abs(self.y))

    def max_norm(self) -> float:
        """ ||x||8
        max Norm
        """
        return max(abs(self.x), abs(self.y))

    def normalize(self) -> Vec2:
        current_len = self.l2_norm()
        if current_len == 0:
            return Vec2(0.0, 0.0)

        return Vec2(self.x / current_len, self.y / current_len)

    def transform(self, matrix: np.ndarray):
        vector = np.array([self.x, self.y, 1])
        transformed_vector = vector @ matrix.T

        self.x = transformed_vector[0]
        self.y = transformed_vector[1]

    def __str__(self):
        return f"Vec2(x={self.x}, y={self.y})"


class Rect:
    def __init__(self, minx: float, miny: float, maxx: float, maxy: float):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def width(self):
        return abs(self.maxx - self.minx)

    def height(self):
        return abs(self.maxy - self.miny)

    def __add__(self, other: Rect):
        minx = min(self.minx, other.minx)
        miny = min(self.miny, other.miny)
        maxx = max(self.maxx, other.maxx)
        maxy = max(self.maxy, other.maxy)
        return Rect(minx, miny, maxx, maxy)

    def translate(self, translation: Vec2):
        self.minx += translation.x
        self.miny += translation.y
        self.maxx += translation.x
        self.maxy += translation.y

    def transform(self, matrix: np.ndarray):
        corners = np.array([[self.minx, self.miny, 1], [self.minx, self.maxy, 1],
                            [self.maxx, self.miny, 1], [self.maxx, self.maxy, 1]])
        transformed_corners = corners @ matrix.T
        self.minx = np.min(transformed_corners[:, 0])
        self.miny = np.min(transformed_corners[:, 1])
        self.maxx = np.max(transformed_corners[:, 0])
        self.maxy = np.max(transformed_corners[:, 1])

    def contains(self, other):
        if isinstance(other, Rect):
            return (
                self.minx <= other.minx and
                self.maxx >= other.maxx and
                self.miny <= other.miny and
                self.maxy >= other.maxy
            )
        elif isinstance(other, Vec2):
            return (
                self.minx <= other.x <= self.maxx and
                self.miny <= other.y <= self.maxy
            )

    def __str__(self):
        return f"Rect(minx={self.minx}, miny={self.miny}, maxx={self.maxx}, maxy={self.maxy})"


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

    def __str__(self):
        if self.control1 and self.control2:
            return f"BezierPoint(pos={self.pos}, control1={self.control1}, control2={self.control2})"
        elif self.control1:
            return f"BezierPoint(pos={self.pos}, control1={self.control1})"
        else:
            return f"BezierPoint(pos={self.pos})"


class BezierContour:
    def __init__(self, closed: bool = True):
        self.points = []
        self.closed = closed

    def add_point(self, point: BezierPoint):
        self.points.append(point)

    def transform(self, matrix: np.ndarray):
        for point in self.points:
            point.transform(matrix)

    def translate(self, translation: Vec2):
        for point in self.points:
            point.translate(translation)

    def contains(self, point: Vec2):
        for i in range(len(self.points) - 1):
            start = self.points[i].pos
            end = self.points[i + 1].pos
            control1 = self.points[i].control2
            control2 = self.points[i + 1].control1

            if control1 and control2:
                curve = LineString(
                    [start.to_tuple(), control1.to_tuple(), control2.to_tuple(), end.to_tuple()])
            else:
                curve = LineString([start.to_tuple(), end.to_tuple()])

            if curve.contains(Point(point.x, point.y)):
                return True

        return False

    def __str__(self):
        points_str = "\n".join(str(point) for point in self.points)
        return f"BezierContour(points=[\n{points_str}\n])"


class BezierPath:
    def __init__(self):
        self.contours = []

    def add_contour(self, contour: BezierContour):
        self.contours.append(contour)

    def bounds(self):
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

    def contains(self, point: Vec2):
        for contour in self.contours:
            if contour.contains(point):
                return True

        return False

    def __str__(self):
        contours_str = "\n".join(str(contour) for contour in self.contours)
        return f"BezierPath(contours=[\n{contours_str}\n])"


class BezierPathA:
    def __init__(self):
        self.paths = []
        self.__iter = 0

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter < len(self.paths):
            ret = self.paths[self.__iter]
            self.__iter += 1
            return ret
        else:
            raise StopIteration

    def bounds(self):
        accum = Rect(float('inf'), float('inf'), float('-inf'), float('-inf'))
        for path in self.paths:
            accum += path.bounds()

        return accum

    def contains(self, point: Vec2):
        for path in self.paths:
            if path.contains(point):
                return True

        return False

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

    def __str__(self):
        contours_str = "\n".join(str(contour) for contour in self.paths)
        return f"BezierPathA(paths=[\n{contours_str}\n])"
