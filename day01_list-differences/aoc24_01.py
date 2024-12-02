import sys
import re
import copy

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
    total_distance = 0

    # Leave the original lists as-is
    left = copy.copy(data["left"])
    right = copy.copy(data["right"])

    # Sorting doesn't return, so it has to be done as a separate step.
    left.sort()
    right.sort()

    for i in range(len(left)):
        total_distance += abs(right[i] - left[i])

    return total_distance

def part2(data):
    """Solve part 2."""
    total_similarity = 0

    left = data["left"]
    right = data["right"]

    # Using sum() + generator expression
    # This method uses the trick of adding 1 to the sum whenever the generator expression returns true.
    # By the time list gets exhausted, summation of count of numbers matching a condition is returned. 
    for l in left:
        total_similarity += l * sum(1 for r in right if r == l)

    return total_similarity

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