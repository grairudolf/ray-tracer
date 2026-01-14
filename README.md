
# Simple Physically-Based Ray Tracer (Python)

This repository contains a compact, educational physically-based ray tracer
implemented in pure Python. It's intentionally focused on mathematical
correctness and clarity rather than performance.

Contents
- `vec3.py`: vector math utilities (Vec3) with reflection/refraction helpers
- `ray.py`: Ray class (origin + direction * t)
- `hittable.py`: `Sphere` and intersection math
- `hittable_list.py`: scene object container
- `material.py`: `Lambertian`, `Metal`, `Dielectric` (Snell + Schlick)
- `camera.py`: perspective camera with `lookfrom`, `lookat`, `vup`, and FOV
- `scene.py`: simple demo scene builder and point-light container
- `main.py`: renderer and CLI driver (writes PPM, optionally PNG)

Features
- Perspective camera with configurable field of view
- Correct ray-sphere intersection and surface normals
- Lambertian diffuse using cosine-weighted hemisphere sampling
- Metallic reflection with adjustable roughness (fuzz)
- Dielectric materials using Snell's Law, total internal reflection,
    and Fresnel via the Schlick approximation
- Point lights with shadow rays for direct illumination
- Recursive path tracing-style indirect lighting (depth-limited)
- Multisample anti-aliasing and gamma correction

Quick start

1. (Optional) install Pillow for PNG output:

```powershell
pip install Pillow
```

2. Run the renderer (quick default settings):

```powershell
C:\Users\Rudolf\AppData\Local\Programs\Python\Python314\python.exe C:\workspace\main.py
```

This writes `render.ppm` and, if Pillow is installed, `render.png`.

CLI options
- `--width`: image width in pixels (default 200)
- `--samples`: samples per pixel (default 20)
- `--depth`: max ray bounce depth (default 10)
- `--out`: output file prefix (default `render` → `render.ppm` / `render.png`)

Notes on the implementation
- Diffuse (Lambertian) scattering uses cosine-weighted hemisphere sampling for
    physically-plausible energy distribution (importance sampling).
- Metal reflection is implemented by reflecting the incoming ray about the
    surface normal, with a small random ``fuzz`` term to simulate roughness.
- Dielectric materials compute refraction using Snell's Law. When refraction is
    not possible (total internal reflection), the ray is reflected. Fresnel
    reflectance is approximated using the Schlick approximation.

Extending the tracer
- Add more geometry types by implementing the `Hittable` interface
- Add textured materials by modulating albedo per-surface point
- Replace the point-light model with an emissive area light for softer shadows

Virtual environment and installation

1. Create project folder and venv (example on Windows PowerShell):

```powershell
mkdir C:\Users\<you>\Desktop\projects\ray-traycer
robocopy C:\workspace C:\Users\<you>\Desktop\projects\ray-traycer /MIR
C:\path\to\python.exe -m venv C:\Users\<you>\Desktop\projects\ray-traycer\.venv
C:\Users\<you>\Desktop\projects\ray-traycer\.venv\Scripts\python.exe -m pip install -r C:\Users\<you>\Desktop\projects\ray-traycer\requirements.txt
```

2. Run the renderer inside the venv:

```powershell
C:\Users\<you>\Desktop\projects\ray-traycer\.venv\Scripts\python.exe main.py --width 400 --samples 50 --depth 10 --out my_render
```

Visualization

Use the included `visualize.py` to produce a luminance histogram from the rendered image. Example:

```powershell
C:\Users\<you>\Desktop\projects\ray-traycer\.venv\Scripts\python.exe visualize.py --input my_render.png --out lum_hist.png
```

The script accepts PNG (preferred) or ASCII PPM (`.ppm`) as input and writes a PNG histogram.

License
This code is provided for educational purposes—no license is included.

