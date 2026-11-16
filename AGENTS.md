# Instructions for coding agents working in this repo

This is a class game. Each person adds one floor, at the same time, by pull request.

## The one rule

**Change only the student's own floor file, `floors/<their_name>.py`, plus their single line in
`CREDITS.md`.** Do not edit `engine/`, `main.py`, `check.py`, `.github/`, or anyone else's floor, even to
fix a bug or "improve" something. If the floor needs behavior the engine lacks, write it as a class inside
the floor file. If the engine looks broken, stop and tell the student.

If the student explicitly asks to change another piece (a kit part, the screens, the engine), that is a
separate pull request on its own branch, one piece per pull request (OWNERS.md lists every piece and its
owner, who reviews it). Never mix it with their floor. Never make an
engine change as a side effect of floor work, and never edit `RULES.md` or `DECISIONS.md` unless the
maintainer asked for it: rules change by decision.

## Before you say a floor is done

1. `python check.py --floor <name>` prints `OK`. The check also runs on plain pygame 2.6, so don't use
   pygame-ce-only calls (`FRect`, `get_frect`, `pygame.Window`, `key.get_just_pressed`, `scale_by`, `fblits`).
2. `python main.py --floor <name>` opens and both rooms play. The check cannot tell whether the floor is
   fun or readable, so tell the student to play it themselves.
3. `git diff --stat` shows only their floor file (and CREDITS.md).

## How floors work

Read the docstring at the top of `engine/room.py`, then `floors/example_floor.py`, `KIT.md` and
`floors/example_kit_floor.py`. A floor file sets `NAME`, `AUTHOR` and `ROOMS` (2 to 5 Room classes, west to
east: the West elevator is through the first room's left edge, the East elevator through the last room's
right edge), and exactly one piece of furniture on the whole floor has `holds_piece=True`. Prefer kit parts
(`from engine.kit import ...`) over drawing from scratch; never edit the kit. Coordinates are pixels on a 960 x 540 screen, y grows downward, and the
floor's top is `C.FLOOR_Y` (500). `Furniture(x, y, w, h, ...)` takes its **bottom**-left corner, so `y` is
the surface it stands on. Build fonts and big Surfaces once in `build()`, never inside `draw_*`.

## Git

Commit after each working change, with a message that says what changed. Never force-push. Never
commit `.venv/` or `shots/`.
