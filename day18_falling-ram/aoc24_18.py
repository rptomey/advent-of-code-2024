import sys
import time
import re
import networkx as nx
import copy
import matplotlib.pyplot as plt

# To run, go to the folder in the terminal, and enter:
# python <code-filename.py> <input-filename.txt>

# Don't forget to use `copy.copy(thing)` or `copy.deepcopy(thing)`
# to make changes to a thing without impacting the original version.

def create_square_grid_graph(N):
    """
    Creates a square grid graph of size N x N where each node is connected
    to its up, down, left, and right neighbors.

    Args:
        N (int): The size of the grid (N x N).

    Returns:
        nx.Graph: A NetworkX graph representing the grid.
    """
    G = nx.Graph()
    
    # Add nodes and edges
    for x in range(N + 1):
        for y in range(N + 1):
            G.add_node((x, y))  # Add the node (x, y)
            
            # Add an edge to the right neighbor if within bounds
            if x + 1 <= N:
                G.add_edge((x, y), (x + 1, y))
            
            # Add an edge to the upper neighbor if within bounds
            if y + 1 <= N:
                G.add_edge((x, y), (x, y + 1))
    
    return G

def parse(file_name):
    """Parse input"""
    data = {
        "positions": []
    }

    if file_name == "input.txt":
        graph = create_square_grid_graph(70)
    else:
        graph = create_square_grid_graph(6)

    data["graph"] = graph

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                position = tuple([int(x) for x in re.findall(r"\d+", line)])
                data["positions"].append(position)
    
    return data

def visualize_graph_on_grid_inverted(G):
    """
    Visualizes the graph with nodes aligned to a grid based on (x, y) coordinates,
    with the y-axis inverted so that (0, 0) is at the top-left corner.

    Args:
        G (nx.Graph): The graph to visualize.
    """
    # Use node coordinates as positions
    pos = {node: node for node in G.nodes()}
    
    # Create the plot
    plt.figure(figsize=(8, 8))
    
    # Draw the graph with grid-aligned positions
    nx.draw(
        G, pos, with_labels=False, node_color="lightblue", edge_color="gray", node_size=500
    )
    
    # Draw the labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    
    # Set grid and invert y-axis
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.gca().invert_yaxis()  # Invert the y-axis
    
    # Adjust axis ticks to align with grid
    plt.xticks(range(min(x for x, y in G.nodes()), max(x for x, y in G.nodes()) + 1))
    plt.yticks(range(min(y for x, y in G.nodes()), max(y for x, y in G.nodes()) + 1))
    plt.gca().set_aspect("equal", adjustable="box")
    
    # Add title and display
    plt.title("Graph Aligned to Grid (Inverted Y-Axis)")
    plt.show()

def part1(data):
    """Solve part 1."""
    graph = copy.deepcopy(data["graph"])
    
    positions = data["positions"]

    for position in positions[:1024]:
        if position in graph:
            graph.remove_node(position)

    # visualize_graph_on_grid_inverted(graph)
    
    distance = nx.shortest_path_length(graph, source=(0,0), target=(70,70))

    return distance

def part2(data):
    """Solve part 2."""
    graph = copy.deepcopy(data["graph"])
    
    positions = data["positions"]

    last_position = None

    for position in positions:
        if position in graph:
            graph.remove_node(position)
            if not nx.has_path(graph, source=(0,0), target=(70,70)):
                last_position = position
                break
    
    return last_position

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