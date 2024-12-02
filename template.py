import sys
import re
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)` to prevent
# changing the original input in your part 1 solution before doing part 2.

def parse(file_name):
    """Parse input"""
    lists = {
        "left": [],
        "right": []
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                nums = re.split(r"\s+", line)
                lists["left"].append(int(nums[0]))
                lists["right"].append(int(nums[1]))
    
    return lists

def part1(data):
    """Solve part 1."""
    pass

def part2(data):
    """Solve part 2."""
    pass

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