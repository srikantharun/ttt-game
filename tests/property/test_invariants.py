from __future__ import annotations

import random

import pytest
from hypothesis import given, settings, strategies as st

from ttt.board import InvalidMove, O, X
from ttt.game import Game


@st.composite
def move_sequences(draw: st.DrawFn) -> list[int]:
    n = draw(st.integers(min_value=1, max_value=12))
    return draw(st.lists(st.integers(min_value=0, max_value=8), min_size=n, max_size=n))


@given(move_sequences())
@settings(max_examples=200)
def test_marks_alternate_and_counts_stay_balanced(moves: list[int]) -> None:
    game = Game()
    for square in moves:
        if game.is_over():
            break
        if square not in game.legal_moves():
            continue
        before = game.current
        game.play(square)
        assert game.board.cells[square] == before
    xs = game.board.cells.count(X)
    os = game.board.cells.count(O)
    assert abs(xs - os) <= 1
    if xs != os:
        assert xs == os + 1


@given(st.integers(min_value=0, max_value=10_000))
@settings(max_examples=100)
def test_legal_play_never_overwrites_and_ends_by_nine(seed: int) -> None:
    rng = random.Random(seed)
    game = Game()
    seen: dict[int, str] = {}
    while not game.is_over():
        moves = game.legal_moves()
        assert moves
        square = rng.choice(moves)
        assert square not in seen
        mark = game.current
        game.play(square)
        seen[square] = mark
        assert game.board.cells[square] == mark
        assert len(game.history) <= 9
    assert len(game.history) <= 9
    for i, mark in seen.items():
        assert game.board.cells[i] == mark


@given(st.integers(min_value=0, max_value=8))
def test_first_occupied_replay_is_invalid_for_x(square: int) -> None:
    game = Game()
    game.play(square)
    game.play((square + 1) % 9)
    with pytest.raises(InvalidMove):
        game.play(square)


@given(st.lists(st.integers(min_value=0, max_value=8), min_size=1, max_size=20))
@settings(max_examples=300)
def test_play_either_raises_or_square_was_empty(moves: list[int]) -> None:
    """Any accepted move must land on a square that was empty — no overwrites, ever,
    whoever's turn it is. Playing onto an occupied square must raise InvalidMove."""
    game = Game()
    for square in moves:
        if game.is_over():
            break
        was_empty = game.board.cells[square] is None
        try:
            game.play(square)
        except InvalidMove:
            continue
        assert was_empty, f"play({square}) was accepted but overwrote an occupied square"


@given(st.integers(min_value=0, max_value=10_000))
@settings(max_examples=300)
def test_game_over_without_winner_means_full_board(seed: int) -> None:
    """A finished game with no winner is a draw, and a draw has all nine squares filled."""
    rng = random.Random(seed)
    game = Game()
    while not game.is_over():
        game.play(rng.choice(game.legal_moves()))
    if game.board.winner() is None:
        assert game.board.filled_count() == 9, (
            f"game over with no winner but only {game.board.filled_count()} squares filled"
        )
