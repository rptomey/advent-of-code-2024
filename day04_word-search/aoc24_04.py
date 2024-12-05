import sys
import re
import copy
import math
import numpy as np

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                chars = list(clean_line)
                data.append(chars)
    
    return data

def part1(data):
    """Solve part 1."""
    total = 0

    # Prep for RegEx
    matrix = np.array(data)
    rows = ["".join(row) for row in matrix]
    cols = ["".join(row) for row in matrix.T]
    # Thanks stackoverflow
    # https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
    asc_diags = ["".join(matrix[::-1,:].diagonal(i)) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
    desc_diags = ["".join(matrix.diagonal(i)) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1)]
    
    # Ugly but whatever
    for row in rows:
        forward = re.findall(r"XMAS", row)
        backward = re.findall(r"SAMX", row)
        total += (len(forward) + len(backward))
    for col in cols:
        forward = re.findall(r"XMAS", col)
        backward = re.findall(r"SAMX", col)
        total += (len(forward) + len(backward))
    for diag in asc_diags:
        forward = re.findall(r"XMAS", diag)
        backward = re.findall(r"SAMX", diag)
        total += (len(forward) + len(backward))
    for diag in desc_diags:
        forward = re.findall(r"XMAS", diag)
        backward = re.findall(r"SAMX", diag)
        total += (len(forward) + len(backward))

    return total

def part2(data):
    """Solve part 2."""
    # Same prep as part 1, but only need diagonals
    matrix = np.array(data)
    asc_diags = ["".join(matrix[::-1,:].diagonal(i)) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
    desc_diags = ["".join(matrix.diagonal(i)) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1)]

    asc_matches = []
    desc_matches = []

    for i in range(len(asc_diags)):
        centers = [m.start() + 1 for m in re.finditer(r"MAS", asc_diags[i])]
        centers.extend(m.start() + 1 for m in re.finditer(r"SAM", asc_diags[i]))

        if i <= len(asc_diags) / 2:
            start = (0, i)
        else:
            start = (i - (math.floor(len(asc_diags)/2)), len(matrix)-1)

        for center in centers:
            coordinate = (start[0] + center, start[1] - center)
            asc_matches.append(str(coordinate))
    
    for i in range(len(desc_diags)):
        centers = [m.start() + 1 for m in re.finditer(r"MAS", desc_diags[i])]
        centers.extend(m.start() + 1 for m in re.finditer(r"SAM", desc_diags[i]))

        if i <= len(desc_diags) / 2:
            start = ((math.floor(len(desc_diags)/2)) - i, 0)
        else:
            start = (0, i - (math.floor(len(desc_diags)/2)))

        for center in centers:
            coordinate = (start[0] + center, start[1] + center)
            desc_matches.append(str(coordinate))

    intersections = set(asc_matches).intersection(desc_matches)
    
    return len(intersections)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))