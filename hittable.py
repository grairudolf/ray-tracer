"""Hittable objects and ray-sphere intersection.

We compute intersections using the analytic solution of the quadratic
equation for ray-sphere intersection.
"""
from dataclasses import dataclass
from typing import Optional
from vec3 import Vec3


@dataclass
class HitRecord:
    p: Vec3
    normal: Vec3
    t: float
    front_face: bool
    material: object

    def set_face_normal(self, ray_dir: Vec3, outward_normal: Vec3):
        # Determine if the hit was on the outside by checking ray and outward normal
        self.front_face = ray_dir.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable:
    def hit(self, ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        raise NotImplementedError()


class Sphere(Hittable):
    def __init__(self, center: Vec3, radius: float, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min: float, t_max: float):
        # Solve |P(t) - C|^2 = r^2 where P(t) = O + tD
        oc = ray.origin - self.center
        a = ray.direction.length_squared()
        half_b = oc.dot(ray.direction)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return None
        sqrtd = discriminant ** 0.5

        # Find the nearest root in acceptable range
        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return None

        p = ray.at(root)
        outward_normal = (p - self.center) / self.radius
        rec = HitRecord(p=p, normal=outward_normal, t=root, front_face=True, material=self.material)
        rec.set_face_normal(ray.direction, outward_normal)
        return rec
