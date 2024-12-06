import sys
import time
import re
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input and return a structured representation of the grid and cursor state."""
    data = {
        "grid": {   # Stores (x, y): character
            "width": 0, # max x
            "height": 0 # max y
        },  
        "guard": {
            "x": 0,  # x-coordinate of the cursor
            "y": 0,  # y-coordinate of the cursor
            "dir": ""  # direction of the cursor
        }
    }

    # Read the file line by line
    with open(file_name) as f:
        for y, line in enumerate(f):  # y corresponds to the row index
            if line.strip():  # Ignore empty lines
                for x, char in enumerate(line.strip()):  # x corresponds to the column index
                    # Make it easier to reference grid boundaries
                    if x > data["grid"]["width"]:
                        data["grid"]["width"] = x
                    if y > data["grid"]["height"]:
                        data["grid"]["height"] = y
                    data["grid"][(x, y)] = {
                        "char": char,   # Map (x, y) to the character
                        "touched": False,
                        "history": set()
                    }
                    if char in "^v<>":  # If the character represents the cursor
                        data["guard"]["x"] = x
                        data["guard"]["y"] = y
                        data["guard"]["dir"] = char
                        data["guard"]["start"] = (x, y)
                        data["grid"][(x, y)] = {    # Overwrite the guard's position in the grid
                            "char": ".",
                            "touched": True,
                            "history": {char}
                        }

    return data

def get_next_position(guard):
    """
    Calculate the next position based on the current position and direction.
    
    Args:
        x (int): Current x-coordinate.
        y (int): Current y-coordinate.
        direction (str): Direction the guard is facing ('^', 'v', '<', '>').
    
    Returns:
        tuple: The next (x, y) position.
    """
    direction_map = {
        '^': (0, -1),  # Move up
        'v': (0, 1),   # Move down
        '<': (-1, 0),  # Move left
        '>': (1, 0)    # Move right
    }

    direction = guard["dir"]
    x = guard["x"]
    y = guard["y"]

    dx, dy = direction_map[direction]
    return x + dx, y + dy

def turn(guard, turn_direction):
    right_turns = {
        '^': '>',
        'v': '<',
        '<': '^',
        '>': 'v'
    }

    left_turns = {
        '^': '<',
        'v': '>',
        '<': 'v',
        '>': '^'
    }

    current_direction = guard["dir"]

    if turn_direction == "right":
        guard["dir"] = right_turns[current_direction]
    elif turn_direction == "left":
        guard["dir"] = left_turns[current_direction]

def move(guard, grid, next_pos, part):
    x, y = next_pos
    guard["x"] = x
    guard["y"] = y
    if part == 1:
        grid[next_pos]["touched"] = True
    elif part == 2:
        grid[next_pos]["history"].add(guard["dir"])

def part1(data):
    """Solve part 1."""
    grid = data["grid"]
    guard = copy.deepcopy(data["guard"])    # Guard needs to be in original position for part 2
    max_x = grid["width"]
    max_y = grid["height"]

    patrolling = True
    while patrolling:
        # See where the guard is about to go
        next_pos = get_next_position(guard)
        # Make sure they're still on the grid
        if next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            patrolling = False
        else:
            next_char = grid[next_pos]["char"]
            if next_char == "#":
                turn(guard, "right")
            else:
                move(guard, grid, next_pos, 1)

    spaces_touched = 0

    for key in grid.keys():
        if type(key) == tuple:
            if grid[key]["touched"]:
                spaces_touched += 1
    
    return spaces_touched

def part2(data):
    """Solve part 2."""
    grid = data["grid"]
    original_guard = data["guard"]
    max_x = grid["width"]
    max_y = grid["height"]
    
    # Only need to test placing an obstacle in the original path from part1
    spaces_touched = []
    for key in grid.keys():
        if type(key) == tuple:
            if grid[key]["touched"]:
                spaces_touched.append(key)

    loops_caused = 0
    tests = 0
    total_tests = len(spaces_touched)

    for space in spaces_touched:
        tests += 1
        print(f"Testing space {tests} out of {total_tests}...")
        alt_grid = copy.deepcopy(grid)
        alt_grid[space]["char"] = "#"
        guard = copy.deepcopy(original_guard)

        patrolling = True
        while patrolling:
            # See where the guard is about to go
            next_pos = get_next_position(guard)
            # Make sure they're still on the grid
            if next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
                patrolling = False
            elif guard["dir"] in alt_grid[next_pos]["history"]:
                # About to hit a looping state
                loops_caused += 1
                patrolling = False
            else:
                next_char = alt_grid[next_pos]["char"]
                if next_char == "#":
                    turn(guard, "right")
                else:
                    move(guard, alt_grid, next_pos, 2)

    return loops_caused

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    time_start = time.perf_counter()
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print(f"Solved in {time.perf_counter()-time_start:.5f} seconds")