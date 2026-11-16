"""The contract every floor keeps. Read this before you build yours.

Your floor is one file, floors/<your_name>.py, with 2 to 5 rooms side by side, listed west to east in
ROOMS. The WEST elevator opens at the left edge of the first room; each room's right edge leads into the
next; the last room's right edge opens onto the EAST elevator. Players cross your floor to switch
elevators. A room is one screen. You subclass Room for each, fill in build(), and list them at the bottom.
Ready-made furniture, hazards, platforms and decor are in engine/kit/ (pictures in KIT.md).
The engine owns the player, searching, dying, the clock and the elevator. You own the layout, the
furniture, the hazards and the look.

    from engine.room import Room, Platform, Furniture
    from engine.bots import PatrolBot

    NAME = "Animation Floor"          # shown on the elevator panel
    AUTHOR = "Your Name"

    class Studio(Room):
        title = "Animation Studio"
        def build(self):
            self.platforms.append(Platform(200, 400, 240))
            self.furniture.append(Furniture(260, 400, 60, 40, "flat file"))
            self.furniture.append(Furniture(600, 500, 80, 50, "plinth", holds_piece=True))
            self.furniture.append(Furniture(820, 500, 60, 30, "stool"))
            self.hazards.append(PatrolBot(500, 500, left=420, right=860))

    class Kitchen(Room):
        title = "Kitchen"
        def build(self):
            ...

    ROOMS = [Studio, Kitchen]     # west to east: West elevator -> Studio -> Kitchen -> East elevator
    # (LEFT = Studio and RIGHT = Kitchen also works for a two-room floor)

Rules the check script enforces (python check.py):
  - exactly ONE piece of furniture on the whole floor holds_piece=True (it hides your floor's digit
    of the door code), and a player can reach it
  - 2 to 5 rooms; each has at least 3 pieces of furniture, and furniture sits on the floor or a platform
    (its bottom edge is that surface's y)
  - both edges of every room are doorways: keep the first 80 px of floor at each side clear
  - nothing stands on a moving platform; decor only needs .draw(surf)
  - nothing crashes for 20 seconds of play, and a frame takes under 8 ms
  - only your own file changes, plus your line in CREDITS.md
  - no pygame-ce-only calls (FRect, get_frect, pygame.Window, get_just_pressed ...)
"""
import math

import pygame

from . import config as C


class Platform:
    """A ledge you can stand on. One-way: you jump up through it and land on top.

    x, y is the left end of the top surface; width is how far it runs right.
    """

    THICK = 12

    def __init__(self, x, y, width):
        self.rect = pygame.Rect(int(x), int(y), int(width), self.THICK)

    @property
    def top(self):
        return self.rect.top

    def draw(self, surf):
        pygame.draw.rect(surf, C.PLATFORM, self.rect)
        pygame.draw.line(surf, C.PLATFORM_EDGE, self.rect.bottomleft, self.rect.bottomright, 3)


class Lift:
    """A platform the player drives up and down with UP / DOWN while standing on it.

    x, width as Platform; it travels between y_top and y_bottom and starts at y_start.
    Use y_bottom=C.FLOOR_Y for a lift you can walk straight onto from the floor.
    """

    SPEED = 160.0
    RETURN_AFTER = 2.0      # seconds with nobody on it before it glides back to where it started (Decision 6, DECISIONS.md)

    def __init__(self, x, y_top, y_bottom, width=64, y_start=None):
        self.y_top, self.y_bottom = int(y_top), int(y_bottom)
        self.y = float(self.y_bottom if y_start is None else y_start)
        self.home = self.y
        self.idle = 0.0
        self.rect = pygame.Rect(int(x), int(self.y), int(width), Platform.THICK)

    @property
    def top(self):
        return self.rect.top

    def drive(self, direction, dt):
        """direction -1 = up, +1 = down. Returns how far it moved (pixels, may be 0)."""
        old = self.y
        self.y = max(self.y_top, min(self.y_bottom, self.y + direction * self.SPEED * dt))
        self.rect.y = int(round(self.y))
        return self.y - old

    def go_home(self, dt):
        """The engine calls this while nobody is riding: after RETURN_AFTER seconds, glide back home."""
        self.idle += dt
        if self.idle < self.RETURN_AFTER or self.y == self.home:
            return
        step = self.SPEED * dt
        self.y = self.home if abs(self.home - self.y) <= step else self.y + math.copysign(step, self.home - self.y)
        self.rect.y = int(round(self.y))

    def draw(self, surf):
        cx = self.rect.centerx
        pygame.draw.line(surf, C.PLATFORM_EDGE, (cx, self.y_top - 30), (cx, self.y_bottom + 6), 2)
        pygame.draw.rect(surf, (230, 210, 120), self.rect)
        pygame.draw.line(surf, C.PLATFORM_EDGE, self.rect.bottomleft, self.rect.bottomright, 3)


