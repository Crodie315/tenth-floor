"""Kit part: FloorLaser (hazard). Its owner is listed in OWNERS.md."""
import pygame

from .. import config as C

__all__ = ["FloorLaser"]


class FloorLaser:
    """A low beam across a stretch of floor that switches on and off. Jump it while it's on.

    x_left..x_right: where it runs. y: the surface it runs along (C.FLOOR_Y or a ledge's y).
    """

    def __init__(self, x_left, x_right, y=C.FLOOR_Y, on_time=1.4, off_time=1.4, offset=0.0, height=14):
        self.on_time, self.off_time, self.t = on_time, off_time, offset
        self.box = pygame.Rect(int(x_left), int(y) - int(height) - 4, int(x_right - x_left), 6)
        self.posts = (int(x_left) - 6, int(x_right))
        self.on = False
        self.rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt, room, player):
        self.t = (self.t + dt) % (self.on_time + self.off_time)
        self.on = self.t < self.on_time
        self.rect = self.box if self.on else pygame.Rect(0, 0, 0, 0)

    def draw(self, surf):
        for px in self.posts:
            pygame.draw.rect(surf, (90, 90, 100), (px, self.box.top - 8, 6, self.box.bottom + 8 - self.box.top + 4))
        if self.on:
            pygame.draw.rect(surf, C.DANGER, self.box)
            pygame.draw.line(surf, (255, 200, 190), self.box.midleft, self.box.midright, 2)

