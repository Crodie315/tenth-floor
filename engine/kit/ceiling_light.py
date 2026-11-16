"""Kit part: CeilingLight (decor). Its owner is listed in OWNERS.md."""
import pygame



__all__ = ["CeilingLight"]


class CeilingLight:
    """A hanging lamp with a soft cone of light."""

    def __init__(self, x, cord=50, reach=300, color=(255, 236, 180)):
        self.x, self.cord = int(x), int(cord)
        self.cone = pygame.Surface((240, reach), pygame.SRCALPHA)
        pygame.draw.polygon(self.cone, (*color, 16), [(110, 0), (130, 0), (240, reach), (0, reach)])
        self.color = color

    def draw(self, surf):
        y = 34 + self.cord
        pygame.draw.line(surf, (40, 40, 44), (self.x, 34), (self.x, y), 2)
        surf.blit(self.cone, (self.x - 120, y + 6))
        pygame.draw.polygon(surf, (70, 70, 76), [(self.x - 14, y + 8), (self.x + 14, y + 8), (self.x + 7, y), (self.x - 7, y)])
        pygame.draw.circle(surf, self.color, (self.x, y + 9), 4)