class Furniture:
    """Something the player can search. x, y is the BOTTOM-left corner: y is the surface it stands on.

    Stand in front of it and hold UP to search. The one with holds_piece=True gives a keycard piece.
    Override draw() to give it your own look; keep self.rect as the searchable area.
    """

    def __init__(self, x, y, w, h, name, holds_piece=False):
        self.rect = pygame.Rect(int(x), int(y - h), int(w), int(h))
        self.name = name
        self.holds_piece = holds_piece
        self.searched = False
        self.progress = 0.0  # 0..1, set by the engine while the player searches

    def draw(self, surf):
        body = (150, 130, 100) if not self.searched else (110, 104, 96)
        pygame.draw.rect(surf, body, self.rect, border_radius=3)
        pygame.draw.rect(surf, C.INK, self.rect, 2, border_radius=3)
        mid = self.rect.top + self.rect.height // 2
        pygame.draw.line(surf, C.INK, (self.rect.left + 6, mid), (self.rect.right - 6, mid), 2)


class Room:
    """Subclass this. Set title, fill build(). The author comes from your floor's AUTHOR."""

    title = "Untitled room"
    author = "nobody yet"

    def __init__(self):
        self.platforms = []   # Platform objects (the ground floor is added for you)
        self.lifts = []       # Lift objects
        self.furniture = []   # Furniture objects; one holds_piece=True on the whole floor
        self.hazards = []     # anything with .rect, .update(dt, room, player), .draw(surf)
        self.decor = []       # wall things that are only looked at: anything with .draw(surf) (see engine/kit/)
        self.spawn_x = 40     # where the player appears, on the ground, coming from the elevator
        self.ground = Platform(0, C.FLOOR_Y, C.W)
        self.time = 0.0
        self.build()

    # --- yours ---------------------------------------------------------------------------------
    def build(self):
        raise NotImplementedError("fill in build() in your room")

    def update(self, dt, player):
        """Optional: anything that moves on its own besides hazards (lights, steam, signs)."""

    def draw_background(self, surf):
        """Optional: your walls, windows, posters. Drawn first."""
        surf.fill(C.WALL)
        for x in range(0, C.W, 120):
            pygame.draw.line(surf, (78, 82, 96), (x, 0), (x, C.FLOOR_Y), 1)

    def draw_foreground(self, surf):
        """Optional: anything drawn over the player (railings, steam, light cones)."""

    # --- the engine's; don't override ----------------------------------------------------------
    def surfaces(self):
        """Everything the player can stand on."""
        return [self.ground] + self.platforms + self.lifts

    def tick(self, dt, player):
        self.time += dt
        for p in self.platforms:
            if hasattr(p, "move"):            # a MovingPlatform from the kit
                p.move(dt)
        for lift in self.lifts:
            if player is not None and player.on is lift:
                lift.idle = 0.0
            else:
                lift.go_home(dt)
        self.update(dt, player)
        for h in self.hazards:
            h.update(dt, self, player)

    def draw(self, surf, player):
        self.draw_background(surf)
        for d in self.decor:
            d.draw(surf)
        pygame.draw.rect(surf, (54, 56, 64), (0, C.FLOOR_Y, C.W, C.H - C.FLOOR_Y))
        for p in self.platforms + self.lifts:
            p.draw(surf)
        for f in self.furniture:
            f.draw(surf)
            if 0 < f.progress < 1:
                bar = pygame.Rect(f.rect.left, f.rect.top - 10, int(f.rect.width * f.progress), 5)
                pygame.draw.rect(surf, C.PIECE, bar)
        for h in self.hazards:
            h.draw(surf)
        player.draw(surf)
        self.draw_foreground(surf)
