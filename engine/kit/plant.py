"""Kit part: Plant (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, shade, INK

__all__ = ["Plant"]


class Plant(KitFurniture):
    W, H, NAME = 44, 80, "plant"

    def draw(self, surf):
        r = self.rect
        pot = pygame.Rect(r.left + 8, r.bottom - 26, r.w - 16, 26)
        leaf = self.tone((70, 140, 80))
        for k, (dx, dy) in enumerate(((-14, -40), (12, -46), (0, -56), (-8, -24), (14, -22))):
            pygame.draw.ellipse(surf, shade(leaf, 0.85 + 0.05 * k), (r.centerx + dx - 10, pot.top + dy, 22, 30))
        pygame.draw.rect(surf, self.tone((180, 100, 60)), pot)
        pygame.draw.rect(surf, INK, pot, 2)

