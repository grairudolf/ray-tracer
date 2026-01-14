"""Perspective camera implementation.

Constructs a camera from `lookfrom`, `lookat`, `vup` and vertical field-of-view.
Generates rays through image plane coordinates (s, t) in [0,1].
"""
import math
from vec3 import Vec3
from ray import Ray


class Camera:
    def __init__(self, lookfrom: Vec3, lookat: Vec3, vup: Vec3, vfov: float, aspect_ratio: float):
        # vfov is vertical field-of-view in degrees
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        # Camera basis
        w = (lookfrom - lookat).unit()
        u = vup.cross(w).unit()
        v = w.cross(u)

        self.origin = lookfrom
        self.horizontal = u * viewport_width
        self.vertical = v * viewport_height
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - w

    def get_ray(self, s: float, t: float):
        # Create ray from origin through the image plane point
        direction = (self.lower_left_corner + self.horizontal * s + self.vertical * t) - self.origin
        return Ray(self.origin, direction.unit())
