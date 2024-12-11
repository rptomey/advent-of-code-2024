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
    data = {}

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                stones = [int(x) for x in re.findall(r"\d+", line)]
                for stone in stones:
                    if stone in data:
                        data[stone] += 1
                    else:
                        data[stone] = 1

    return data

memory = {}

def apply_rule(stone):
    if stone in memory:
        return memory[stone]
    else:
        match stone:
            case 0:
                val = 1
            case stone if len(str(stone)) % 2 == 0:
                stone_string = str(stone)
                middle = len(stone_string) // 2
                val = tuple([int(x) for x in (stone_string[:middle], stone_string[middle:])])
            case _:
                val = stone * 2024
        memory[stone] = val
        return val

def log_adjustments(stone, quantity, adj_type, adjustments):
    if stone in adjustments:
        if adj_type in adjustments[stone]:
            adjustments[stone][adj_type] += quantity
        else:
            adjustments[stone][adj_type] = quantity
    else:
        adjustments[stone] = {}
        adjustments[stone][adj_type] = quantity

def apply_adjustments(library, adjustments):
    for stone in adjustments:
        if stone in library:
            if "plus" in adjustments[stone]:
                library[stone] += adjustments[stone]["plus"]
            if "minus" in adjustments[stone]:
                library[stone] -= adjustments[stone]["minus"]
                if library[stone] == 0:
                    del library[stone]
        else:
            library[stone] = 0
            if "plus" in adjustments[stone]:
                library[stone] += adjustments[stone]["plus"]
            if "minus" in adjustments[stone]:
                library[stone] -= adjustments[stone]["minus"]
                if library[stone] == 0:
                    del library[stone]

def blink(library):
    adjustments = {}
    for stone in library:
        quantity = library[stone]
        new_stones = apply_rule(stone)
        if type(new_stones) == int:
            log_adjustments(new_stones, quantity, "plus", adjustments)
        elif type(new_stones) == tuple:
            for new_stone in new_stones:
                log_adjustments(new_stone, quantity, "plus", adjustments)
        log_adjustments(stone, quantity, "minus", adjustments)
    apply_adjustments(library, adjustments)

def part1(data):
    """Solve part 1."""
    stone_library = data
    for i in range(25):
        blink(stone_library)
    
    total = 0
    
    for stone in stone_library:
        total += stone_library[stone]
    
    return total

def part2(data):
    """Solve part 2."""
    stone_library = data

    # Part 1 already did it 25 times, so just do 50 more times
    for i in range(50):
        blink(stone_library)

    total = 0
    
    for stone in stone_library:
        total += stone_library[stone]
    
    return total

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