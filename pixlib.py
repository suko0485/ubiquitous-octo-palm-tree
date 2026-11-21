"""Mini librería de pixel-art sin dependencias (solo stdlib)."""
import zlib, struct, math

class Img:
    def __init__(self, w=32, h=32):
        self.w, self.h = w, h
        self.p = [[(0, 0, 0, 0)] * w for _ in range(h)]
    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y][x] = c if len(c) == 4 else tuple(c) + (255,)
    def get(self, x, y): return self.p[y][x]
    def rect(self, x0, y0, x1, y1, c):  # inclusivo
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): self.px(x, y, c)
    def frame(self, x0, y0, x1, y1, c):
        for x in range(x0, x1 + 1): self.px(x, y0, c); self.px(x, y1, c)
        for y in range(y0, y1 + 1): self.px(x0, y, c); self.px(x1, y, c)
    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
        for i in range(n + 1):
            t = i / n; self.px(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)
    def disc(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.3: self.px(x, y, c)
    def ring(self, cx, cy, r, c, w=1):
        for y in range(int(cy - r - 2), int(cy + r + 3)):
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                d = math.hypot(x - cx, y - cy)
                if r - w < d <= r + 0.4: self.px(x, y, c)
    def poly(self, pts, c):
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            xs = []
            for i in range(len(pts)):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
                if (y0 <= y + .5 < y1) or (y1 <= y + .5 < y0):
                    xs.append(x0 + (y + .5 - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1]))): self.px(x, y, c)
    def save(self, path):
        raw = b"".join(b"\x00" + b"".join(bytes(self.p[y][x]) for x in range(self.w)) for y in range(self.h))
        def ch(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0))
                               + ch(b"IDAT", zlib.compress(raw, 9)) + ch(b"IEND", b""))

def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c[:3])
