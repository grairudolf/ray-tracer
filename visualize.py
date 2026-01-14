"""Simple visualization utilities for rendered images.

This script loads a PNG or PPM image produced by the renderer, computes
luminance for each pixel, and plots a histogram of luminance values using
Matplotlib. It saves the histogram as a PNG.
"""
import argparse
import math
import sys

try:
    from PIL import Image
except Exception:
    Image = None

import matplotlib.pyplot as plt


def load_image(path):
    if path.lower().endswith('.ppm'):
        # Simple PPM (P3) parser
        with open(path, 'r') as f:
            header = f.readline().strip()
            if header != 'P3':
                raise RuntimeError('Only ASCII PPM (P3) supported')
            dims = ''
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue
                dims = line
                break
            width, height = map(int, dims.split())
            maxval = int(f.readline().strip())
            data = []
            for token in f.read().split():
                data.append(int(token))
            pixels = []
            for i in range(0, len(data), 3):
                pixels.append((data[i], data[i+1], data[i+2]))
            return width, height, pixels
    else:
        if Image is None:
            raise RuntimeError('Pillow is required to load PNG/JPEG images')
        img = Image.open(path).convert('RGB')
        pixels = list(img.getdata())
        return img.width, img.height, pixels


def rgb_to_luminance(rgb):
    # Convert sRGB-ish 8-bit per channel to linear luminance approximation
    r, g, b = [c / 255.0 for c in rgb]
    # Inverse gamma to approximate linear light (assume gamma 2.2)
    r_lin = pow(r, 2.2)
    g_lin = pow(g, 2.2)
    b_lin = pow(b, 2.2)
    # Rec. 709 luma coefficients
    lum = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
    return lum


def plot_luminance_hist(pixels, out_path, bins=50):
    lums = [rgb_to_luminance(px) for px in pixels]
    plt.figure(figsize=(6, 4))
    plt.hist(lums, bins=bins, color='gray', edgecolor='black')
    plt.xlabel('Luminance (linear)')
    plt.ylabel('Pixel count')
    plt.title('Luminance Histogram')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Input image (PNG or PPM)')
    parser.add_argument('--out', '-o', default='luminance_hist.png', help='Output histogram PNG')
    parser.add_argument('--bins', type=int, default=50, help='Histogram bins')
    args = parser.parse_args()
    w, h, pixels = load_image(args.input)
    print(f'Loaded image {args.input} ({w}x{h}) with {len(pixels)} pixels')
    plot_luminance_hist(pixels, args.out, bins=args.bins)
    print(f'Wrote histogram to {args.out}')


if __name__ == '__main__':
    main()
