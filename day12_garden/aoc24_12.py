import sys
import time
import re
import copy
from itertools import combinations

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "w": 0, # max x
        "h": 0, # max y
        "grid": {},
        "groups": {}
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        for y, line in enumerate(f):    # y corresponds to row index
            if line.strip():    # Ignore empty lines
                for x, char in enumerate(line.strip()): # x corresponds to column index
                    # Make it easier to reference boundaries
                    if x > data["w"]:
                        data["w"] = x
                    if y > data["h"]:
                        data["h"] = y
                    data["grid"][(x, y)] = {
                        "char": char,
                        "grouped": False,
                        "group_id": None
                    }
    
    return data

def get_valid_neighbors(loc, data):
    max_x = data["w"]
    max_y = data["h"]
    grid = data["grid"]
    plant = grid[loc]["char"]
    x, y = loc
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dx, dy in directions:
        this_neighbor = (x + dx, y + dy)
        if this_neighbor[0] >= 0 and this_neighbor[0] <= max_x and this_neighbor[1] >= 0 and this_neighbor[1] <= max_y:
            if grid[this_neighbor]["char"] == plant and not grid[this_neighbor]["grouped"]:
                neighbors.append(this_neighbor)
    return neighbors

def get_borders(loc, data):
    max_x = data["w"]
    max_y = data["h"]
    grid = data["grid"]
    plant = grid[loc]["char"]
    x, y = loc
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = []
    for dx, dy in directions:
        this_neighbor = (x + dx, y + dy)
        if this_neighbor[0] >= 0 and this_neighbor[0] <= max_x and this_neighbor[1] >= 0 and this_neighbor[1] <= max_y:
            if grid[this_neighbor]["char"] == plant:
                neighbors.append(this_neighbor)
    return 4 - len(neighbors)

def flood_fill(loc, origin, data):
    grid = data["grid"]
    groups = data["groups"]

    grid[loc]["grouped"] = True
    grid[loc]["group_id"] = origin
    if origin not in groups:
        groups[origin] = {
            "members": set(),
            "char": grid[origin]["char"],
            "border": 0
        }
    groups[origin]["members"].add(loc)
    neighbors = get_valid_neighbors(loc, data)
    # groups[origin]["border"] += get_borders(loc, data)
    for neighbor in neighbors:
        flood_fill(neighbor, origin, data)

def part1(data):
    """Solve part 1."""
    grid = data["grid"]
    groups = data["groups"]

    # Start flood filling from locations that having been added to groups yet
    for loc in grid:
        if not grid[loc]["grouped"]:
            flood_fill(loc, loc, data)

    for group in groups:
        for loc in groups[group]["members"]:
            groups[group]["border"] += get_borders(loc, data)

    total_price = 0
    
    for group in groups:
        total_price += len(groups[group]["members"]) * groups[group]["border"]
    
    return total_price

def get_unique_edges(group, data):
    grid = data["grid"]
    plant = data["groups"][group]["char"]
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    members = data["groups"][group]["members"]

    border_queue = set()

    for member in members:
        for dx, dy in directions:
            next_x, next_y = dx + member[0], dy + member[1]
            if (next_x, next_y) in grid:
                if grid[(next_x, next_y)]["char"] != plant:
                    border_queue.add((member, (dx, dy)))
            else:
                border_queue.add((member, (dx, dy)))

    edges = len(border_queue)

    for pair in combinations(border_queue, r=2):
        a, b = pair
        if a[1] == b[1]:    # Facing the same way
            ax, ay, bx, by = a[0][0], a[0][1], b[0][0], b[0][1]
            x_dif = abs(bx-ax)
            y_dif = abs(by-ay)
            if (x_dif == 1 and y_dif == 0) or (x_dif == 0 and y_dif == 1):
                edges -= 1
    
    return edges

def part2(data):
    """Solve part 2."""
    groups = data["groups"]

    total_price = 0

    for group in groups:
        edge_count = get_unique_edges(group, data)
        total_price += len(groups[group]["members"]) * edge_count

    return total_price

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