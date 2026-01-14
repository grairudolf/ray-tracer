"""Scene description and simple point light representation."""
from vec3 import Vec3
from material import Lambertian, Metal, Dielectric
from hittable_list import HittableList
from hittable import Sphere


class PointLight:
    def __init__(self, position: Vec3, intensity: Vec3):
        self.position = position
        self.intensity = intensity


def simple_scene():
    # Create a scene with one diffuse, one metal, one glass sphere and a ground
    world = HittableList()

    material_ground = Lambertian(Vec3(0.8, 0.8, 0.0))
    material_center = Lambertian(Vec3(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_right = Metal(Vec3(0.8, 0.6, 0.2), fuzz=0.0)

    world.add(Sphere(Vec3(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Vec3(0.0, 0.0, -1.0), 0.5, material_center))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), -0.45, material_left))
    world.add(Sphere(Vec3(1.0, 0.0, -1.0), 0.5, material_right))

    # Point light slightly above and to the right
    lights = [PointLight(Vec3(5, 5, -2), Vec3(6.0, 6.0, 6.0))]

    return world, lights
