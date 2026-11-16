"""Kit part: Sign (decor). Its owner is listed in OWNERS.md."""
import pygame



__all__ = ["Sign"]


class Sign:
    """Text on the wall, like a room sign."""

    def __init__(self, x, y, text, color=(220, 220, 228), size=28):
        self.pos = (int(x), int(y))
        self.img = pygame.font.Font(None, int(size)).render(text, True, color)

    def draw(self, surf):
        surf.blit(self.img, self.pos)

