
from PIL import Image

SRC_DIR = '/home/***/'


def grid(w, h, base_width, frame):
    img = Image.new('1', (w, h), 0)
    for x in range(0, w, base_width * frame):
        for y in range(h):
            for j in range(base_width):
                x_pos = x + base_width * (frame - 1) + j
                if x_pos >= w:
                    break
                img.putpixel((x_pos, y), 1)
    return img


def synthesize(w, h, base, frame, mode=None, fillcolor=None):
    srcs = [Image.open(f'{SRC_DIR}/{i + 1}.png') for i in range(frame)]
    srcs = [s.convert('RGB') for s in srcs]
    img = Image.new(mode or 'RGB', (w, h),
                    fillcolor if fillcolor is not None else (255, 255, 255))
    for x in range(0, w, base):
        for y in range(h):
            for j in range(base):
                x_pos = x + j
                if x_pos >= w:
                    break
                src_idx = (x // base + 1) % frame
                img.putpixel((x_pos, y), srcs[src_idx].getpixel((x_pos, y)))
    return img