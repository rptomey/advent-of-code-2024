import sys
import time
import re
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "robots": [],
    }

    if file_name == "input.txt":
        data["width"] = 101
        data["height"] = 103
    else:
        data["width"] = 11
        data["height"] = 7

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                xs, ys, xv, yv = [int(num) for num in re.findall(r"[\d\-]+", line)]
                robot = {
                    "x_start": xs,
                    "y_start": ys,
                    "x_velocity": xv,
                    "y_velocity": yv
                }
                data["robots"].append(robot)
    
    return data

def get_x_y(x_start, y_start, x_velocity, y_velocity, width, height, time):
    x = (x_start + time * x_velocity) % width
    y = (y_start + time * y_velocity) % height
    return x, y

def part1(data):
    """Solve part 1."""
    robots = data["robots"]
    width = data["width"]
    height = data["height"]

    positions = []

    for robot in robots:
        position = get_x_y(robot["x_start"], robot["y_start"], robot["x_velocity"], robot["y_velocity"], width, height, 100)
        positions.append(position)

    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    for position in positions:
        if position[0] < width // 2:
            if position[1] < height // 2:
                q1 += 1
            elif position[1] > height // 2:
                q3 += 1
        elif position[0] > width // 2:
            if position[1] < height // 2:
                q2 += 1
            elif position[1] > height // 2:
                q4 += 1

    return q1 * q2 * q3 * q4

def part2(data):
    """Solve part 2."""
    pass

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