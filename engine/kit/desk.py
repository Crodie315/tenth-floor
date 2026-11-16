"""Kit part: Desk (furniture). Its owner is listed in OWNERS.md."""
import pygame

from ._base import KitFurniture, INK

__all__ = ["Desk"]


class Desk(KitFurniture):
    W, H, NAME = 110, 70, "desk"

    def draw(self, surf):
        r = self.rect
        top = pygame.Rect(r.left, r.bottom - 34, r.w, 8)
        pygame.draw.rect(surf, self.tone((150, 110, 70)), top)
        pygame.draw.rect(surf, self.tone((120, 88, 56)), (r.left + 6, top.bottom, 8, r.bottom - top.bottom))
        pygame.draw.rect(surf, self.tone((120, 88, 56)), (r.right - 14, top.bottom, 8, r.bottom - top.bottom))
        mon = pygame.Rect(r.centerx - 22, r.top, 44, 28)                 # a monitor on top
        pygame.draw.rect(surf, (30, 32, 40), mon, border_radius=2)
        pygame.draw.rect(surf, self.tone((90, 160, 220)), mon.inflate(-6, -6))
        pygame.draw.line(surf, (30, 32, 40), (r.centerx, mon.bottom), (r.centerx, top.top), 3)
        pygame.draw.rect(surf, INK, top, 2)

