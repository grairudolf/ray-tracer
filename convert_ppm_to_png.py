#!/usr/bin/env python3
"""convert_ppm_to_png.py

Simple helper to convert an ASCII PPM (P3) file produced by this renderer
into a PNG using Pillow.

Usage: python convert_ppm_to_png.py render.ppm render.png
"""
import sys

try:
    from PIL import Image
except Exception as e:
    print("Pillow is required to run this script. Install with: pip install Pillow")
    raise


def read_ppm_ascii(path):
    with open(path, 'r', encoding='utf8') as f:
        # Read header (magic number)
        magic = f.readline().strip()
        if magic != 'P3':
            raise ValueError('Only ASCII PPM (P3) supported')

        tokens = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens.extend(line.split())

    if len(tokens) < 3:
        raise ValueError('PPM header incomplete')

    width = int(tokens[0])
    height = int(tokens[1])
    maxval = int(tokens[2])
    vals = list(map(int, tokens[3:]))

    expected = width * height * 3
    if len(vals) < expected:
        raise ValueError(f'PPM does not contain enough pixel data: {len(vals)} < {expected}')

    # Normalize to 0-255
    if maxval == 255:
        raw = bytes(vals[:expected])
    else:
        scale = 255.0 / maxval
        raw = bytes(int(v * scale + 0.5) for v in vals[:expected])

    return width, height, raw


def main():
    if len(sys.argv) < 3:
        print('Usage: python convert_ppm_to_png.py input.ppm output.png')
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]

    w, h, raw = read_ppm_ascii(inp)
    img = Image.frombytes('RGB', (w, h), raw)
    img.save(out)
    print(f'Wrote {out} ({w}x{h})')


if __name__ == '__main__':
    main()
