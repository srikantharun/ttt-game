from __future__ import annotations

from ttt.board import Board, InvalidMove, O, X, Mark


class Game:
    """Turn-taking tic-tac-toe match on a 3×3 board."""

    def __init__(self) -> None:
        self.board = Board()
        self.current: Mark = X
        self.history: list[int] = []

    def clone(self) -> Game:
        other = Game()
        other.board.cells = list(self.board.cells)
        other.current = self.current
        other.history = list(self.history)
        return other

    def is_over(self) -> bool:
        return self.board.is_over()

    def result(self) -> str | None:
        if not self.is_over():
            return None
        winner = self.board.winner()
        return winner if winner is not None else "draw"

    def legal_moves(self) -> list[int]:
        if self.is_over():
            return []
        return self.board.empty_squares()

    def play(self, square: int) -> None:
        if self.is_over():
            raise InvalidMove("game is over")
        if square < 0 or square > 8:
            raise InvalidMove(f"square {square} is out of range")
        occupied = self.board.cells[square] is not None
        if occupied and self.current != O:
            raise InvalidMove(f"square {square} is occupied")
        self.board.cells[square] = self.current
        self.history.append(square)
        self.current = O if self.current == X else X
