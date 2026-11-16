"""Checks every floor keeps the contract. Run it before you push; GitHub runs it on every pull request.

    python check.py                      # check every floor
    python check.py --floor my_floor     # check one floor
    python check.py --pr origin/main     # also check your branch only changes your own files
    python check.py --shots              # also save a picture of each room to shots/
    python check.py --codeowners         # rewrite .github/CODEOWNERS from OWNERS.md

It checks floors, not taste: a floor can pass and still be no fun. Play it: python main.py --floor NAME
"""
import argparse
import fnmatch
import importlib
import math
import os
import random
import re
import subprocess
import sys
import time
import traceback

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame  # noqa: E402

from engine import building, config as C, lobby  # noqa: E402
from engine.player import Keys, Player  # noqa: E402
from engine.room import Lift, Room  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# Calls that exist in pygame-ce but not in plain pygame 2.6. Someone in class runs plain pygame.
CE_ONLY = [r"\bFRect\b", r"get_frect", r"pygame\.Window\b", r"get_just_pressed", r"get_just_released",
           r"\.scale_by\(", r"pygame\.geometry", r"pygame\.typing", r"_sdl2", r"\.draw\.aacircle",
           r"\.draw\.aaline\(.*,\s*\d+\s*\)", r"\bfblits\b", r"\.premul_alpha", r"\.blur\("]

FRAME_BUDGET_MS = 8.0
SIM_SECONDS = 20


def fail(msgs, text):
    msgs.append(text)


def air_time(rise):
    """Seconds until the feet are back down at `rise` px above takeoff (None if too high)."""
    v, g = C.JUMP_SPEED, C.GRAVITY
    disc = v * v - 2 * g * rise
    if disc < 0:
        return None
    return (v + math.sqrt(disc)) / g


def can_hop(a_top, a_left, a_right, b_top, b_left, b_right):
    rise = a_top - b_top                      # positive = b is higher
    if rise > C.JUMP_HEIGHT - 6:
        return False
    t = air_time(max(rise, 0.0))
    if rise < 0:                              # dropping down: more time in the air
        t = air_time(0) + math.sqrt(2 * -rise / C.GRAVITY)
    gap = max(0, b_left - a_right, a_left - b_right)
    return gap <= C.RUN_SPEED * t * 0.85 + Player.W - 6


def span(s):
    """Left and right x a surface can reach: a moving platform covers its whole track (ride it, or wait for it)."""
    if hasattr(s, "x_left") and hasattr(s, "move"):
        return s.x_left, s.x_right + s.rect.w
    return s.rect.left, s.rect.right


def reachable(room):
    """Which surfaces a player can stand on, starting from the ground. Lifts can stop anywhere on their track;
    moving platforms can be anywhere along theirs."""
    nodes = []
    for s in room.surfaces():
        if isinstance(s, Lift):
            nodes.append((s, s.rect.top, s.y_top, s.y_bottom))
        else:
            nodes.append((s, s.rect.top, s.rect.top, s.rect.top))
    seen = {id(room.ground)}
    frontier = [room.ground]
    while frontier:
        a = frontier.pop()
        a_lo, a_hi = (a.y_top, a.y_bottom) if isinstance(a, Lift) else (a.rect.top, a.rect.top)
        for b, start, b_lo, b_hi in nodes:
            if id(b) in seen:
                continue
            ok = False
            # from any height a can be at, to b's resting height (a lift you reach at its start position)
            b_at = [start] if isinstance(b, Lift) else [b_lo]
            for ya in {a_lo, a_hi} | ({start} if False else set()):
                for yb in b_at:
                    if can_hop(ya, *span(a), yb, *span(b)):
                        ok = True
            if isinstance(a, Lift) and not ok:   # ride a to any height in its track
                for ya in range(a_lo, a_hi + 1, 4):
                    if can_hop(ya, *span(a), b_at[0], *span(b)):
                        ok = True
                        break
            if ok:
                seen.add(id(b))
                frontier.append(b)
    return seen


def standing_on(room, f):
    for s in [room.ground] + room.platforms:
        if abs(f.rect.bottom - s.rect.top) <= 1 and s.rect.left <= f.rect.centerx <= s.rect.right:
            return s
    return None


def check_source(path, msgs):
    text = open(path, encoding="utf-8").read()
    for i, line in enumerate(text.splitlines(), 1):
        code = line.split("#", 1)[0]
        for pat in CE_ONLY:
            if re.search(pat, code):
                fail(msgs, f"line {i}: {pat.strip(chr(92) + 'b')} is pygame-ce only; someone in class runs plain pygame")
    if re.search(r"^\s*(import|from)\s+(subprocess|socket|requests|urllib)", text, re.M):
        fail(msgs, "floors may not run programs or reach the network")


