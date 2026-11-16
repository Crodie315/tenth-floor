"""Kit part: Crusher (hazard). Its owner is listed in OWNERS.md."""
import pygame

from .. import config as C
from ._base import INK

__all__ = ["Crusher"]


class Crusher:
    """A block on a piston: waits up high, slams down, waits, rises slowly. Touching it costs you.

    x, w: where it is. y_top: its top when raised. y_bottom: the surface it slams onto (C.FLOOR_Y or a ledge).
    h: how tall the block is. offset: seconds into its cycle, so two crushers can take turns.
    """

    WAIT_UP, DROP, WAIT_DOWN, RISE = 1.6, 0.18, 0.6, 1.0

    def __init__(self, x, y_top, y_bottom=C.FLOOR_Y, w=60, h=50, offset=0.0):
        self.x, self.w, self.h = int(x), int(w), int(h)
        self.y_top, self.y_bottom = int(y_top), int(y_bottom)
        self.t = offset
        self.y = float(self.y_top)
        self.rect = pygame.Rect(self.x, self.y_top, self.w, self.h)

    def update(self, dt, room, player):
        cycle = self.WAIT_UP + self.DROP + self.WAIT_DOWN + self.RISE
        self.t = (self.t + dt) % cycle
        t, low = self.t, self.y_bottom - self.h
        if t < self.WAIT_UP:
            self.y = self.y_top
        elif t < self.WAIT_UP + self.DROP:
            self.y = self.y_top + (low - self.y_top) * (t - self.WAIT_UP) / self.DROP
        elif t < self.WAIT_UP + self.DROP + self.WAIT_DOWN:
            self.y = low
        else:
            k = (t - self.WAIT_UP - self.DROP - self.WAIT_DOWN) / self.RISE
            self.y = low + (self.y_top - low) * k
        self.rect.y = int(self.y)

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, (90, 92, 100), (r.centerx - 5, self.y_top - 40, 10, r.top - self.y_top + 40))
        pygame.draw.rect(surf, (120, 70, 60), r)
        for x in range(r.left, r.right, 12):                              # hazard stripes
            pygame.draw.line(surf, (240, 200, 60), (x, r.bottom - 2), (x + 8, r.bottom - 10), 3)
        pygame.draw.rect(surf, INK, r, 2)

