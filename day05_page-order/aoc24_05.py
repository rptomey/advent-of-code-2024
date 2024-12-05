import sys
import re
import copy
import math

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def parse(file_name):
    """Parse input"""
    data = {
        "rules": {},
        "updates": []
    }

    # First just get the stuff out of the file
    with open(file_name) as f:
        parsing = "rules"
        for line in f:
            if line != "\n":
                if parsing == "rules":
                    a, b = re.findall(r"\d+", line.strip())
                    if a not in data["rules"]:
                        data["rules"][a] = {"numbers": {b}}
                    else:
                        data["rules"][a]["numbers"].add(b)
                else:
                    data["updates"].append(line.strip().split(","))
            else:
                parsing = "updates"
    
    return data

def part1(data):
    """Solve part 1."""
    total = 0
    rules = data["rules"]
    updates = data["updates"]

    # Prep for part2
    data["failures"] = set()

    for rule in rules.keys():
        rules[rule]["regex"] = re.compile(f"(?:{'|'.join(rules[rule]["numbers"])}).*{rule}")

    for update in updates:
        relevant_rules = set(rules.keys()).intersection(update)
        update_string = ",".join(update)
        checking = True
        safe = True
        while checking:
            for rule in relevant_rules:
            # for rule in rules.keys():
                if re.search(rules[rule]["regex"], update_string):
                    data["failures"].add(update_string)
                    safe = False
                    checking = False
            checking = False
        if safe:
            middle_index = math.floor(len(update)/2)
            middle = int(update[middle_index])
            total += middle
    
    return total

def part2(data):
    """Solve part 2."""
    total = 0
    rules = data["rules"]
    failures = data["failures"]

    for update_string in failures:
        update = update_string.split(",")
        relevant_rules = set(rules.keys()).intersection(update)
        rules_to_satisfy = list(relevant_rules)
        while len(rules_to_satisfy) > 0:
            rule_id = rules_to_satisfy.pop(0)
            relevant_numbers = set(rules[rule_id]["numbers"]).intersection(update)
            if len(relevant_numbers) > 0:
                id_index = update.index(rule_id)
                first_relevant_index = min([update.index(num) for num in relevant_numbers])
                if id_index > first_relevant_index:
                    num = update.pop(id_index)
                    update.insert(first_relevant_index, num)
                    rules_to_satisfy.append(rule_id)
        
        middle_index = math.floor(len(update)/2)
        middle = int(update[middle_index])
        total += middle
    
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