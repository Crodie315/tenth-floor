"""Shared helpers for kit furniture. Owner: the maintainer (see OWNERS.md)."""
from .. import config as C
from ..room import Furniture

INK = C.INK


def shade(col, k):
    return tuple(max(0, min(255, int(c * k))) for c in col)


class KitFurniture(Furniture):
    """Kit furniture: fixed default size, optional name, drawn greyer once searched."""

    W, H, NAME = 60, 60, "thing"

    def __init__(self, x, y, name=None, holds_piece=False, w=None, h=None):
        super().__init__(x, y, w or self.W, h or self.H, name or self.NAME, holds_piece)

    def tone(self, col):
        return shade(col, 0.7) if self.searched else col

