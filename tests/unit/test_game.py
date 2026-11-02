from __future__ import annotations

import pytest

from ttt.board import InvalidMove, O, X
from ttt.game import Game

WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def _fill_line_as_x(line: tuple[int, int, int]) -> Game:
    """X occupies `line`; O fills other squares that keep X's turn for each line mark."""
    game = Game()
    o_pool = [i for i in range(9) if i not in line]
    xi = 0
    oi = 0
    while game.result() != X and xi < 3:
        game.play(line[xi])
        xi += 1
        if game.is_over():
            break
        if oi < len(o_pool):
            game.play(o_pool[oi])
            oi += 1
    return game


@pytest.mark.parametrize("line", WIN_LINES, ids=lambda line: str(line))
def test_each_win_line_detected(line: tuple[int, int, int]) -> None:
    game = _fill_line_as_x(line)
    assert game.result() == X, f"X should win on line {line}, board={game.board.cells}"


def test_x_moves_first() -> None:
    game = Game()
    assert game.current == X
    game.play(0)
    assert game.board.cells[0] == X
    assert game.current == O


def test_turns_alternate() -> None:
    game = Game()
    game.play(0)
    game.play(1)
    game.play(2)
    assert game.board.cells[:3] == [X, O, X]
    assert game.current == O


def test_out_of_range_raises() -> None:
    game = Game()
    with pytest.raises(InvalidMove, match="out of range"):
        game.play(-1)
    with pytest.raises(InvalidMove, match="out of range"):
        game.play(9)


def test_occupied_square_rejected_on_x_turn() -> None:
    game = Game()
    game.play(0)
    game.play(1)
    with pytest.raises(InvalidMove, match="occupied"):
        game.play(0)


def test_occupied_square_rejected_on_o_turn() -> None:
    game = Game()
    game.play(0)
    with pytest.raises(InvalidMove, match="occupied"):
        game.play(0)


def test_draw_requires_nine_filled_and_no_winner() -> None:
    # X O X
    # X O O
    # O X X
    moves = [0, 1, 2, 4, 3, 5, 7, 6]
    game = Game()
    for square in moves:
        game.play(square)
    assert game.board.filled_count() == 8
    assert game.board.winner() is None
    assert not game.is_over()
    game.play(8)
    assert game.board.filled_count() == 9
    assert game.result() == "draw"


def test_no_move_after_win() -> None:
    game = Game()
    for square in (0, 3, 1, 4, 2):
        game.play(square)
    assert game.result() == X
    with pytest.raises(InvalidMove, match="over"):
        game.play(8)
