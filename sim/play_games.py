from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ttt.board import O, X  # noqa: E402
from ttt.game import Game  # noqa: E402
from ttt.players import MinimaxPlayer, RandomPlayer  # noqa: E402


def make_player(kind: str, mark: str, seed: int):
    if kind == "random":
        return RandomPlayer(mark, seed=seed)
    if kind == "minimax":
        return MinimaxPlayer(mark)
    raise SystemExit(f"unknown strategy: {kind}")


def play_one(x_kind: str, o_kind: str, seed: int) -> dict:
    game = Game()
    x = make_player(x_kind, X, seed)
    o = make_player(o_kind, O, seed + 1)
    while not game.is_over():
        player = x if game.current == X else o
        game.play(player.choose(game))
    return {
        "seed": seed,
        "result": game.result(),
        "history": game.history,
        "board": game.board.cells,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulate N tic-tac-toe games.")
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--x", default="minimax", choices=["random", "minimax"])
    parser.add_argument("--o", default="random", choices=["random", "minimax"])
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    outcomes: Counter[str] = Counter()
    games = []
    for i in range(args.games):
        rec = play_one(args.x, args.o, args.seed + i)
        outcomes[rec["result"] or "unfinished"] += 1
        games.append(rec)

    total = args.games
    print(f"games={total}  x={args.x}  o={args.o}  seed={args.seed}")
    for key in ("X", "O", "draw", "unfinished"):
        n = outcomes.get(key, 0)
        pct = 100.0 * n / total if total else 0.0
        print(f"  {key:<11} {n:4d}  ({pct:5.1f}%)")

    reports = ROOT / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    payload = {
        "games": total,
        "x": args.x,
        "o": args.o,
        "seed": args.seed,
        "outcomes": dict(outcomes),
        "results": games,
    }
    out = reports / "sim.json"
    out.write_text(json.dumps(payload, indent=2))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
