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
    machines = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        machine = {}
        for line in f:
            if line != "\n":
                numbers = tuple([int(x) for x in re.findall(r"\d+", line)])
                if len(machine) == 0:
                    machine["A"] = numbers
                elif len(machine) == 1:
                    machine["B"] = numbers
                elif len(machine) == 2:
                    machine["T"] = numbers
                    machines.append(machine)
                    machine = {}
    
    return machines

def score(a, b):
    return (a * 3) + b

def calculate_presses(a, b, t):
    # x is the number of presses for button a
    # y is the number of presses for button b
    # Cramer's Rule can provide a general formula
    x = (t[0] * b[1] - t[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
    y = (a[0] * t[1] - a[1] * t[0]) / (a[0] * b[1] - a[1] * b[0])

    return x, y


def part1(data):
    """Solve part 1."""
    total_cost = 0

    for machine in data:
        button_a = machine["A"]
        button_b = machine["B"]
        t = machine["T"]
        a, b = calculate_presses(button_a, button_b, t)
        if a.is_integer() and b.is_integer():
            total_cost += int(score(a, b))
    
    return total_cost

def part2(data):
    """Solve part 2."""
    total_cost = 0

    for machine in data:
        button_a = machine["A"]
        button_b = machine["B"]
        t = (machine["T"][0] + 10000000000000, machine["T"][1] + 10000000000000)
        a, b = calculate_presses(button_a, button_b, t)
        if a.is_integer() and b.is_integer():
            total_cost += int(score(a, b))
    
    return total_cost

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