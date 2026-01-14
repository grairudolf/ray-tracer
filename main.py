""" Small physically-based ray tracer demo.

Run `python main.py` to render a small image (PPM) to `render.ppm`.
"""
import sys
import math
import random
import argparse
from vec3 import Color, Vec3
from ray import Ray
from hittable_list import HittableList
from camera import Camera
from scene import simple_scene
from material import Material

# Optional PNG output if Pillow is installed
try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False


def color_to_ints(pixel_color: Color, samples_per_pixel: int, gamma: float = 2.2):
    # Convert a linear color to 8-bit per channel integers with gamma correction
    scale = 1.0 / samples_per_pixel
    r = max(0.0, pixel_color.x * scale)
    g = max(0.0, pixel_color.y * scale)
    b = max(0.0, pixel_color.z * scale)

    # Gamma correction (convert from linear to sRGB-like)
    r = pow(r, 1.0 / gamma)
    g = pow(g, 1.0 / gamma)
    b = pow(b, 1.0 / gamma)

    ir = int(256 * max(0.0, min(0.999, r)))
    ig = int(256 * max(0.0, min(0.999, g)))
    ib = int(256 * max(0.0, min(0.999, b)))
    return ir, ig, ib


def hit_world(ray, world, t_min, t_max):
    return world.hit(ray, t_min, t_max)


def ray_color(ray, world, lights, depth):
    # Recursive ray tracing with a depth limit
    if depth <= 0:
        return Color(0, 0, 0)

    rec = hit_world(ray, world, 0.001, float('inf'))
    if rec is None:
        # Background (simple gradient)
        unit_dir = ray.direction.unit()
        t = 0.5 * (unit_dir.y + 1.0)
        return Color(1.0, 1.0, 1.0) * (1.0 - t) + Color(0.5, 0.7, 1.0) * t

    # Direct illumination from point lights with shadow rays (occlusion)
    direct = Color(0, 0, 0)
    for light in lights:
        to_light = light.position - rec.p
        dist2 = to_light.length_squared()
        to_light_dir = to_light.unit()

        # Shadow ray: if any object blocks the path, the light is occluded
        shadow_ray = Ray(rec.p, to_light_dir)
        shadow_hit = hit_world(shadow_ray, world, 0.001, math.sqrt(dist2) - 0.001)
        if shadow_hit is None:
            # Lambert's cosine law and inverse-square falloff
            n_dot_l = max(0.0, rec.normal.dot(to_light_dir))
            attenuation = light.intensity / dist2
            # If the material has an albedo attribute, use it; otherwise assume white
            albedo = getattr(rec.material, 'albedo', Color(1, 1, 1))
            direct += albedo * attenuation * n_dot_l

    # Indirect light via material scattering
    scattered_info = rec.material.scatter(ray, rec)
    indirect = Color(0, 0, 0)
    if scattered_info is not None:
        scattered, attenuation = scattered_info
        if scattered is not None:
            indirect = attenuation * ray_color(scattered, world, lights, depth - 1)

    return direct + indirect


def render(image_width: int = 2000, samples_per_pixel: int = 20, max_depth: int = 15, out_prefix: str = 'render'):
    # Image
    aspect_ratio = 16.0 / 9.0
    image_height = int(image_width / aspect_ratio)

    # World and lights
    world, lights = simple_scene()

    # Camera
    lookfrom = Vec3(3, 3, 2)
    lookat = Vec3(0, 0, -1)
    vup = Vec3(0, 1, 0)
    vfov = 20.0
    cam = Camera(lookfrom, lookat, vup, vfov, aspect_ratio)

    # Prepare output buffers
    ppm_path = f"{out_prefix}.ppm"
    png_path = f"{out_prefix}.png"
    pixels = [None] * (image_width * image_height)

    # Render loop (store pixels for optional PNG save)
    with open(ppm_path, 'w') as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        idx = 0
        for j in range(image_height - 1, -1, -1):
            print(f"Scanlines remaining: {j}", file=sys.stderr)
            for i in range(image_width):
                pixel_color = Color(0, 0, 0)
                for s in range(samples_per_pixel):
                    u = (i + random.random()) / (image_width - 1)
                    v = (j + random.random()) / (image_height - 1)
                    r = cam.get_ray(u, v)
                    pixel_color += ray_color(r, world, lights, max_depth)
                ir, ig, ib = color_to_ints(pixel_color, samples_per_pixel)
                f.write(f"{ir} {ig} {ib}\n")
                pixels[idx] = (ir, ig, ib)
                idx += 1

    print(f"Done. Wrote {ppm_path}")

    # If Pillow is available, write PNG as well
    if HAVE_PIL:
        img = Image.new('RGB', (image_width, image_height))
        # PPM wrote scanlines from top-to-bottom, our pixels list is in same order
        img.putdata(pixels)
        img.save(png_path)
        print(f"Also wrote {png_path}")
    else:
        print("Pillow not available; skipping PNG output. Install Pillow to enable PNG.")


def parse_args_and_run():
    parser = argparse.ArgumentParser(description='Simple physically-based ray tracer')
    parser.add_argument('--width', type=int, default=2000, help='Image width in pixels')
    parser.add_argument('--samples', type=int, default=20, help='Samples per pixel')
    parser.add_argument('--depth', type=int, default=15, help='Maximum ray bounce depth')
    parser.add_argument('--out', type=str, default='render', help='Output file prefix (render.ppm and render.png)')
    args = parser.parse_args()
    render(image_width=args.width, samples_per_pixel=args.samples, max_depth=args.depth, out_prefix=args.out)


if __name__ == '__main__':
    parse_args_and_run()


if __name__ == '__main__':
    render()
