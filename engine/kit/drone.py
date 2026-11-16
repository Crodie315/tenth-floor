"""Kit part: Drone (hazard). Its owner is listed in OWNERS.md."""
import pygame

from .. import config as C
from ._base import INK

__all__ = ["Drone"]


class Drone:
    """A security drone that hovers up and down between y_top and y_bottom at x. Fly under it or time it."""

    W, H = 36, 22

    def __init__(self, x, y_top, y_bottom, speed=70.0, offset=0.0):
        self.x, self.y_top, self.y_bottom, self.speed = int(x), int(y_top), int(y_bottom), float(speed)
        span = max(1, self.y_bottom - self.y_top)
        self.y = self.y_top + (offset * self.speed) % span
        self.dir = 1
        self.rect = pygame.Rect(self.x, int(self.y), self.W, self.H)

    def update(self, dt, room, player):
        self.y += self.dir * self.speed * dt
        if self.y > self.y_bottom - self.H:
            self.y, self.dir = float(self.y_bottom - self.H), -1
        elif self.y < self.y_top:
            self.y, self.dir = float(self.y_top), 1
        self.rect.y = int(self.y)

    def draw(self, surf):
        r = self.rect
        spin = pygame.time.get_ticks() // 40 % 2
        for px in (r.left + 4, r.right - 4):
            pygame.draw.line(surf, (200, 200, 210), (px - (8 if spin else 4), r.top), (px + (8 if spin else 4), r.top), 2)
        pygame.draw.rect(surf, (70, 74, 84), r.inflate(0, -8).move(0, 2), border_radius=6)
        pygame.draw.circle(surf, C.DANGER, (r.centerx, r.centery + 2), 4)
        pygame.draw.rect(surf, INK, r.inflate(0, -8).move(0, 2), 2, border_radius=6)

