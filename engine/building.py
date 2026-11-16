"""The building: which floor is whose, and where the two elevators stop.

Every floor runs between two elevators: the WEST elevator at its left end and the EAST elevator at its
right end. You get off one, walk the floor's rooms west to east (two or more), and get on the other.
The West elevator stops at the lobby through floor 9; the East elevator stops at 2 through the top,
including 10. So the only way up to 10 is across at least one floor.

Floors are found by file: every floors/<name>.py with its ROOMS (or LEFT and RIGHT) is in the game. Nobody edits
this file to add a floor, so a whole class can add floors at once without a merge conflict here.
Floors listed in ASSIGN go where they're told. The rest fill floors 2 to 9, then 11 and up, in
alphabetical order of file name, with the example floors last. The building is as tall as it needs to be.
"""
import importlib
import os
import pkgutil

GOAL = 10                # the floor you're trying to reach: MFA Computer Arts
PIECES_NEEDED = 8        # keycard pieces that unlock it (capped at the number of floors)

# Floor names on the elevator panel: SVA, 133/141 West 21st Street. Known (Isaac 11-14; sva.edu listings):
# the ground floor is the SVA Flatiron Gallery and the 10th floor is MFA Computer Arts. A student's floor
# shows its own NAME.
FLOOR_NAMES = {1: "Lobby / Flatiron Gallery", GOAL: "MFA Computer Arts"}

# Pin a floor file to a floor number: "file_name": 4. Empty = everyone placed in order.
ASSIGN = {}


class Floor:
    """One student's floor, read from floors/<name>.py."""

    def __init__(self, name, mod):
        self.file = name
        self.name = mod.NAME
        self.author = mod.AUTHOR
        # Rooms, west to east: ROOMS = [A, B, C, ...], or the two-room form LEFT = A and RIGHT = B.
        self.room_classes = list(mod.ROOMS) if hasattr(mod, "ROOMS") else [mod.LEFT, mod.RIGHT]


def load_floors(only=None):
    """Returns {file_name: Floor} for every floor file that imports. Broken files are skipped with a
    message so one bad floor can't stop the class's game; check.py is where they get caught."""
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "floors")
    found = {}
    for info in sorted(pkgutil.iter_modules([here]), key=lambda i: i.name):
        if info.name.startswith("_") or (only and info.name != only):
            continue
        try:
            mod = importlib.import_module("floors." + info.name)
            found[info.name] = Floor(info.name, mod)
        except Exception as e:  # noqa: BLE001 - a student's floor must not take the game down
            print(f"[skipped floor {info.name}: {type(e).__name__}: {e}]")
    return found


def open_floors():
    """Floor numbers a student can have, in the order they fill: 2..9, then 11, 12, ..."""
    n = 2
    while True:
        if n != GOAL:
            yield n
        n += 1


def place(floors):
    """Returns {floor_number: file_name}."""
    where = {}
    for name, number in ASSIGN.items():
        if name in floors and number not in (1, GOAL):
            where[number] = name
    order = sorted((n for n in floors if n not in where.values()), key=lambda n: (n.startswith("example"), n))
    numbers = (n for n in open_floors() if n not in where)
    for name in order:
        where[next(numbers)] = name
    return where


def west_stops(top_floor):
    return list(range(1, GOAL))


def east_stops(top_floor):
    return list(range(2, top_floor + 1))


def top(where):
    """The highest floor in the building."""
    return max([GOAL] + list(where))


def floor_name(number, where, floors):
    if number in where:
        return floors[where[number]].name
    return FLOOR_NAMES.get(number, f"Floor {number}")
