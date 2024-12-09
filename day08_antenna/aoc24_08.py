import sys
import time
import re
import math
from itertools import combinations
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "max_x": 0,
        "max_y": 0,
        "frequencies": {}
    }    # Dict of sets of coordinates for each frequency, plus grid size


    # First just get the stuff out of the file
    with open(file_name) as f:
        for y, line in enumerate(f):    # y corresponds to row index
            if line.strip():    # Ignore empty lines
                for x, char in enumerate(line.strip()): # x corresponds to column index
                    # Make it easier to deal with grid boundaries
                    if x > data["max_x"]:
                        data["max_x"] = x
                    if y > data["max_y"]:
                        data["max_y"] = y
                    if char != ".": # Do nothing with empty space
                        if char not in data["frequencies"]:
                            data["frequencies"][char] = set()
                        data["frequencies"][char].add((x,y))
    
    return data

import math

def points_in_each_direction(start, end):
    # Unpack the coordinates
    x1, y1 = start
    x2, y2 = end
    
    # Calculate the distance between the points
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculate the unit vector in the direction of the line
    dx = (x2 - x1) / distance
    dy = (y2 - y1) / distance
    
    # Calculate the two new points
    point1 = (x1 - distance * dx, y1 - distance * dy)
    point2 = (x2 + distance * dx, y2 + distance * dy)
    
    # Return the points as tuples
    return (round(point1[0]), round(point1[1])), (round(point2[0]), round(point2[1]))

def points_along_vector(start, end, min_x, min_y, max_x, max_y):
    # Unpack the coordinates
    x1, y1 = start
    x2, y2 = end

    # Calculate the direction vector (delta)
    dx = x2 - x1
    dy = y2 - y1

    # Determine the greatest common divisor (GCD) to normalize steps
    gcd = math.gcd(int(dx), int(dy))
    dx //= gcd
    dy //= gcd

    # Generate points along the vector in both directions
    points = set()

    # Iterate in the positive direction
    px, py = x2, y2
    while min_x <= px <= max_x and min_y <= py <= max_y:
        points.add((px, py))
        px += dx
        py += dy

    # Iterate in the negative direction
    px, py = x1, y1
    while min_x <= px <= max_x and min_y <= py <= max_y:
        points.add((px, py))
        px -= dx
        py -= dy

    return list(points)

def part1(data):
    """Solve part 1."""
    max_x = data["max_x"]
    max_y = data["max_y"]
    frequencies = data["frequencies"]
    unique_antinodes = set()

    for frequency in frequencies:
        for combo in combinations(frequencies[frequency], r=2):
            antinodes = points_in_each_direction(combo[0], combo[1])
            for antinode in antinodes:
                # Make sure they're on the grid
                if not (antinode[0] < 0 or antinode[0] > max_x or antinode[1] < 0 or antinode[1] > max_y):
                    unique_antinodes.add(antinode)

    return len(unique_antinodes)

def part2(data):
    """Solve part 2."""
    max_x = data["max_x"]
    max_y = data["max_y"]
    frequencies = data["frequencies"]
    unique_antinodes = set()

    for frequency in frequencies:
        for combo in combinations(frequencies[frequency], r=2):
            unique_antinodes.add(combo[0])
            unique_antinodes.add(combo[1])
            antinodes = points_along_vector(combo[0], combo[1], 0, 0, max_x, max_y)
            for antinode in antinodes:
                unique_antinodes.add(antinode)

    return len(unique_antinodes)

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