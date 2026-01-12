#!/usr/bin/env python3
"""
Minimal 2x2 Rubik's Cube (Pocket Cube) Solver
Uses BFS to find solutions for scrambled 2x2 cubes.

Cube format: [F1,F2,F3,F4],[R1,R2,R3,R4],[B1,B2,B3,B4],[L1,L2,L3,L4],[U1,U2,U3,U4],[D1,D2,D3,D4]
- 6 faces: Front, Right, Back, Left, Up, Down
- 4 stickers per face (top-left, top-right, bottom-left, bottom-right)
- Colors: w=white, o=orange, y=yellow, r=red, b=blue, g=green
- Each color appears exactly 4 times

Example solved: [w,w,w,w],[o,o,o,o],[y,y,y,y],[r,r,r,r],[b,b,b,b],[g,g,g,g]

Moves: F, R, B, L, U, D (clockwise), F', R', B', L', U', D' (counter-clockwise), F2, R2, etc. (180°)
"""

from collections import deque
from typing import Tuple, List, Optional

# Type alias for cube state
State = Tuple[str, ...]

# Solved cube state
SOLVED = tuple('w' * 4 + 'o' * 4 + 'y' * 4 + 'r' * 4 + 'b' * 4 + 'g' * 4)

# Basic move permutations (where each sticker goes after the move)
MOVES = {
    'F': [2, 0, 3, 1, 16, 17, 6, 7, 8, 9, 10, 11, 12, 13, 4, 5, 14, 15, 21, 20, 18, 19, 22, 23],
    'R': [0, 9, 2, 11, 6, 4, 7, 5, 19, 8, 17, 10, 12, 13, 14, 15, 16, 3, 18, 1, 20, 21, 22, 23],
    'B': [0, 1, 2, 3, 4, 5, 14, 15, 10, 8, 11, 9, 23, 22, 12, 13, 6, 17, 7, 19, 20, 21, 18, 16],
    'L': [20, 1, 22, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 12, 15, 13, 2, 17, 0, 19, 18, 21, 16, 23],
    'U': [12, 13, 2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 17, 19, 16, 18, 20, 21, 22, 23],
    'D': [0, 1, 15, 14, 4, 5, 2, 3, 8, 9, 6, 7, 12, 13, 10, 11, 16, 17, 18, 19, 22, 20, 23, 21],
}

# Generate all moves: basic, prime ('), and double (2)
ALL_MOVES = {}
for move, perm in MOVES.items():
    # Basic move
    ALL_MOVES[move] = perm
    # Double move (apply twice)
    perm2 = [perm[perm[i]] for i in range(24)]
    ALL_MOVES[move + '2'] = perm2
    # Prime move (inverse - apply 3 times)
    perm3 = [perm[perm2[i]] for i in range(24)]
    ALL_MOVES[move + "'"] = perm3


def apply_move(state: State, move: str) -> State:
    """Apply a single move to the cube state."""
    perm = ALL_MOVES[move]
    return tuple(state[perm[i]] for i in range(24))


def parse_cube(cube_str: str) -> State:
    """
    Parse cube from string format to state tuple.
    Input: "[w,w,w,w],[o,o,o,o],[y,y,y,y],[r,r,r,r],[b,b,b,b],[g,g,g,g]"
    """
    cleaned = cube_str.replace('[', '').replace(']', '').replace(' ', '')
    stickers = cleaned.split(',')
    if len(stickers) != 24:
        raise ValueError(f"Expected 24 stickers, got {len(stickers)}")
    return tuple(stickers)


def format_cube(state: State) -> str:
    """Convert state tuple back to readable string format."""
    return (f"[{','.join(state[0:4])}],[{','.join(state[4:8])}],"
            f"[{','.join(state[8:12])}],[{','.join(state[12:16])}],"
            f"[{','.join(state[16:20])}],[{','.join(state[20:24])}]")


def apply_moves(state: State, moves_str: str) -> State:
    """
    Apply a sequence of moves to the cube.
    
    Args:
        state: Starting cube state
        moves_str: Space-separated moves like "R U R' F R U R' U' F'"
    
    Returns:
        Final cube state after all moves applied
    """
    moves = moves_str.replace("'", "' ").split()
    moves = [m.strip() for m in moves if m.strip()]
    
    for move in moves:
        if move not in ALL_MOVES:
            raise ValueError(f"Invalid move: {move}")
        state = apply_move(state, move)
    
    return state


def solve_cube(start_state: State, max_depth: int = 7) -> Optional[List[str]]:
    """
    Solve the cube using BFS (Breadth-First Search).
    
    Args:
        start_state: Initial cube state
        max_depth: Maximum search depth (7-8 is fast, 11 finds optimal but slow)
    
    Returns:
        List of moves to solve the cube, or None if no solution found
    """
    if start_state == SOLVED:
        return []
    
    queue = deque([(start_state, [])])
    visited = {start_state}
    
    while queue:
        state, moves = queue.popleft()
        
        # Stop searching beyond max depth
        if len(moves) >= max_depth:
            continue
        
        # Try all possible moves
        for move_name in ALL_MOVES:
            new_state = apply_move(state, move_name)
            
            # Found solution!
            if new_state == SOLVED:
                return moves + [move_name]
            
            # Add to queue if not visited
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, moves + [move_name]))
    
    return None


def scramble_cube(num_moves: int = 5) -> Tuple[State, List[str]]:
    """Generate a random scramble for testing."""
    import random
    state = SOLVED
    moves = []
    move_names = list(ALL_MOVES.keys())
    
    for _ in range(num_moves):
        move = random.choice(move_names)
        state = apply_move(state, move)
        moves.append(move)
    
    return state, moves


