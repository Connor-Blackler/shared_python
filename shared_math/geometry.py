from __future__ import annotations


class vec2():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: vec2):
        x = self.x + other.x
        y = self.y + other.y
        return vec2(x, y)

    def translate(self, other: vec2):
        self.x = self.x + other.x
        self.y = self.y + other.y
