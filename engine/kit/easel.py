"""Kit part: Easel (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["Easel"]


class Easel(KitFurniture):
    W, H, NAME = 60, 100, "easel"

    def draw(self, surf):
        r = self.rect
        leg = self.tone((140, 100, 60))
        pygame.draw.line(surf, leg, (r.left + 8, r.bottom), (r.centerx, r.top), 4)
        pygame.draw.line(surf, leg, (r.right - 8, r.bottom), (r.centerx, r.top), 4)
        canvas = pygame.Rect(r.left + 6, r.top + 14, r.w - 12, 44)
        pygame.draw.rect(surf, (240, 236, 226), canvas)
        pygame.draw.circle(surf, self.tone((200, 90, 70)), (canvas.centerx - 6, canvas.centery), 10)
        pygame.draw.line(surf, self.tone((60, 110, 170)), canvas.bottomleft, canvas.midtop, 3)
        pygame.draw.rect(surf, INK, canvas, 2)

