"""Hazards you can use as they are, or subclass for your own.

Any hazard is an object with .rect, .update(dt, room, player) and .draw(surf). Touching its rect
costs the player a life (DEATH_PENALTY seconds off the clock) and sends them back to the door.
"""
import math

import pygame

from . import config as C


class PatrolBot:
    """A security bot that rolls back and forth along a surface.

    x is where it starts; y is the surface it rolls on (C.FLOOR_Y for the ground, or a platform's y).
    It patrols between left and right. With sees=True it speeds up when the player is on its level
    and in front of it.
    """

    W, H = 34, 40

    def __init__(self, x, y, left, right, speed=90.0, sees=True):
        self.x = float(x)
        self.y_surface = int(y)
        self.left, self.right = int(left), int(right)
        self.speed = float(speed)
        self.sees = sees
        self.dir = 1
        self.alert = False
        self.t = 0.0
        self.rect = pygame.Rect(int(self.x), self.y_surface - self.H, self.W, self.H)

    def update(self, dt, room, player):
        self.t += dt
        level = abs(player.rect.bottom - self.y_surface) < 6
        ahead = (player.rect.centerx - self.rect.centerx) * self.dir > 0
        self.alert = self.sees and level and ahead and abs(player.rect.centerx - self.rect.centerx) < 320
        v = self.speed * (2.2 if self.alert else 1.0)
        self.x += self.dir * v * dt
        if self.x < self.left:
            self.x, self.dir = float(self.left), 1
        elif self.x + self.W > self.right:
            self.x, self.dir = float(self.right - self.W), -1
        self.rect.x = int(self.x)

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, (60, 64, 72), r, border_radius=8)
        pygame.draw.rect(surf, C.INK, r, 2, border_radius=8)
        eye_x = r.centerx + self.dir * 8
        eye = C.DANGER if self.alert else (120, 220, 255)
        pygame.draw.circle(surf, eye, (eye_x, r.top + 13), 6)
        if self.alert:
            s = pygame.Surface((90, 30), pygame.SRCALPHA)
            tip = 0 if self.dir > 0 else 90
            pygame.draw.polygon(s, (230, 70, 60, 70), [(tip, 13), (90 - tip, 2), (90 - tip, 28)])
            surf.blit(s, (eye_x if self.dir > 0 else eye_x - 90, r.top))
        wob = int(2 * math.sin(self.t * 14))
        pygame.draw.circle(surf, C.INK, (r.left + 8, r.bottom), 5 + (wob > 0))
        pygame.draw.circle(surf, C.INK, (r.right - 8, r.bottom), 5 + (wob <= 0))


class Zapper:
    """A floor-to-ceiling beam that switches on and off. x is its centre; it spans y_top..y_bottom.

    on_time and off_time are seconds; offset shifts it in the cycle so two zappers can alternate.
    """

    def __init__(self, x, y_top=0, y_bottom=C.FLOOR_Y, on_time=1.5, off_time=1.5, offset=0.0):
        self.on_time, self.off_time, self.t = on_time, off_time, offset
        self.on = False
        self.box = pygame.Rect(int(x) - 4, int(y_top), 8, int(y_bottom - y_top))
        self.rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt, room, player):
        self.t = (self.t + dt) % (self.on_time + self.off_time)
        self.on = self.t < self.on_time
        self.rect = self.box if self.on else pygame.Rect(0, 0, 0, 0)

    def draw(self, surf):
        pygame.draw.rect(surf, (90, 90, 100), (self.box.x - 4, self.box.top - 8, 16, 8))
        pygame.draw.rect(surf, (90, 90, 100), (self.box.x - 4, self.box.bottom, 16, 8))
        if self.on:
            pygame.draw.rect(surf, C.DANGER, self.box)
            pygame.draw.rect(surf, (255, 200, 190), self.box.inflate(-4, 0))
