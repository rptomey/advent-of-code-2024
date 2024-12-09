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
    data = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                data = [int(num) for num in list(line.strip())]
    
    return data

def part1(data):
    """Solve part 1."""
    mem_array = []
    mode = "file"
    file_count = 0
    checksum = 0

    # Blow up the file notation to the full mem_array
    for el in data:
        if mode == "file":
            file_id = file_count
            for i in range(el):
                mem_array.append(file_id)
            file_count += 1
            mode = "blank"
        elif mode == "blank":
            for i in range(el):
                mem_array.append(".")
            mode = "file"

    # Sort the files as requested
    while "." in mem_array:
        print(f"1-mem size: {len(mem_array)}")
        free_space = mem_array.index(".")
        print(f"1-index: {free_space}")
        chunk = mem_array.pop()
        if chunk != ".":
            mem_array[free_space] = chunk

    # Calculate the checksum
    for i in range(len(mem_array)):
        checksum += (mem_array[i] * i)

    return checksum

def part2(data):
    """Solve part 2."""
    mem = {}
    mode = "file"
    file_count = 0
    memory_location = 0
    checksum = 0

    # Store as content of memory locations
    for index in range(len(data)):
        length = data[index]
        store = {
            "type": mode,
            "size": length
        }
        if mode == "file":
            store["id"] = file_count
            file_count += 1
            mode = "blank"
        elif mode == "blank":
            mode = "file"
        mem[memory_location] = store
        memory_location += length
    
    # Try to move each file once, starting with the last file
    file_keys = [x for x in mem if mem[x]["type"] == "file"]
    file_keys.sort(reverse=True)
    
    for key in file_keys:
        file = mem[key]
        file_size = file["size"]
        # Find all of the blanks where it could fit
        blank_keys = [x for x in mem if mem[x]["type"] == "blank" and mem[x]["size"] >= file_size and x < key]
        blank_keys.sort()
        if len(blank_keys) > 0:
            blank_key = blank_keys[0]
            remaining_space = mem[blank_key]["size"] - file_size
            # Relabel the rest of the blank space
            if remaining_space > 0:
                new_blank_index = blank_key + file_size
                mem[new_blank_index] = {
                    "type": "blank",
                    "size": remaining_space
                }
            # Move the file
            mem[blank_key] = file
            # Clear the old file
            mem[key] = {
                "type": "blank",
                "size": file_size
            }
            # Join blank space if either neighbor was blank
            all_blank_keys = [x for x in mem if mem[x]["type"] == "blank"]
            all_blank_keys.sort()
            blank_index = all_blank_keys.index(key)
            if blank_index < len(all_blank_keys) - 1:
                right_neighbor = all_blank_keys[blank_index+1]
                if right_neighbor == key + file_size:
                    mem[key]["size"] += mem[right_neighbor]["size"]
                    del mem[right_neighbor]
            if blank_index > 0:
                left_neighbor = all_blank_keys[blank_index-1]
                if key == left_neighbor + mem[left_neighbor]["size"]:
                    mem[left_neighbor]["size"] += mem[key]["size"]
                    del mem[key]

    # Reconstruct the memory
    mem_list = []
    mem_keys = [int(x) for x in mem.keys()]
    mem_keys.sort()
    for key in mem_keys:
        if mem[key]["type"] == "file":
            file_id = mem[key]["id"]
            size = mem[key]["size"]
            mem_list.extend([file_id] * size)
        else:
            size = mem[key]["size"]
            mem_list.extend(["."] * size)

    # Calculate the checksum
    for i in range(len(mem_list)):
        if mem_list[i] != ".":
            checksum += (mem_list[i] * i)

    return checksum

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