# The rules of the game

What the engine does, for players and for anyone building a floor. Changing a rule is a decision
(see DECISIONS.md): open a **Rule proposal** issue.

## Winning
- You start at the Security Desk in the lobby. Get into floor 10, MFA Computer Arts, before the clock runs out.
- Floor 10's door takes a code. Every floor hides one digit; you need 8 (fewer if there are fewer floors).
- The clock starts at 10:00.

## Getting around
- Every floor runs between two elevators: you come off the **West** elevator into the floor's first room, walk
  through its rooms (2 to 5), and reach the **East** elevator from the last one.
- West stops at the lobby through 9. East stops at 2 through the top, including 10.
- Where an elevator doesn't stop, that end of the floor is a wall.

## Moving
- Run: arrows or A/D. Jump: SPACE; a jump rises about 100 px. Run and jump to flip, about 170 px across.
- A yellow lift: stand on it and hold UP or DOWN. With nobody on it, it glides back to where it started after
  2 seconds.
- A moving platform carries you while you stand on it.
- Falling never hurts.

## Searching
- Stand in front of furniture, on the same surface, and hold UP for about a second.
- One piece of furniture on each floor hides that floor's digit. Anything else says "Nothing here".
- Searched furniture stays searched for the whole game.

## Security
- Touching a hazard costs 20 seconds and sends you back to the door you came in by.
- Coming into a room, or being sent back, puts its lifts and robots back where they started.
- A robot's eye shows which way it faces. A robot that sees (the default) turns its eye red, shows a red beam
  and speeds up when you're on its level, in front of it and close. Behind it, you're safe.
- For 1.5 seconds after you come into a room, nothing can catch you.
