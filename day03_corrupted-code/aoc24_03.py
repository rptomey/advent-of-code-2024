import sys
import re
import copy

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
                data.append(line.strip())

    return data

def part1(data):
    """Solve part 1."""
    total = 0

    for line in data:
        muls = re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)
        for mul in muls:
            a, b = [int(x) for x in re.findall(r"\d{1,3}", mul)]
            total += (a * b)

    return total

def part2(data):
    """Solve part 2."""
    total = 0
    enabled = True

    for line in data:
        # instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line)
        instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do(?:n't)?\(\)", line)
        for instruction in instructions:
            if instruction == "do()":
                enabled = True
            elif instruction == "don't()":
                enabled = False
            else:
                if enabled:
                    a, b = [int(x) for x in re.findall(r"\d{1,3}", instruction)]
                    total += (a * b)
    return total

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