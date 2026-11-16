"""Example floor with three rooms, built from the kit (engine/kit/; pictures in KIT.md).

A floor can have 2 to 5 rooms. List them west to east in ROOMS: the first opens onto the West elevator,
the last onto the East elevator, and you walk through the rest. One digit for the whole floor.
"""
from engine import config as C
from engine.kit import (Bookshelf, CeilingLight, Couch, Crusher, Desk, Drone, Easel, FilingCabinet, FloorLaser,
                        Locker, MovingPlatform, PatrolBot, Plant, Poster, Printer3D, Sign, VendingMachine, Window)
from engine.room import Platform, Room

NAME = "Studio Floor (kit example)"
AUTHOR = "Example"


class AnimationStudio(Room):
    title = "Animation Studio"

    def build(self):
        self.decor += [Window(70, 70), Window(640, 70, seed=2), Poster(300, 84, "CRIT"),
                       CeilingLight(250), CeilingLight(740), Sign(380, 46, "ANIMATION STUDIO")]
        self.platforms.append(Platform(400, 400, 200))
        self.furniture += [Desk(140, C.FLOOR_Y), Desk(620, C.FLOOR_Y), Bookshelf(450, 400), Plant(790, C.FLOOR_Y)]
        self.hazards.append(PatrolBot(300, C.FLOOR_Y, left=200, right=780, speed=80))


class FabLab(Room):
    """The digit is in the locker up on the ledge: ride the moving platform up to it."""

    title = "Fabrication Lab"

    def build(self):
        self.decor += [Sign(360, 46, "FABRICATION LAB"), CeilingLight(480), Poster(130, 90, "PLA", (70, 130, 180))]
        self.platforms.append(MovingPlatform(170, 470, 410, width=110, speed=70))
        self.platforms.append(Platform(640, 320, 260))
        self.furniture += [Printer3D(110, C.FLOOR_Y), Printer3D(560, C.FLOOR_Y),
                           Locker(690, 320, holds_piece=True), FilingCabinet(830, 320)]
        self.hazards.append(FloorLaser(180, 520, on_time=1.2, off_time=1.6))
        self.hazards.append(Crusher(760, y_top=170, y_bottom=320, w=50, h=40))


class Lounge(Room):
    title = "Lounge"

    def build(self):
        self.decor += [Window(560, 70, seed=5), Poster(120, 80, "MFA"), Poster(210, 80, "OPEN", (80, 140, 90)),
                       CeilingLight(330), Sign(360, 46, "LOUNGE")]
        self.platforms.append(Platform(250, 390, 150))
        self.furniture += [Couch(140, C.FLOOR_Y), VendingMachine(400, C.FLOOR_Y), Plant(280, 390), Easel(740, C.FLOOR_Y)]
        self.hazards.append(Drone(560, y_top=300, y_bottom=C.FLOOR_Y, speed=90))


ROOMS = [AnimationStudio, FabLab, Lounge]
