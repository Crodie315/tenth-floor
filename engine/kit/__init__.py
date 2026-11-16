"""The kit: ready-made parts for your floor. Import what you need: `from engine.kit import Desk, Crusher`.

One file per part, so each part can have its own owner (OWNERS.md). To add a part, add a file here with
`__all__ = ["YourPart"]`; it's picked up on its own. Pictures of every part: KIT.md
(redraw them with `python -m engine.kit_catalog`).

FURNITURE (searchable; pass holds_piece=True to hide your digit in it):
    Desk, Bookshelf, Locker, FilingCabinet, ServerRack, Printer3D, Easel, Couch, Plant, VendingMachine, Plinth
HAZARDS (self.hazards):   PatrolBot, Zapper (from engine.bots), Crusher, Drone, FloorLaser
PLATFORMS (self.platforms): MovingPlatform, a ledge that slides left and right and carries you
DECOR (self.decor; only looked at, drawn on the wall): Window, Poster, Sign, CeilingLight
"""
import importlib
import pkgutil

from ..bots import PatrolBot, Zapper  # noqa: F401  (part of the kit too)

__all__ = ["PatrolBot", "Zapper"]
PARTS = {}          # {class name: module name}, for the catalog and the check

for _info in sorted(pkgutil.iter_modules(__path__), key=lambda i: i.name):
    if _info.name.startswith("_") or _info.name == "catalog":
        continue
    _mod = importlib.import_module(f"{__name__}.{_info.name}")
    for _name in getattr(_mod, "__all__", []):
        globals()[_name] = getattr(_mod, _name)
        __all__.append(_name)
        PARTS[_name] = _info.name
