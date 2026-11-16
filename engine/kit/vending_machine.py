"""Kit part: VendingMachine (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["VendingMachine"]


class VendingMachine(KitFurniture):
    W, H, NAME = 70, 120, "vending machine"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.tone((180, 40, 50)), r, border_radius=3)
        glass = pygame.Rect(r.left + 6, r.top + 8, r.w - 26, r.h - 40)
        pygame.draw.rect(surf, (30, 34, 44), glass)
        cols = [(230, 200, 80), (90, 180, 230), (230, 120, 80)]
        for row, y in enumerate(range(glass.top + 6, glass.bottom - 8, 16)):
            for k, x in enumerate(range(glass.left + 4, glass.right - 6, 10)):
                pygame.draw.rect(surf, self.tone(cols[(row + k) % 3]), (x, y, 6, 9))
        pygame.draw.rect(surf, (40, 40, 44), (r.right - 16, r.top + 20, 10, 30))   # coin slot panel
        pygame.draw.rect(surf, (20, 20, 24), (r.left + 10, r.bottom - 24, r.w - 30, 14))
        pygame.draw.rect(surf, INK, r, 2, border_radius=3)

