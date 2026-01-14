"""Simple 3D vector utilities with physics-friendly names.

This module implements a compact Vec3 class used for positions,
directions, colors, and provides vector operations used throughout
the tracer (dot, cross, normalization, reflection, refraction).
"""
import math
import random


class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # Convenience constructors
    @staticmethod
    def zero():
        return Vec3(0.0, 0.0, 0.0)

    # Basic math operators
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, t):
        # Support both scalar multiplication and component-wise (Hadamard) multiplication
        if isinstance(t, Vec3):
            return Vec3(self.x * t.x, self.y * t.y, self.z * t.z)
        return Vec3(self.x * t, self.y * t, self.z * t)

    __rmul__ = __mul__

    def __truediv__(self, t):
        return self * (1.0 / t)

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    # Vector operations
    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def unit(self):
        return self / self.length()

    # Reflection: r = v - 2*(v·n)*n
    def reflect(self, n):
        return self - n * (2 * self.dot(n))

    # Refraction using Snell's Law. Returns None if total internal reflection occurs.
    def refract(self, n, etai_over_etat):
        # Compute cos(theta) using negative dot because ray directions are outgoing
        cos_theta = min((-self).dot(n), 1.0)
        r_out_perp = (self + n * cos_theta) * etai_over_etat
        # Ensure numerical safety for sqrt
        k = 1.0 - r_out_perp.length_squared()
        if k < 0.0:
            return None
        r_out_parallel = n * (-math.sqrt(k))
        return r_out_perp + r_out_parallel

    # Random sampling helpers
    @staticmethod
    def random(min_val=0.0, max_val=1.0):
        return Vec3(random.uniform(min_val, max_val), random.uniform(min_val, max_val), random.uniform(min_val, max_val))

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random(-1, 1)
            if p.length_squared() >= 1:
                continue
            return p

    @staticmethod
    def random_unit_vector():
        return Vec3.random_in_unit_sphere().unit()

    @staticmethod
    def random_in_hemisphere(normal):
        # Sample uniformly in hemisphere oriented by normal
        in_unit = Vec3.random_in_unit_sphere()
        if in_unit.dot(normal) > 0.0:
            return in_unit
        else:
            return -in_unit

    @staticmethod
    def random_cosine_direction():
        # Cosine-weighted hemisphere sampling useful for Lambertian diffuse
        r1 = random.random()
        r2 = random.random()
        z = math.sqrt(1 - r2)
        phi = 2 * math.pi * r1
        x = math.cos(phi) * math.sqrt(r2)
        y = math.sin(phi) * math.sqrt(r2)
        return Vec3(x, y, z)


Color = Vec3
