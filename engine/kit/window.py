"""Kit part: Window (decor). Its owner is listed in OWNERS.md."""
import pygame



__all__ = ["Window"]


class Window:
    """A night window onto the city. Drawn once when made; costs nothing per frame."""

    def __init__(self, x, y, w=140, h=110, seed=0):
        self.pos = (int(x), int(y))
        self.img = pygame.Surface((int(w), int(h)))
        self.img.fill((20, 26, 48))
        k = seed * 7 + 3
        bx = 0
        while bx < w:                                                   # skyline
            bw = 14 + (k % 4) * 6
            bh = 30 + (k * 13) % int(h * 0.6)
            pygame.draw.rect(self.img, (36, 40, 60), (bx, h - bh, bw, bh))
            for wy in range(int(h - bh + 6), int(h) - 4, 9):
                for wx in range(bx + 3, bx + bw - 3, 6):
                    if (wx * 31 + wy * 17 + k) % 5 == 0:
                        pygame.draw.rect(self.img, (240, 210, 120), (wx, wy, 3, 4))
            bx += bw + 2
            k += 5
        pygame.draw.rect(self.img, (150, 150, 160), self.img.get_rect(), 6)
        pygame.draw.line(self.img, (150, 150, 160), (w // 2, 0), (w // 2, h), 4)

    def draw(self, surf):
        surf.blit(self.img, self.pos)

