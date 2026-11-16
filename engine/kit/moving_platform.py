"""Kit part: MovingPlatform (platform). Its owner is listed in OWNERS.md."""
import pygame

from .. import config as C
from ..room import Platform

__all__ = ["MovingPlatform"]


class MovingPlatform(Platform):
    """A ledge that slides between x_left and x_right (its left end) at speed, carrying whoever stands on it."""

    def __init__(self, x_left, x_right, y, width=110, speed=70.0, offset=0.0):
        super().__init__(x_left, y, width)
        self.x_left, self.x_right, self.speed = int(x_left), int(x_right), float(speed)
        self.x = float(x_left) + (offset * self.speed) % max(1, self.x_right - self.x_left)
        self.dir = 1
        self.carry = 0.0          # how far it moved this frame; the engine moves a rider by the same
        self.rect.x = int(self.x)

    def move(self, dt):
        old = self.rect.x
        self.x += self.dir * self.speed * dt
        if self.x > self.x_right:
            self.x, self.dir = float(self.x_right), -1
        elif self.x < self.x_left:
            self.x, self.dir = float(self.x_left), 1
        self.rect.x = int(round(self.x))
        self.carry = self.rect.x - old

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 170, 110), self.rect)
        pygame.draw.line(surf, C.PLATFORM_EDGE, self.rect.bottomleft, self.rect.bottomright, 3)
        for x in (self.rect.left + 10, self.rect.right - 14):
            pygame.draw.circle(surf, C.PLATFORM_EDGE, (x, self.rect.centery), 3)

