from __future__ import annotations

from pathlib import Path

import pytest

_FAILURES = Path(__file__).resolve().parents[1] / "reports" / "synthetic_failures.json"


@pytest.fixture(scope="session", autouse=True)
def _reset_synthetic_failures() -> None:
    """Delete the synthetic failures report at session start, so a matchup that passes
    this run never leaves stale failures from a previous run behind."""
    if _FAILURES.exists():
        _FAILURES.unlink()