def check_room(name, side, cls, shots, msgs):
    """One side of a floor. Returns (pieces in it, avg ms, worst ms), or None if it couldn't run."""
    def bad(text):
        fail(msgs, f"{side}: {text}")
    if not (isinstance(cls, type) and issubclass(cls, Room)):
        return bad("must be one of your Room classes (the class itself, no brackets)")
    if cls.title == Room.title:
        bad("set title = \"...\" on this room")
    try:
        room = cls()
    except Exception:
        return bad("build() crashed:\n" + traceback.format_exc(limit=3))

    pieces = sum(1 for f in room.furniture if f.holds_piece)
    if len(room.furniture) < 3:
        bad(f"put out at least 3 pieces of furniture so there's something to search (found {len(room.furniture)})")

    ok_surfaces = reachable(room)
    for f in room.furniture:
        s = standing_on(room, f)
        if s is None:
            bad(f"furniture '{f.name}' floats: its bottom (y={f.rect.bottom}) isn't on the floor ({C.FLOOR_Y}) "
                f"or on a platform under its middle")
        elif id(s) not in ok_surfaces and f.holds_piece:
            bad(f"the piece in '{f.name}' can't be reached: no jump or lift gets a player onto the "
                f"surface at y={s.rect.top} (a jump rises about {int(C.JUMP_HEIGHT)} px)")
        if not (0 <= f.rect.left and f.rect.right <= C.W):
            bad(f"furniture '{f.name}' is off the screen")
    for p in room.platforms:
        if not (0 <= p.rect.left and p.rect.right <= C.W and 40 <= p.rect.top < C.FLOOR_Y):
            bad(f"platform at {p.rect.topleft} is off the screen or under the HUD (keep y between 40 and {C.FLOOR_Y})")
    for f in room.furniture:
        s_ = standing_on(room, f)
        if s_ is not None and hasattr(s_, "move"):
            bad(f"furniture '{f.name}' is on a moving platform; it would be left floating when the platform moves")
    for d in room.decor:
        if not hasattr(d, "draw"):
            bad(f"decor {type(d).__name__} needs .draw(surf)")
    for h in room.hazards:
        for attr in ("rect", "update", "draw"):
            if not hasattr(h, attr):
                bad(f"hazard {type(h).__name__} needs .{attr}")
    # You walk in at both edges: from an elevator at the floor's end, from the other room in the middle.
    doors = [pygame.Rect(x - 20, C.FLOOR_Y - Player.H, Player.W + 40, Player.H) for x in (40, C.W - 40 - Player.W)]
    in_door = set()        # hazards that stand still (no .dir) and are ever in a doorway while it plays

    # Play it for a while with mashed keys: nothing may crash, and it must stay fast.
    rng = random.Random(name + side)
    player = Player(40, C.FLOOR_Y)
    surf = pygame.Surface((C.W, C.H))
    keys = Keys()
    worst, total, frames = 0.0, 0.0, int(SIM_SECONDS * C.FPS)
    dt = 1.0 / C.FPS
    try:
        for i in range(frames):
            if i % 20 == 0:
                keys = Keys(left=rng.random() < 0.4, right=rng.random() < 0.4, up=rng.random() < 0.3,
                            down=rng.random() < 0.15, jump=rng.random() < 0.3)
            t0 = time.perf_counter()
            room.tick(dt, player)
            for h in room.hazards:
                if not hasattr(h, "dir") and hasattr(h, "rect") and h.rect.collidelist(doors) >= 0:
                    in_door.add(type(h).__name__)
            ev = player.update(dt, keys, room)
            room.draw(surf, player)
            ms = (time.perf_counter() - t0) * 1000
            worst, total = max(worst, ms), total + ms
            if "exit_left" in ev or "exit_right" in ev or "dead" in ev:
                player = Player(40 if rng.random() < 0.5 else C.W - 40 - Player.W, C.FLOOR_Y)
            if i == 60 and shots:
                os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
                pygame.image.save(surf, os.path.join(HERE, "shots", f"{name}_{side.replace(' ', '')}.png"))
    except Exception:
        return bad(f"crashed {i / C.FPS:.1f} s into play:\n" + traceback.format_exc(limit=4))
    for name_ in sorted(in_door):
        bad(f"hazard {name_} sits in a doorway; leave the first 80 px of floor at each side clear")
    avg = total / frames
    if avg > FRAME_BUDGET_MS:
        bad(f"too slow: {avg:.1f} ms a frame on average (budget {FRAME_BUDGET_MS} ms). "
            f"Make big Surfaces and Fonts once in build(), not every frame")
    return pieces, avg, worst


MAX_ROOMS = 5


