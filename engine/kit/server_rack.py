"""Kit part: ServerRack (furniture). Its owner is listed in OWNERS.md."""
import math

import pygame

from ._base import KitFurniture, INK

__all__ = ["ServerRack"]


class ServerRack(KitFurniture):
    W, H, NAME = 50, 90, "server rack"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, (36, 38, 46) if not self.searched else (60, 60, 64), r, border_radius=2)
        pygame.draw.rect(surf, INK, r, 2, border_radius=2)
        t = pygame.time.get_ticks() / 1000.0
        for i, y in enumerate(range(r.top + 8, r.bottom - 6, 10)):
            on = math.sin(t * 3 + i * 1.7 + r.x) > 0
            pygame.draw.line(surf, (70, 72, 84), (r.left + 6, y), (r.right - 16, y), 2)
            pygame.draw.circle(surf, (90, 230, 120) if on else (40, 80, 50), (r.right - 9, y), 2)

