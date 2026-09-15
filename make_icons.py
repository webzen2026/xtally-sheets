#!/usr/bin/env python3
"""Generate PWA icon set for Xtally Sheets — a grid/table mark on a
teal->emerald gradient rounded-square, distinct from Xtally Documents
(indigo/fuchsia + tally strokes) and from SYNTHLUCIDA's own look."""
from PIL import Image, ImageDraw

# Brand colors
C1 = (13, 148, 136)    # teal-600
C2 = (5, 150, 105)     # emerald-600
WHITE = (255, 255, 255, 255)


def gradient_square(size, radius_ratio=0.22):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = grad.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)  # diagonal gradient
            r = int(C1[0] + (C2[0] - C1[0]) * t)
            g = int(C1[1] + (C2[1] - C1[1]) * t)
            b = int(C1[2] + (C2[2] - C1[2]) * t)
            px[x, y] = (r, g, b, 255)
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    radius = int(size * radius_ratio)
    mdraw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    img.paste(grad, (0, 0), mask)
    return img


def draw_grid_mark(img, scale=1.0, offset=(0, 0)):
    """Draw a rounded-square outer frame with a 3x3 grid of cells (white
    strokes) and the top-left cell filled solid white, evoking a spreadsheet
    with the active/selected cell — centered on the canvas, sized by `scale`
    (1.0 = content fills ~58% of canvas, safe for maskable icons)."""
    size = img.width
    draw = ImageDraw.Draw(img)

    content = size * 0.58 * scale
    cx, cy = size / 2 + offset[0], size / 2 + offset[1]
    left = cx - content / 2
    top = cy - content / 2
    right = left + content
    bottom = top + content

    stroke_w = max(2, content * 0.055)
    frame_radius = content * 0.14

    # Outer frame
    draw.rounded_rectangle([left, top, right, bottom], radius=frame_radius,
                            outline=WHITE, width=int(stroke_w))

    # Grid lines (2 verticals, 2 horizontals -> 3x3 cells)
    col1 = left + content / 3
    col2 = left + content * 2 / 3
    row1 = top + content / 3
    row2 = top + content * 2 / 3

    inset = stroke_w * 0.15
    draw.line([col1, top + inset, col1, bottom - inset], fill=WHITE, width=int(stroke_w * 0.85))
    draw.line([col2, top + inset, col2, bottom - inset], fill=WHITE, width=int(stroke_w * 0.85))
    draw.line([left + inset, row1, right - inset, row1], fill=WHITE, width=int(stroke_w * 0.85))
    draw.line([left + inset, row2, right - inset, row2], fill=WHITE, width=int(stroke_w * 0.85))

    # Fill the top-left cell solid (the "active cell"), inset from the frame
    pad = stroke_w * 0.55
    draw.rounded_rectangle(
        [left + pad, top + pad, col1 - pad * 0.4, row1 - pad * 0.4],
        radius=frame_radius * 0.35, fill=WHITE
    )

    return img


def make_icon(size, filename, maskable=False):
    img = gradient_square(size, radius_ratio=0.0 if maskable else 0.22)
    scale = 0.62 if maskable else 1.0
    draw_grid_mark(img, scale=scale)
    img.save(filename)
    print("wrote", filename, img.size)


if __name__ == "__main__":
    make_icon(512, "icons/icon-512.png")
    make_icon(192, "icons/icon-192.png")
    make_icon(512, "icons/icon-maskable-512.png", maskable=True)
    make_icon(180, "icons/apple-touch-icon.png")
    make_icon(32, "icons/favicon-32.png")
    make_icon(16, "icons/favicon-16.png")

    # og:image (1200x630) — gradient banner with mark + wordmark space
    og = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
    grad = gradient_square(1200, radius_ratio=0)
    og.paste(grad, (0, 0))
    og = og.crop((0, (1200 - 630) // 2, 1200, (1200 - 630) // 2 + 630))
    mark_canvas = Image.new("RGBA", (630, 630), (0, 0, 0, 0))
    draw_grid_mark(mark_canvas, scale=0.75, offset=(0, 0))
    og.paste(mark_canvas, (60, 0), mark_canvas)
    og.convert("RGB").save("icons/og-image.png", quality=92)
    print("wrote icons/og-image.png", og.size)
