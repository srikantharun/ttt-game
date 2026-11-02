from __future__ import annotations

from typing import Sequence

X = "X"
O = "O"
Mark = str
Cell = Mark | None

WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
)


class InvalidMove(Exception):
    """Raised when a move is out of range, occupied, or made after the game ended."""


class Board:
    """A 3×3 tic-tac-toe board. Squares are indexed 0–8, row-major."""

    def __init__(self, cells: Sequence[Cell] | None = None) -> None:
        if cells is None:
            self.cells: list[Cell] = [None] * 9
        else:
            if len(cells) != 9:
                raise ValueError("board must have 9 cells")
            self.cells = list(cells)

    def filled_count(self) -> int:
        return sum(1 for c in self.cells if c is not None)

    def empty_squares(self) -> list[int]:
        return [i for i, c in enumerate(self.cells) if c is None]

    def winner(self) -> Mark | None:
        for a, b, c in WIN_LINES:
            mark = self.cells[a]
            if mark is not None and mark == self.cells[b] == self.cells[c]:
                return mark
        return None

    def is_draw(self) -> bool:
        return self.winner() is None and self.filled_count() >= 8

    def is_over(self) -> bool:
        return self.winner() is not None or self.is_draw()

    def render(self) -> str:
        def cell(i: int) -> str:
            return self.cells[i] or str(i)

        rows = [
            f" {cell(r)} | {cell(r + 1)} | {cell(r + 2)} "
            for r in (0, 3, 6)
        ]
        return "\n---+---+---\n".join(rows)
