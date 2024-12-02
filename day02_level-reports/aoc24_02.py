import sys
import re
import copy

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)` to prevent
# changing the original input in your part 1 solution before doing part 2.

def parse(file_name):
    """Parse input"""
    reports = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                levels = re.split(r"\s+", line.strip())
                report = [int(x) for x in levels]
                reports.append(report)
    
    return reports

def safe_test(report, dampen=False):
    deltas = [report[i+1] - report[i] for i in range(len(report) - 1)]
    if 1 <= min(deltas) <= max(deltas) <= 3:
        return True
    elif -3 <= min(deltas) <= max(deltas) <= -1:
        return True
    else:
        if dampen:
            return dampened_safe_test(report)
        else:
            return False

def dampened_safe_test(report):
    for i in range(len(report)):
        modified_report = copy.copy(report)
        del modified_report[i]
        if safe_test(modified_report):
            return True
        
    return False

def part1(data):
    """Solve part 1."""
    total_safe = 0
    for report in data:
        if safe_test(report):
            total_safe += 1
    return total_safe

def part2(data):
    """Solve part 2."""
    total_safe = 0
    for report in data:
        if safe_test(report, dampen=True):
            total_safe += 1
    return total_safe

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