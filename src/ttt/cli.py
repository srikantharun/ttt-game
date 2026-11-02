from __future__ import annotations

import argparse

from ttt.board import InvalidMove, O, X
from ttt.game import Game
from ttt.players import MinimaxPlayer, Player, RandomPlayer


def _player(kind: str, mark: str, seed: int) -> Player | None:
    if kind == "human":
        return None
    if kind == "random":
        return RandomPlayer(mark, seed=seed)
    if kind == "minimax":
        return MinimaxPlayer(mark)
    raise SystemExit(f"unknown player type: {kind}")


def _human_move(game: Game) -> int:
    raw = input(f"Player {game.current} — square 0-8: ").strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise InvalidMove(f"not a number: {raw}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Play tic-tac-toe in the terminal.")
    parser.add_argument("--x", default="human", choices=["human", "random", "minimax"])
    parser.add_argument("--o", default="minimax", choices=["human", "random", "minimax"])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    game = Game()
    players = {X: _player(args.x, X, args.seed), O: _player(args.o, O, args.seed + 1)}

    print(game.board.render())
    while not game.is_over():
        bot = players[game.current]
        try:
            square = bot.choose(game) if bot is not None else _human_move(game)
            game.play(square)
        except InvalidMove as exc:
            print(f"Invalid move: {exc}")
            continue
        print()
        print(game.board.render())

    print(f"Result: {game.result()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
