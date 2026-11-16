"""Kit part: FilingCabinet (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["FilingCabinet"]


class FilingCabinet(KitFurniture):
    W, H, NAME = 50, 80, "filing cabinet"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.tone((150, 150, 140)), r)
        for k in range(3):
            d = pygame.Rect(r.left + 4, r.top + 4 + k * (r.h - 8) // 3, r.w - 8, (r.h - 8) // 3 - 3)
            pygame.draw.rect(surf, INK, d, 1)
            pygame.draw.rect(surf, (60, 60, 60), (d.centerx - 6, d.top + 5, 12, 3))
        pygame.draw.rect(surf, INK, r, 2)

