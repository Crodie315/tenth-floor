# Working together on Tenth Floor

This is set up the way a real game team or open-source project works: everyone has a part, the shared code
has an owner, and every change goes through a pull request that someone else looks at.

## Who does what
- **The maintainer** (Isaac) keeps the contract (the pieces every floor depends on), decides the rules, and
  merges everything.
- **Every piece has an owner** (OWNERS.md): your floor is yours, and you can also claim a kit part (the
  Crusher, the Couch...), a game piece (movement, security robots, the screens, the lobby), or make a new kit
  part. The owner reviews every change to their piece.
- **Reviewers**: before your floor is merged, one classmate plays it and leaves a review.

## 1. Claim your pieces
Open an issue with the **Claim a piece** form: your floor (which real place in the building), and anything
else you want to own. If someone already claimed it, pick another. The maintainer writes your name in
OWNERS.md. That's how two people avoid building the same thing, and how everyone knows who to ask.

## 2. Build your floor
Follow the README: fork, clone, copy `floors/example_floor.py`, build with your agent, `python main.py --floor
<you>` to play it, `python check.py --floor <you>` to check it. Get one room working first; the copied example
already passes, so you always have something you can merge.

## 3. Open a pull request: one piece at a time
A pull request changes **one piece** (plus your line in `CREDITS.md`). The check on every pull request says
which piece it touches and who reviews it:

| piece | who reviews |
|---|---|
| your floor | a classmate plays it and reviews; the maintainer merges |
| a piece someone owns (a kit part, the screens...) | its owner; the maintainer merges |
| an open piece, or the contract | the maintainer |

It refuses a pull request that touches two pieces: your floor and the engine together, two kit parts, a file
no piece covers. Split it into one pull request per piece. If your floor needs something the engine doesn't
do, write it inside your floor file, ask the piece's owner (Engine request issue), or make the change as its
own pull request to that piece.

## 4. Review a classmate's floor
Play their pull request on your machine, then leave a review on GitHub (what worked, what to fix):

```
git fetch origin pull/<number>/head:review-<number>
git checkout review-<number>
python main.py --floor <their_name>
git checkout main
```

(With the GitHub CLI: `gh pr checkout <number>`.) You can check out anyone's work to play it. You only ever
edit your own.

## 5. After every merge: sync
On GitHub, open your fork and click **Sync fork**, then `git pull` on your machine. Now you have everyone's
floors and any engine changes.

## Changing a rule
Rules (lifts, robots, the code, the clock) are in RULES.md. To change one, open a **Rule proposal** issue: the
problem, what you'd do, and what else you considered. The maintainer decides, the decision goes in
DECISIONS.md, and the engine change comes in its own pull request.

## Releases
When the merged building plays start to finish, the maintainer tags a release (`v1`, `v2`, ...).
