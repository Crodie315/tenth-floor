"""Kit part: Printer3D (furniture). Its owner is listed in OWNERS.md."""
import math

import pygame

from ._base import KitFurniture, INK

__all__ = ["Printer3D"]


class Printer3D(KitFurniture):
    W, H, NAME = 70, 80, "3D printer"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.tone((60, 62, 70)), r, border_radius=3)
        win = r.inflate(-14, -24).move(0, -2)
        pygame.draw.rect(surf, (24, 26, 32), win)
        t = pygame.time.get_ticks() / 1000.0
        nx = win.left + 6 + int((math.sin(t * 2 + r.x) + 1) / 2 * (win.w - 12))
        pygame.draw.line(surf, (160, 160, 170), (win.left, win.top + 8), (win.right, win.top + 8), 2)
        pygame.draw.rect(surf, (200, 200, 210), (nx - 4, win.top + 6, 8, 8))
        pygame.draw.rect(surf, self.tone((230, 140, 60)), (win.centerx - 12, win.bottom - 10, 24, 10))   # the print
        pygame.draw.rect(surf, INK, r, 2, border_radius=3)

