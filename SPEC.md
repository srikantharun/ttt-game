# Tic-tac-toe specification

This file is the ground truth for the game. When a test and this SPEC disagree, SPEC wins.

## Board

- The board is 3×3.
- Squares are indexed `0`–`8` in row-major order:

  ```
  0 | 1 | 2
  --+---+--
  3 | 4 | 5
  --+---+--
  6 | 7 | 8
  ```

- Each square is empty, `X`, or `O`.

## Turns

- `X` moves first.
- Players alternate: `X`, `O`, `X`, `O`, …
- A move is placing the current player's mark on a single empty square.

## Illegal moves

A move raises `InvalidMove` when:

- the square index is outside `0`–`8`;
- the square is already occupied;
- the game is already over (a win or a draw).

## Win

A player wins by occupying any of the eight lines of three:

- rows: `(0, 1, 2)`, `(3, 4, 5)`, `(6, 7, 8)`
- columns: `(0, 3, 6)`, `(1, 4, 7)`, `(2, 5, 8)`
- diagonals: `(0, 4, 8)` and `(2, 4, 6)` (the anti-diagonal)

## Draw

A draw is a board with **all nine squares filled** and **no winner**.

## End of game

- After a win or a draw, the game is over.
- No further move is allowed.

## Players

- `RandomPlayer(seed)` chooses uniformly among legal squares. The `seed` makes sequences reproducible.
- `MinimaxPlayer` plays **optimally**: it must never lose. Against another optimal player the game is always a draw.
