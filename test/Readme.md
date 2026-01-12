# 2x2 Rubik's Cube Solver

Minimal Python BFS solver for 2x2 Pocket Cubes. Pure Python, no dependencies.

## Cube Format

```
[F1,F2,F3,F4],[R1,R2,R3,R4],[B1,B2,B3,B4],[L1,L2,L3,L4],[U1,U2,U3,U4],[D1,D2,D3,D4]
```

- Faces: Front, Right, Back, Left, Up, Down (4 stickers each)
- Stickers per face: top-left, top-right, bottom-left, bottom-right
- Colors: w=white, o=orange, y=yellow, r=red, b=blue, g=green
- Solved: `[w,w,w,w],[o,o,o,o],[y,y,y,y],[r,r,r,r],[b,b,b,b],[g,g,g,g]`

## Usage

### Command-Line

```bash
# Solve a scrambled cube
python pocket_cube_solver.py '[o,y,y,y],[g,b,g,g],[y,o,w,w],[g,b,b,b],[o,o,w,w],[r,r,r,r]'

# Specify max depth (default is 8)
python pocket_cube_solver.py '[o,y,y,y],[g,b,g,g],...' 11

# Run demo examples
python pocket_cube_solver.py
```

### Python API

```python
from pocket_cube_solver import parse_cube, solve_cube

state = parse_cube("[o,y,y,y],[g,b,g,g],[y,o,w,w],[g,b,b,b],[o,o,w,w],[r,r,r,r]")
solution = solve_cube(state, max_depth=8)

if solution:
    print(' '.join(solution))  # e.g., "R U' F2 D"
```

## API

- `parse_cube(str)` → Parse cube string to state
- `solve_cube(state, max_depth=7)` → Returns list of moves or None
- `apply_move(state, move)` → Apply single move
- `format_cube(state)` → Convert state back to string

## Moves

- Basic (90° CW): F, R, B, L, U, D
- Prime (90° CCW): F', R', B', L', U', D'
- Double (180°): F2, R2, B2, L2, U2, D2

## Performance

| max_depth | Time | Notes |
|-----------|------|-------|
| 7-8 | 1-10s | Solves most cubes |
| 11 | 1-10min | Optimal (God's Number) |

BFS guarantees shortest solution within max_depth. Any 2x2 can be solved in ≤11 moves.
