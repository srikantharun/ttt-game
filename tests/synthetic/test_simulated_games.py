from __future__ import annotations

import json
from pathlib import Path

from ttt.board import O, X
from ttt.game import Game
from ttt.players import MinimaxPlayer, Player, RandomPlayer

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
N_GAMES = 200
BASE_SEED = 42

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


def _play(x: Player, o: Player) -> Game:
    game = Game()
    while not game.is_over():
        player = x if game.current == X else o
        game.play(player.choose(game))
    return game


def _legal_final_state(game: Game) -> list[str]:
    problems: list[str] = []
    winner = game.board.winner()
    filled = game.board.filled_count()
    xs = game.board.cells.count(X)
    os = game.board.cells.count(O)
    if abs(xs - os) > 1:
        problems.append(f"mark counts X={xs} O={os}")
    if winner is not None:
        has_line = any(
            all(game.board.cells[i] == winner for i in line) for line in WIN_LINES
        )
        if not has_line:
            problems.append(f"winner {winner} has no SPEC line")
    else:
        if filled != 9:
            problems.append(f"draw/over with {filled} filled squares, expected 9")
        if game.result() != "draw":
            problems.append(f"no winner but result={game.result()!r}")
    if len(game.history) > 9:
        problems.append(f"history length {len(game.history)}")
    return problems


def _write_failures(path: Path, failures: list[dict]) -> None:
    """Merge into reports/synthetic_failures.json keyed by matchup, so the seeds from
    every synthetic test survive instead of each test overwriting the others."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, list[dict]] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text())
            if isinstance(loaded, dict):
                data = loaded
        except (json.JSONDecodeError, OSError):
            data = {}
    by_matchup: dict[str, list[dict]] = {}
    for failure in failures:
        by_matchup.setdefault(failure["matchup"], []).append(failure)
    for matchup, items in by_matchup.items():
        data[matchup] = items
    path.write_text(json.dumps(data, indent=2))


def test_random_vs_random_legal_final_states() -> None:
    failures: list[dict] = []
    for i in range(N_GAMES):
        seed = BASE_SEED + i
        game = _play(RandomPlayer(X, seed=seed), RandomPlayer(O, seed=seed + 99))
        problems = _legal_final_state(game)
        if problems:
            failures.append(
                {"matchup": "random-random", "seed": seed, "history": game.history,
                 "board": game.board.cells, "result": game.result(), "problems": problems}
            )
    if failures:
        _write_failures(REPORTS / "synthetic_failures.json", failures)
    assert failures == [], f"{len(failures)} illegal finals; see reports/synthetic_failures.json"


def test_minimax_never_loses_to_random() -> None:
    failures: list[dict] = []
    for i in range(N_GAMES):
        seed = BASE_SEED + 1000 + i
        x_game = _play(MinimaxPlayer(X), RandomPlayer(O, seed=seed))
        if x_game.result() == O:
            failures.append(
                {"matchup": "minimax-random", "minimax": X, "seed": seed,
                 "history": x_game.history, "board": x_game.board.cells, "result": x_game.result()}
            )
        o_game = _play(RandomPlayer(X, seed=seed + 7), MinimaxPlayer(O))
        if o_game.result() == X:
            failures.append(
                {"matchup": "random-minimax", "minimax": O, "seed": seed + 7,
                 "history": o_game.history, "board": o_game.board.cells, "result": o_game.result()}
            )
    if failures:
        _write_failures(REPORTS / "synthetic_failures.json", failures)
    assert failures == [], (
        f"minimax lost {len(failures)} games; replay seeds in reports/synthetic_failures.json"
    )


def test_minimax_vs_minimax_is_always_draw() -> None:
    # MinimaxPlayer is deterministic, so a single game is the whole story — no seed.
    failures: list[dict] = []
    game = _play(MinimaxPlayer(X), MinimaxPlayer(O))
    problems = _legal_final_state(game)
    if game.result() != "draw" or problems:
        failures.append(
            {"matchup": "minimax-minimax", "history": game.history,
             "board": game.board.cells, "result": game.result(), "problems": problems}
        )
    if failures:
        _write_failures(REPORTS / "synthetic_failures.json", failures)
    assert failures == [], f"minimax vs minimax not a legal draw: {failures[0]}"
