"""Kit part: Locker (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, shade, INK

__all__ = ["Locker"]


class Locker(KitFurniture):
    W, H, NAME = 40, 100, "locker"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.tone((80, 120, 150)), r)
        for y in range(r.top + 8, r.top + 30, 6):                         # vents
            pygame.draw.line(surf, shade((80, 120, 150), 0.6), (r.left + 8, y), (r.right - 8, y), 2)
        pygame.draw.rect(surf, (210, 210, 210), (r.right - 10, r.centery - 6, 4, 12))
        pygame.draw.rect(surf, INK, r, 2)

