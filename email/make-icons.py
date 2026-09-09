from PIL import Image, ImageDraw, ImageFont
import os

NAVY = (15, 38, 71, 255)
WHITE = (255, 255, 255, 255)
S = 8                      # supersample factor
OUT = "email"
os.makedirs(OUT, exist_ok=True)

def canvas(size):
    return Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))

def finish(img, size, name):
    img = img.resize((size, size), Image.LANCZOS)
    # flatten onto white so clients that ignore alpha still look right
    flat = Image.new("RGB", (size, size), (255, 255, 255))
    flat.paste(img, (0, 0), img)
    flat.save(os.path.join(OUT, name), "PNG", optimize=True)
    print(name, f"{size}x{size}", os.path.getsize(os.path.join(OUT, name)), "bytes")

# ---------- LinkedIn: navy circle, white "in" ----------
SIZE = 96
img = canvas(SIZE)
d = ImageDraw.Draw(img)
D = SIZE * S
d.ellipse([0, 0, D - 1, D - 1], fill=NAVY)

# "i" stem + dot, and "n", drawn as primitives so it stays crisp at any size
u = D / 96.0                      # one design unit == 1px at final size
stem_w = 9 * u
left_x = 28 * u
body_top = 43 * u
body_bot = 71 * u
# i stem
d.rounded_rectangle([left_x, body_top, left_x + stem_w, body_bot], radius=1.5 * u, fill=WHITE)
# i dot
dot_r = 5.6 * u
dot_cx, dot_cy = left_x + stem_w / 2, 32 * u
d.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=WHITE)
# n stem
n_x = 47 * u
d.rounded_rectangle([n_x, body_top, n_x + stem_w, body_bot], radius=1.5 * u, fill=WHITE)
# n shoulder + right leg
r_x = 60 * u
d.rounded_rectangle([r_x, 52 * u, r_x + stem_w, body_bot], radius=1.5 * u, fill=WHITE)
# arch joining the two legs
d.pieslice([n_x, body_top, r_x + stem_w, body_top + 2 * (52 * u - body_top)],
           180, 360, fill=WHITE)
d.pieslice([n_x + stem_w, body_top + stem_w,
            r_x, body_top + stem_w + 2 * (52 * u - body_top - stem_w)],
           180, 360, fill=NAVY)
finish(img, SIZE, "icon-linkedin.png")

# ---------- Website: navy circle, white globe ----------
img = canvas(SIZE)
d = ImageDraw.Draw(img)
d.ellipse([0, 0, D - 1, D - 1], fill=NAVY)
u = D / 96.0
lw = int(round(4.0 * u))
cx = cy = D / 2
r = 26 * u
# outline
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=lw)
# equator
d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=lw)
# meridian (narrow ellipse)
mw = 11 * u
d.ellipse([cx - mw, cy - r, cx + mw, cy + r], outline=WHITE, width=lw)
# two latitude arcs
for sign in (-1, 1):
    off = 13 * u * sign
    d.arc([cx - r, cy + off - 11 * u, cx + r, cy + off + 11 * u],
          0 if sign < 0 else 180, 180 if sign < 0 else 360, fill=WHITE, width=lw)
finish(img, SIZE, "icon-website.png")