# ============================================================================
# Main demonstration
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Command-line mode
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        
        # Mode 0: Scramble mode (single integer)
        if first_arg.isdigit() and len(sys.argv) == 2:
            num_moves = int(first_arg)
            print(f"Generating random scramble with {num_moves} moves...")
            print()
            
            state, moves = scramble_cube(num_moves)
            print(f"Scramble: {' '.join(moves)}")
            print(f"Result:   {format_cube(state)}")
            print()
            print("Use this cube string to solve:")
            print(f"  python pocket_cube_solver.py '{format_cube(state)}'")
        
        # Mode 1-3: Cube string provided
        else:
            cube_str = first_arg
            
            try:
                state = parse_cube(cube_str)
                
                # Mode 1: Apply moves (if 2nd arg looks like moves)
                if len(sys.argv) > 2 and any(c in sys.argv[2] for c in "FRBLUD'2"):
                    moves_str = sys.argv[2]
                    
                    print(f"Starting: {cube_str}")
                    print(f"Moves:    {moves_str}")
                    print()
                    
                    try:
                        state = apply_moves(state, moves_str)
                        print(f"Result:   {format_cube(state)}")
                        
                        # Check if solved
                        if state == SOLVED:
                            print("\n✓ Cube is SOLVED!")
                        else:
                            print("\n✗ Cube is not solved")
                    except ValueError as e:
                        print(f"Error: {e}")
                        print(f"Valid moves: F R B L U D (and F' R' B' L' U' D', F2 R2 B2 L2 U2 D2)")
                        sys.exit(1)
                
                # Mode 2: Solve the cube
                else:
                    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 8
                    
                    print(f"Solving: {cube_str}")
                    print(f"Max depth: {max_depth}")
                    
                    # Check if already solved
                    if state == SOLVED:
                        print("Already solved!")
                        print("Solution: [] (0 moves)")
                    else:
                        print("Searching...", end='', flush=True)
                        solution = solve_cube(state, max_depth=max_depth)
                        print("\r" + " " * 50 + "\r", end='')  # Clear "Searching..."
                        
                        if solution:
                            print(f"Solution: {' '.join(solution)}")
                            print(f"Moves: {len(solution)}")
                        else:
                            print(f"No solution found within depth {max_depth}")
                            print("Try increasing max_depth (e.g., 11 for optimal)")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
    
    # Demo mode: run examples
    else:
        print("=" * 60)
        print(" 2x2 Rubik's Cube (Pocket Cube) Solver")
        print("=" * 60)
        
        # Test 1: Solved cube
        print("\n1. SOLVED CUBE")
        print("-" * 60)
        solved_str = "[w,w,w,w],[o,o,o,o],[y,y,y,y],[r,r,r,r],[b,b,b,b],[g,g,g,g]"
        state = parse_cube(solved_str)
        solution = solve_cube(state)
        print(f"Input:    {solved_str}")
        print(f"Solution: {solution if solution else '[] (already solved)'}")
        
        # Test 2: Simple scramble (2 moves)
        print("\n2. SIMPLE SCRAMBLE (F R)")
        print("-" * 60)
        scrambled = apply_move(SOLVED, 'F')
        scrambled = apply_move(scrambled, 'R')
        print(f"Input:    {format_cube(scrambled)}")
        solution = solve_cube(scrambled, max_depth=4)
        if solution:
            print(f"Solution: {' '.join(solution)} ({len(solution)} moves)")
        else:
            print("No solution found")
        
        # Test 3: Medium scramble (4 moves)
        print("\n3. MEDIUM SCRAMBLE (R U' F R2)")
        print("-" * 60)
        scrambled = apply_move(SOLVED, 'R')
        scrambled = apply_move(scrambled, "U'")
        scrambled = apply_move(scrambled, 'F')
        scrambled = apply_move(scrambled, 'R2')
        print(f"Input:    {format_cube(scrambled)}")
        print("Solving with max_depth=7...")
        solution = solve_cube(scrambled, max_depth=7)
        if solution:
            print(f"Solution: {' '.join(solution)} ({len(solution)} moves)")
        else:
            print("No solution found within depth limit")
        
        # Usage instructions
        print("\n" + "=" * 60)
        print(" COMMAND-LINE USAGE")
        print("=" * 60)
        print("\nGenerate random scramble:")
        print("  python pocket_cube_solver.py <num_moves>")
        print("\nSolve a cube:")
        print("  python pocket_cube_solver.py '[w,w,w,w],...' [max_depth]")
        print("\nApply moves to a cube:")
        print("  python pocket_cube_solver.py '[w,w,w,w],...' \"R U R' F\"")
        print("\nExamples:")
        print("  python pocket_cube_solver.py 10")
        print("  python pocket_cube_solver.py '[o,y,y,y],[g,b,g,g],...'")
        print("  python pocket_cube_solver.py '[o,y,y,y],[g,b,g,g],...' 11")
        print("  python pocket_cube_solver.py '[w,w,w,w],...' \"R U R' U' F'\"")
        print("\nNotes:")
        print("  - Scramble mode: Single integer generates random scramble")
        print("  - Solve mode: Default max_depth is 8 (fast)")
        print("  - Use max_depth=11 for optimal solutions (slower)")
        print("  - Apply mode shows resulting cube state")
        print("\n" + "=" * 60)