def check_floor(name, shots, msgs):
    """Returns (avg ms, worst ms) over all its rooms, or None."""
    check_source(os.path.join(HERE, "floors", name + ".py"), msgs)
    try:
        mod = importlib.import_module("floors." + name)
    except Exception:
        return fail(msgs, "the file doesn't import:\n" + traceback.format_exc(limit=3))
    for attr, what in (("NAME", 'NAME = "..." (the name on the elevator panel)'), ("AUTHOR", 'AUTHOR = "Your Name"')):
        if not hasattr(mod, attr):
            fail(msgs, f"add {what} to your file")
    if hasattr(mod, "ROOMS"):
        rooms = mod.ROOMS
        if not isinstance(rooms, (list, tuple)):
            fail(msgs, "ROOMS must be a list of your Room classes, west to east: ROOMS = [Lab, Hall, Studio]")
            rooms = []
    elif hasattr(mod, "LEFT") and hasattr(mod, "RIGHT"):
        rooms = [mod.LEFT, mod.RIGHT]
    else:
        fail(msgs, "list your rooms, west to east: ROOMS = [FirstRoom, SecondRoom, ...] (or LEFT = ... and RIGHT = ...)")
        rooms = []
    if msgs:
        return None
    if not (isinstance(mod.NAME, str) and mod.NAME.strip()) or not (isinstance(mod.AUTHOR, str) and mod.AUTHOR.strip()):
        fail(msgs, "NAME and AUTHOR need to be text")
    if not 2 <= len(rooms) <= MAX_ROOMS:
        fail(msgs, f"a floor has 2 to {MAX_ROOMS} rooms (found {len(rooms)})")
    if len(set(map(id, rooms))) != len(rooms):
        fail(msgs, "the same room is listed twice; each room in ROOMS should be its own class")
    labels = [f"room {k + 1}" for k in range(len(rooms))]
    results = [check_room(name, label, cls, shots, msgs) for label, cls in zip(labels, rooms)]
    if not results or any(r is None for r in results):
        return None
    pieces = sum(r[0] for r in results)
    if pieces != 1:
        fail(msgs, f"exactly one piece of furniture on the whole floor needs holds_piece=True (found {pieces})")
    return max(r[1] for r in results), max(r[2] for r in results)


MAINTAINER = "@rattlesnake-ike"


