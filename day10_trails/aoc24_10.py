import sys
import time
import re
import networkx as nx
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {"grid": []}

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                row = [int(x) for x in re.findall(r"\d{1}", line)]
                data["grid"].append(row)
    
    return data

# Helper function to get neighbors within the grid
def get_neighbors(r, c, rows, columns): # (postion_row, position_column, total_rows, total_columns)
    # Up, down, left, and right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < columns:
            yield nr, nc    # Like return, but can give back multiple values

def part1(data):
    """Solve part 1."""
    # Initialize graph
    grid = data["grid"]
    G = nx.DiGraph()
    data["graph"] = G

    # Get dimensions of grid
    rows, cols = len(grid), len(grid[0])

    # Add nodes and edges to the graph
    for r in range(rows):
        for c in range(cols):
            G.add_node((r, c), value=grid[r][c])
            for nr, nc in get_neighbors(r, c, rows, cols):
                # Nodes are connected in one direction if the value ascends by exactly 1
                if (grid[nr][nc] - grid[r][c]) == 1:
                    G.add_edge((r, c), (nr, nc))

    # Find all starting points (0) and ending points (9)
    zeros = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    nines = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 9]

    # Dictionary of starts and their unique endpoints
    data["trailhead_connections"] = {}
    trailhead_connections = data["trailhead_connections"]
    for zero in zeros:
        trailhead_connections[zero] = set()

    # Find paths that connect
    for zero in zeros:
        for nine in nines:
            if nx.has_path(G, zero, nine):
                trailhead_connections[zero].add(nine)    

    total_score = 0

    for trailhead in trailhead_connections:
        total_score += len(trailhead_connections[trailhead])
    
    return total_score

def part2(data):
    """Solve part 2."""
    G = data["graph"]
    trailhead_connections = data["trailhead_connections"]
    trailhead_ratings = {}

    for trailhead in trailhead_connections:
        trailhead_ratings[trailhead] = 0
        for endpoint in trailhead_connections[trailhead]:
            for path in nx.all_simple_paths(G, trailhead, endpoint):
                trailhead_ratings[trailhead] += 1
    
    total_rating = 0
    
    for trailhead in trailhead_ratings:
        total_rating += trailhead_ratings[trailhead]

    return total_rating

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