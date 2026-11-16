# Decisions

Whole-game decisions, newest last. Each one says what was asked, what the options were, who decided, and
why, so nobody has to guess or argue it again. **The maintainer decides** (Isaac); anyone can ask for a
decision by opening a **Rule proposal** issue. When a decision changes the engine, the engine pull request
links back here.

Floor-level choices (your layout, your hazards, your art) are yours and don't go here.

---

### 1. The game and the building (Isaac, 2026-11-14)
- **Asked:** what is the class game, and where is it set?
- **Decided:** *Tenth Floor*, an elevator-and-search platformer set in SVA at 133/141 West 21st Street, after
  hours. The goal is the 10th floor, MFA Computer Arts. The genre is borrowed (elevators, rooms to search,
  security robots, a clock); no other game's name, characters or look.

### 2. Everyone builds a floor (Isaac, 2026-11-16)
- **Asked:** does each person build one room or a whole floor?
- **Options:** one room each; a whole floor each (two rooms); one long scrolling floor.
- **Decided:** a whole floor each: two rooms, `LEFT` and `RIGHT`, in one file, `floors/<name>.py`.
- **Why:** a floor is the unit the building is made of, and it's the right size for one person in an hour
  with an agent. One file per person means no two people ever edit the same file.

### 3. Two elevators, split stops (Isaac, 2026-11-16)
- **Asked:** how do floors connect?
- **Options:** one central elevator; two elevators that both stop everywhere; split stops; alternating stops.
- **Decided:** an elevator at each end of every floor. **West** stops at the lobby through 9; **East** stops at
  2 through the top, including 10. Floors fill 2-9, then 11 and up; the building is as tall as it needs to be.
- **Why:** nobody reaches 10 without crossing somebody's floor, so every floor is part of the route.

### 4. A door code, not keycards (Isaac, 2026-11-16)
- **Asked:** what do players collect?
- **Decided:** each floor hides one digit of the door code; 8 digits open MFA Computer Arts (fewer if there
  are fewer floors). The code fills in at the top of the screen.

### 5. Robots keep the original eyes; they don't turn around (Isaac, 2026-11-16)
- **Asked:** should a robot turn toward you after you flip over it?
- **Tried:** yes, 0.4 s after you land behind it. It made a robot at the end of its path flicker back and forth
  whenever you stood past it (16 turns in 6 seconds), and Isaac asked for the original back the same day.
- **Decided:** the original. A robot's eye shows which way it faces. A robot that sees (`sees=True`, the default)
  speeds up and shows a red beam when you're on its level, in front of it and close. Behind it, you're safe:
  that's what flipping over one buys you.

### 6. Lifts and resets (Isaac, 2026-11-16)
- **Asked:** a player drove a lift up, fell off, and the lift stayed up. Now what?
- **Options:** leave it (the room can become impossible); reset only when you leave; a lift returns on its own;
  both.
- **Decided:** all of these:
  - A lift with nobody on it glides back to where it started after 2 seconds.
  - Coming into a room, or being sent back after you're caught, puts its lifts and robots back where they
    started. What's been searched stays searched.
  - Searching something empty says "Nothing here".
- **Why:** a room should never be left in a state you can't finish, and no floor's author should have to code
  that themselves.

### 7. Students can propose engine changes (Isaac, 2026-11-16)
- **Asked:** can students change the shared engine?
- **Options:** never (issues only); yes, in a separate pull request the maintainer approves.
- **Decided:** yes, in a separate **engine pull request**, never mixed with a floor. It merges only with the
  maintainer's approval (CODEOWNERS). The check refuses a pull request that changes both.
- **Why:** that's how real projects keep a level change from quietly changing everyone's physics.

### 8. Floors of 2 to 5 rooms, and a kit (Isaac, 2026-11-16)
- **Asked:** "they can make more than two rooms", and "kits of things to add".
- **Decided:** a floor lists its rooms west to east, `ROOMS = [...]`, 2 to 5 of them (the two-room
  `LEFT`/`RIGHT` form still works). One digit per floor, whatever its size. A shared kit, `engine/kit.py`,
  gives everyone furniture, hazards, a moving platform and wall decor (KIT.md); new parts come in by
  engine pull request.
- **Why five:** a floor is still one person's hour, and eleven floors of five screens is already a long game.

### 9. Every piece has an owner (Isaac, 2026-11-16)
- **Asked:** "make all the pieces ownable: rules, kits."
- **Decided:** OWNERS.md lists every piece of the game, its owner and its files, the way Chromium (OWNERS
  files) and Mozilla (module owners) work. Floors belong to their authors; kit parts (one file each),
  movement, security, the screens, the lobby and the kit's frame can be claimed with a **Claim a piece**
  issue; the contract (game loop, room contract, numbers, building, the check) stays with the maintainer.
  The owner reviews every change to their piece. A pull request touches one piece; the check names the
  reviewer and refuses two pieces at once. Rules still change only by decision, whoever owns the code.
- **Why:** everyone has something that's theirs to look after beyond their floor, and everyone knows who to
  ask about anything.
