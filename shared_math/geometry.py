from __future__ import annotations
from functools import singledispatchmethod
import numpy as np


class vec2():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: vec2):
        x = self.x + other.x
        y = self.y + other.y
        return vec2(x, y)

    def __sub__(self, other: vec2):
        return vec2(self.x - other.x, self.y - other.y)

    def translate(self, other: vec2):
        self.x = self.x + other.x
        self.y = self.y + other.y

    def transform(self, matrix: np.ndarray):
        vector = np.array([self.x, self.y, 1])
        transformed_vector = vector @ matrix.T

        self.x = transformed_vector[0]
        self.y = transformed_vector[1]


class rect():
    def __init__(self, minx: float, miny: float, maxx: float, maxy: float) -> None:
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def translate(self, translation: vec2):
        self.minx += translation.x
        self.maxx += translation.x
        self.miny += translation.y
        self.maxy += translation.y

    def transform(self, matrix: np.ndarray):
        corners = np.array([
            [self.minx, self.miny, 1],
            [self.minx, self.maxy, 1],
            [self.maxx, self.miny, 1],
            [self.maxx, self.maxy, 1]
        ])

        transformed_corners = corners @ matrix.T

        self.minx = np.min(transformed_corners[:, 0])
        self.maxx = np.max(transformed_corners[:, 0])
        self.miny = np.min(transformed_corners[:, 1])
        self.maxy = np.max(transformed_corners[:, 1])

    @singledispatchmethod
    def contains(self, other: rect) -> bool:
        return (
            self.minx <= other.minx and
            self.maxx >= other.maxx and
            self.miny <= other.miny and
            self.maxy >= other.maxy
        )

    @contains.register
    def _(self, other: vec2) -> bool:
        return (
            self.minx <= other.x <= self.maxx and
            self.miny <= other.y <= self.maxy
        )
