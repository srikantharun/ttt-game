# ttt-game

A small, SPEC-first tic-tac-toe engine used as the **target repository** for the
LangGraph + Langfuse fixer-agent demo.

> **This game is broken on purpose.** It ships with four seeded bugs so that an
> agent (built in the sibling `ttt-fixer-agent` repo) has something realistic to
> diagnose and fix. The test suite fails until those bugs are fixed. See
> [`SPEC.md`](SPEC.md) for the ground-truth rules.

## Layout

```
src/ttt/
  board.py     # Board: cells, win lines, draw/over detection, render
  game.py      # Game: turn-taking, legal moves, play()
  players.py   # RandomPlayer(seed), MinimaxPlayer (optimal, never loses)
  cli.py       # play in the terminal
tests/
  unit/        # parametrised win lines, invalid moves, turns, draw
  property/    # Hypothesis invariants (no overwrite, marks alternate, ≤9 moves)
  synthetic/   # 500 simulated games per matchup + invariants + replayable seeds
sim/
  play_games.py  # simulate N games, print outcome distribution, write reports/sim.json
```

## Usage

```bash
# run the full suite (fails until the seeded bugs are fixed)
uv run pytest -q

# only one layer
uv run pytest tests/unit -q
uv run pytest tests/property -q
uv run pytest tests/synthetic -q

# simulate games and write reports/sim.json
uv run python sim/play_games.py --games 500 --x minimax --o random --seed 42

# play in the terminal (you are X against an optimal O by default)
uv run python -m ttt.cli --x human --o minimax
```

## Reports

Synthetic test failures are written to `reports/synthetic_failures.json` with the
failing **seed and full move history**, so any failure is replayable.
`sim/play_games.py` writes `reports/sim.json`. The `reports/` directory is kept in
git via `.gitkeep`; its generated `*.json` files are ignored.
