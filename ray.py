"""Ray class: origin + direction*t
"""
from vec3 import Vec3


class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction

    def at(self, t: float):
        return self.origin + self.direction * t
