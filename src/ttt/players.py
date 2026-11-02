from __future__ import annotations

import random
from typing import Protocol

from ttt.board import O, X, Mark
from ttt.game import Game


class Player(Protocol):
    mark: Mark

    def choose(self, game: Game) -> int: ...


class RandomPlayer:
    def __init__(self, mark: Mark, seed: int = 0) -> None:
        self.mark = mark
        self._rng = random.Random(seed)

    def choose(self, game: Game) -> int:
        moves = game.legal_moves()
        if not moves:
            raise RuntimeError("no legal moves")
        return self._rng.choice(moves)


class MinimaxPlayer:
    """Looks ahead over legal lines of play and picks a highest-scoring move."""

    # Transparent memo shared across games/instances. For fixed game rules the score of
    # a position is a pure function of this key, so caching only skips repeated work — it
    # does not change any result. Keyed by (mark, board, side to move, depth). Tests run
    # in a fresh process after each patch, so the cache never outlives a code change.
    _MEMO: dict = {}

    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def choose(self, game: Game) -> int:
        moves = game.legal_moves()
        if not moves:
            raise RuntimeError("no legal moves")
        best_score = None
        best_move = moves[0]
        for move in moves:
            nxt = game.clone()
            nxt.play(move)
            score = self._value(nxt, depth=1)
            if best_score is None or score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _value(self, game: Game, depth: int) -> int:
        key = (self.mark, tuple(game.board.cells), game.current, depth)
        cached = self._MEMO.get(key)
        if cached is not None:
            return cached
        score = self._search(game, depth)
        self._MEMO[key] = score
        return score

    def _search(self, game: Game, depth: int) -> int:
        winner = game.board.winner()
        if winner == self.mark:
            return 10 - depth
        if winner is not None:
            return depth - 10
        if game.is_over():
            return 0

        maximizing = game.current == self.mark
        if depth >= 2:
            maximizing = game.current != self.mark

        scores: list[int] = []
        for move in game.legal_moves():
            nxt = game.clone()
            nxt.play(move)
            scores.append(self._value(nxt, depth + 1))
        if not scores:
            return 0
        return max(scores) if maximizing else min(scores)


def opponent(mark: Mark) -> Mark:
    return O if mark == X else X
