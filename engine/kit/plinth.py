"""Kit part: Plinth (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["Plinth"]


class Plinth(KitFurniture):
    """A gallery plinth with a piece on top. colors = (piece color, accent color)."""

    W, H, NAME = 70, 50, "plinth"

    def __init__(self, x, y, name=None, holds_piece=False, w=None, h=None, colors=((60, 110, 170), (230, 230, 230))):
        super().__init__(x, y, name, holds_piece, w, h)
        self.colors = colors

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, (225, 222, 214), r)
        pygame.draw.rect(surf, INK, r, 2)
        art = pygame.Rect(r.left + 6, r.top - 60, r.w - 12, 60)
        pygame.draw.rect(surf, self.tone(self.colors[0]), art)
        pygame.draw.circle(surf, self.colors[1], art.center, min(art.w, art.h) // 3)
        pygame.draw.rect(surf, (30, 30, 30), art, 3)

