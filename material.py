"""Materials implement scattering behaviour for rays.

Lambertian: diffuse with cosine-weighted scattering (physically plausible).
Metal: specular reflection with optional roughness (fuzz).
Dielectric: refraction using Snell's Law, handling total internal reflection
and Fresnel reflectance via the Schlick approximation.
"""
import math
import random
from vec3 import Vec3


def schlick(cosine, ref_idx):
    # Schlick approximation for Fresnel reflectance
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * ((1 - cosine) ** 5)


class Material:
    def scatter(self, ray_in, hit_rec):
        # Returns (scattered_ray, attenuation_color) or (None, None) if absorbed
        raise NotImplementedError()


class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def scatter(self, ray_in, hit_rec):
        # Cosine-weighted scattering using a local tangent space transform.
        # We generate a direction in the hemisphere with cosine weighting,
        # then transform it so the "z" axis aligns with the hit normal.
        target = Vec3.random_cosine_direction()

        # Build orthonormal basis (u,v,w) with w=normal
        w = hit_rec.normal
        # Choose a vector not parallel to w for stable basis construction
        a = Vec3(0, 1, 0) if abs(w.x) > 0.9 else Vec3(1, 0, 0)
        v = w.cross(a)
        # If v is tiny (numerical edge-case) pick another helper
        if v.length_squared() < 1e-8:
            a = Vec3(1, 0, 0)
            v = w.cross(a)
        v = v.unit()
        u = v.cross(w)

        # Map local sample to world
        scatter_dir = (u * target.x) + (v * target.y) + (w * target.z)

        scattered = ray_in.__class__(hit_rec.p, scatter_dir.unit())
        attenuation = self.albedo
        return scattered, attenuation


class Metal(Material):
    def __init__(self, albedo: Vec3, fuzz: float = 0.0):
        self.albedo = albedo
        self.fuzz = max(0.0, min(fuzz, 1.0))

    def scatter(self, ray_in, hit_rec):
        reflected = ray_in.direction.unit().reflect(hit_rec.normal)
        scattered_dir = reflected + Vec3.random_in_unit_sphere() * self.fuzz
        scattered = ray_in.__class__(hit_rec.p, scattered_dir)
        if scattered.direction.dot(hit_rec.normal) > 0:
            return scattered, self.albedo
        return None, None


class Dielectric(Material):
    def __init__(self, index_of_refraction: float):
        self.ir = index_of_refraction

    def scatter(self, ray_in, hit_rec):
        attenuation = Vec3(1.0, 1.0, 1.0)  # Dielectrics do not absorb (ideal)
        etai_over_etat = (1.0 / self.ir) if hit_rec.front_face else self.ir

        unit_direction = ray_in.direction.unit()
        # Try to refract using Snell's Law
        refracted = unit_direction.refract(hit_rec.normal, etai_over_etat)

        # Decide reflection vs refraction via Schlick approximation
        cos_theta = min((-unit_direction).dot(hit_rec.normal), 1.0)
        reflect_prob = schlick(cos_theta, self.ir)
        if refracted is None:
            # Total internal reflection
            reflected = unit_direction.reflect(hit_rec.normal)
            scattered = ray_in.__class__(hit_rec.p, reflected)
            return scattered, attenuation
        else:
            if random.random() < reflect_prob:
                reflected = unit_direction.reflect(hit_rec.normal)
                scattered = ray_in.__class__(hit_rec.p, reflected)
                return scattered, attenuation
            else:
                scattered = ray_in.__class__(hit_rec.p, refracted)
                return scattered, attenuation
