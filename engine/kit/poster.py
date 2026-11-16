"""Kit part: Poster (decor). Its owner is listed in OWNERS.md."""
import pygame

from ._base import shade, INK

__all__ = ["Poster"]


class Poster:
    """A poster with a word or two on it."""

    def __init__(self, x, y, text="SVA", color=(200, 90, 70), w=70, h=96):
        self.pos = (int(x), int(y))
        self.img = pygame.Surface((int(w), int(h)))
        self.img.fill(color)
        pygame.draw.circle(self.img, shade(color, 1.35), (w // 2, h // 2 - 8), w // 3)
        label = pygame.font.Font(None, 22).render(text, True, (250, 248, 240))
        self.img.blit(label, (w // 2 - label.get_width() // 2, h - 22))
        pygame.draw.rect(self.img, INK, self.img.get_rect(), 2)

    def draw(self, surf):
        surf.blit(self.img, self.pos)

