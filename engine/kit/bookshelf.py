"""Kit part: Bookshelf (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["Bookshelf"]


class Bookshelf(KitFurniture):
    W, H, NAME = 70, 110, "bookshelf"

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.tone((110, 76, 50)), r)
        cols = [(170, 60, 60), (60, 110, 170), (200, 170, 70), (80, 140, 90), (150, 90, 160)]
        for row, y in enumerate(range(r.top + 6, r.bottom - 10, 26)):
            x = r.left + 5
            k = row
            while x < r.right - 10:
                w = 6 + (k * 7) % 5
                pygame.draw.rect(surf, self.tone(cols[k % len(cols)]), (x, y + 4, w, 18))
                x += w + 1
                k += 3
            pygame.draw.line(surf, INK, (r.left, y + 22), (r.right, y + 22), 2)
        pygame.draw.rect(surf, INK, r, 2)

