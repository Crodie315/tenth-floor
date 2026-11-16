"""Kit part: Couch (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, shade, INK

__all__ = ["Couch"]


class Couch(KitFurniture):
    W, H, NAME = 130, 50, "couch"

    def draw(self, surf):
        r = self.rect
        col = self.tone((150, 70, 80))
        pygame.draw.rect(surf, col, (r.left, r.top + 10, r.w, r.h - 16), border_radius=8)
        pygame.draw.rect(surf, shade(col, 0.8), (r.left + 10, r.top, r.w - 20, 22), border_radius=6)
        pygame.draw.rect(surf, INK, (r.left, r.top + 10, r.w, r.h - 16), 2, border_radius=8)
        for x in (r.left + 10, r.right - 16):
            pygame.draw.rect(surf, INK, (x, r.bottom - 6, 6, 6))

