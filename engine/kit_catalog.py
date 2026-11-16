"""Draws every part in engine/kit/, labelled, into docs/kit.png (the picture in KIT.md).

    python -m engine.kit_catalog
"""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame  # noqa: E402

from . import config as C, kit  # noqa: E402

CELL_W, CELL_H, COLS = 240, 210, 6

PARTS = [
    ("Desk", lambda x, y: kit.Desk(x - 55, y)), ("Bookshelf", lambda x, y: kit.Bookshelf(x - 35, y)),
    ("Locker", lambda x, y: kit.Locker(x - 20, y)), ("FilingCabinet", lambda x, y: kit.FilingCabinet(x - 25, y)),
    ("ServerRack", lambda x, y: kit.ServerRack(x - 25, y)), ("Printer3D", lambda x, y: kit.Printer3D(x - 35, y)),
    ("Easel", lambda x, y: kit.Easel(x - 30, y)), ("Couch", lambda x, y: kit.Couch(x - 65, y)),
    ("Plant", lambda x, y: kit.Plant(x - 22, y)), ("VendingMachine", lambda x, y: kit.VendingMachine(x - 35, y)),
    ("Plinth", lambda x, y: kit.Plinth(x - 35, y)),
    ("PatrolBot", lambda x, y: kit.PatrolBot(x - 17, y, left=x - 60, right=x + 60)),
    ("Zapper (on)", lambda x, y: _on(kit.Zapper(x, y_top=y - 120, y_bottom=y, on_time=5, off_time=1))),
    ("Crusher", lambda x, y: _at(kit.Crusher(x - 30, y_top=y - 150, y_bottom=y), 1.7)),
    ("Drone", lambda x, y: kit.Drone(x - 18, y_top=y - 120, y_bottom=y - 40)),
    ("FloorLaser (on)", lambda x, y: _on(kit.FloorLaser(x - 80, x + 80, y, on_time=5, off_time=1))),
    ("MovingPlatform", lambda x, y: kit.MovingPlatform(x - 55, x - 55, y - 60, width=110)),
    ("Window", lambda x, y: kit.Window(x - 70, y - 140)), ("Poster", lambda x, y: kit.Poster(x - 35, y - 130, "SVA")),
    ("Sign", lambda x, y: kit.Sign(x - 80, y - 90, "FABRICATION LAB", size=26)),
    ("CeilingLight", None),
]


def _on(h):
    h.update(0.01, None, None)
    return h


def _at(h, t):
    h.update(t, None, None)
    return h


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    rows = (len(PARTS) + COLS - 1) // COLS
    img = pygame.Surface((COLS * CELL_W, rows * CELL_H))
    img.fill(C.WALL)
    font = pygame.font.Font(None, 26)
    for k, (label, make) in enumerate(PARTS):
        cx = (k % COLS) * CELL_W + CELL_W // 2
        top = (k // COLS) * CELL_H
        floor_y = top + CELL_H - 40
        cell = pygame.Rect(cx - CELL_W // 2, top, CELL_W, CELL_H)
        img.set_clip(cell)
        pygame.draw.rect(img, (54, 56, 64), (cell.left, floor_y, CELL_W, CELL_H))
        if label == "CeilingLight":        # it hangs from the top of the room, so draw it in the cell's own frame
            kit.CeilingLight(CELL_W // 2, cord=10, reach=120).draw(img.subsurface(cell))
        else:
            make(cx, floor_y).draw(img)
        img.set_clip(None)
        pygame.draw.rect(img, (40, 42, 52), cell, 1)
        t = font.render(label, True, (235, 235, 240))
        img.blit(t, (cx - t.get_width() // 2, floor_y + 10))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "kit.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pygame.image.save(img, out)
    print("wrote", out)


if __name__ == "__main__":
    main()
