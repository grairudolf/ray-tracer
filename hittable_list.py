"""Container for multiple hittable objects."""
from typing import List, Optional
from hittable import Hittable, HitRecord


class HittableList(Hittable):
    def __init__(self):
        self.objects: List[Hittable] = []

    def add(self, obj: Hittable):
        self.objects.append(obj)

    def clear(self):
        self.objects = []

    def hit(self, ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        hit_anything = None
        closest_so_far = t_max
        for obj in self.objects:
            rec = obj.hit(ray, t_min, closest_so_far)
            if rec:
                closest_so_far = rec.t
                hit_anything = rec
        return hit_anything
