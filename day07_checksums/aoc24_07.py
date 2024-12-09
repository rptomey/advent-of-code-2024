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
    equations = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                equation_list = re.split(r":", line.strip())
                numbers = re.split(r"\s+", equation_list[1].strip())
                equation = {
                    "target": int(equation_list[0]),
                    "numbers": [int(number) for number in numbers]
                }
                equations.append(equation)
    
    return equations

def can_reach_target(equation, part2=False):
    target = equation["target"]
    numbers = equation["numbers"]

    def helper(current_result, remaining_numbers, part2):
        # Base case: no numbers left
        if not remaining_numbers:
            return current_result == target
        
        # Recursive case: try both addition and multiplication
        next_number = remaining_numbers[0]
        rest_numbers = remaining_numbers[1:]

        # Try addition
        if helper(current_result + next_number, rest_numbers, part2):
            return True
        
        # Try multiplication
        if helper(current_result * next_number, rest_numbers, part2):
            return True
        
        if part2:
            # Try concatenation
            if helper(int(str(current_result) + str(next_number)), rest_numbers, part2):
                return True
        
        return False    # No valid path to target found
    
    # Start recursion with the first number
    if not numbers:
        return False    # No numbers to work with
    return helper(numbers[0], numbers[1:], part2)

def part1(data):
    """Solve part 1."""
    valid_equations = 0

    for equation in data:
        if can_reach_target(equation):
            valid_equations += equation["target"]
    
    return valid_equations

def part2(data):
    """Solve part 2."""
    valid_equations = 0

    for equation in data:
        if can_reach_target(equation, part2=True):
            valid_equations += equation["target"]
    
    return valid_equations

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