def read_owners():
    """The pieces table in OWNERS.md: [(piece, owner, github, [patterns])]."""
    rows = []
    for line in open(os.path.join(HERE, "OWNERS.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and "`" in cells[3]:
            rows.append((cells[0], cells[1], cells[2], re.findall(r"`([^`]+)`", cells[3])))
    return rows


def piece_of(path, owners):
    """(piece, owner, github) for a file path, or None if no piece claims it."""
    m = re.fullmatch(r"floors/([A-Za-z0-9_]+)(\.py|_assets/.+)", path)
    for piece, owner, gh, pats in owners:
        if any(fnmatch.fnmatchcase(path, pat) for pat in pats):
            return piece, owner, gh
    if m:
        return f"floor {m.group(1)}", "its AUTHOR", ""
    if re.fullmatch(r"engine/kit/[a-z0-9_]+\.py", path):
        return f"Kit: new part {path[len('engine/kit/'):-3]}", "open", ""
    return None


def check_pr(base, msgs):
    """Returns (description, set of floor names touched). One piece per pull request."""
    try:
        out = subprocess.run(["git", "diff", "--name-status", f"{base}...HEAD"], cwd=HERE,
                             capture_output=True, text=True, check=True).stdout
    except Exception as e:
        fail(msgs, f"could not diff against {base}: {e}")
        return None, set()
    owners = read_owners()
    pieces, floors = {}, set()
    for line in out.splitlines():
        parts = line.split("\t")
        status, paths = parts[0], parts[1:]
        if status.startswith("R"):             # a rename lists old then new; the old one is the problem
            fail(msgs, f"{paths[0]} -> {paths[1]}: don't rename files; add a new one instead")
            paths = paths[1:]
        for p in paths:
            if p == "CREDITS.md":
                continue
            got = piece_of(p, owners)
            if got is None:
                fail(msgs, f"{p}: no piece in OWNERS.md covers this file. Put your work in your own piece "
                           f"(your floor, or a piece you own), or ask the maintainer to add a piece")
                continue
            pieces.setdefault(got, []).append(p)
            if got[0].startswith("floor "):
                floors.add(got[0][6:])
                if status.startswith("D"):
                    fail(msgs, f"{p}: don't delete floor files")
    if len(pieces) > 1:
        fail(msgs, "one piece per pull request: this touches " + "; ".join(
            f"{piece} ({', '.join(files[:3])})" for (piece, _, _), files in pieces.items())
            + ". Split it into one pull request per piece")
    for r in floors:
        if not re.fullmatch(r"[a-z][a-z0-9_]*", r):
            fail(msgs, f"floors/{r}.py: name your file in lowercase letters, numbers and underscores")
    if len(pieces) != 1:
        return None, floors
    (piece, owner, gh), _ = next(iter(pieces.items()))
    if piece.startswith("floor "):
        who = "a classmate plays it and reviews it; the maintainer merges"
    elif owner.lower() == "open" or "maintainer" in owner:
        who = f"the maintainer reviews ({MAINTAINER})"
    else:
        who = f"{owner} {gh} reviews (the piece's owner); the maintainer merges"
    return f"piece: {piece} -> {who}", floors


def write_codeowners():
    """GitHub's CODEOWNERS, from OWNERS.md. GitHub only asks owners who are collaborators on the repo."""
    lines = ["# Made by: python check.py --codeowners   (from OWNERS.md; edit OWNERS.md, not this file)",
             f"*  {MAINTAINER}"]
    for piece, owner, gh, pats in read_owners():
        handle = gh if gh.startswith("@") else MAINTAINER
        for pat in pats:
            lines.append(f"/{pat}  {handle}")
    path = os.path.join(HERE, ".github", "CODEOWNERS")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {path} ({len(lines) - 2} patterns)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor")
    ap.add_argument("--pr", metavar="BASE")
    ap.add_argument("--shots", action="store_true")
    ap.add_argument("--codeowners", action="store_true", help="write .github/CODEOWNERS from OWNERS.md")
    args = ap.parse_args()
    if args.codeowners:
        write_codeowners()
        return 0

    pygame.init()
    pygame.display.set_mode((1, 1))
    print(f"pygame {pygame.version.ver} ({'pygame-ce' if getattr(pygame, 'IS_CE', False) else 'pygame'})")
    bad = 0
    if args.pr:
        msgs = []
        what, touched = check_pr(args.pr, msgs)
        print(f"\n[files] {'OK' if not msgs else 'FAIL'}  {what or ('only CREDITS.md' if not msgs else 'see below')}")
        for m in msgs:
            print("   - " + m)
        bad += bool(msgs)

    files = sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "floors"))
                   if f.endswith(".py") and not f.startswith("_"))
    if args.floor and args.floor not in files:
        print(f"\nno file floors/{args.floor}.py")
        return 1
    for name in files:
        if args.floor and name != args.floor:
            continue
        msgs = []
        timing = check_floor(name, args.shots, msgs)
        t = f"  {timing[0]:.2f} ms/frame avg, {timing[1]:.1f} worst" if timing else ""
        print(f"\n[{name}] {'OK' if not msgs else 'FAIL'}{t}")
        for m in msgs:
            print("   - " + m)
        bad += bool(msgs)
    if not args.floor:                      # every file has an owner, and GitHub's copy of the list is current
        msgs = []
        owners = read_owners()
        try:
            tracked = subprocess.run(["git", "ls-files"], cwd=HERE, capture_output=True, text=True,
                                     check=True).stdout.split()
        except Exception:
            tracked = []
        orphans = [f for f in tracked if f != "CREDITS.md" and piece_of(f, owners) is None]
        if orphans:
            fail(msgs, f"no piece in OWNERS.md covers: {', '.join(orphans[:6])}")
        want = os.path.join(HERE, ".github", "CODEOWNERS")
        have = open(want, encoding="utf-8").read() if os.path.exists(want) else ""
        expect = ["*  " + MAINTAINER] + [f"/{pat}  {gh if gh.startswith('@') else MAINTAINER}"
                                         for _, _, gh, pats in owners for pat in pats]
        if [ln for ln in have.splitlines() if ln and not ln.startswith("#")] != expect:
            fail(msgs, ".github/CODEOWNERS doesn't match OWNERS.md: run python check.py --codeowners")
        print(f"\n[owners] {'OK' if not msgs else 'FAIL'}  {len(owners)} pieces, {len(tracked)} files")
        for m in msgs:
            print("   - " + m)
        bad += bool(msgs)
    if not args.floor:                      # the engine's own lobby keeps the same rules, with no digit
        msgs = []
        res = [check_room("lobby", side, cls, args.shots, msgs) for side, cls in (("room 1", lobby.LEFT), ("room 2", lobby.RIGHT))]
        if all(res) and sum(r[0] for r in res) != 0:
            fail(msgs, "the lobby shouldn't hold a code digit")
        print(f"\n[lobby (engine)] {'OK' if not msgs else 'FAIL'}")
        for m in msgs:
            print("   - " + m)
        bad += bool(msgs)
    floors = building.load_floors(only=args.floor)
    where = building.place(floors)
    print(f"\n{len(floors)} floor{'s' if len(floors) != 1 else ''}, on floors {sorted(where)}; "
          f"{bad} problem{'s' if bad != 1 else ''}.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
