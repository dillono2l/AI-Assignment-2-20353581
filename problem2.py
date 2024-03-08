import networkx as nx
import random
import matplotlib.pyplot as plt

def generate_random_graph(num_nodes, probability):
   
    G = nx.erdos_renyi_graph(num_nodes, probability)
    return G

def assign_random_colors(graph, color_cap):
   
    colors = {}
    for node in graph.nodes():
        colors[node] = random.randint(1, color_cap)  
    return colors


def count_conflicts(graph, colors):
    
    conflicts = 0
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            if colors[node] == colors[neighbor]:
                conflicts += 1
    return conflicts // 2  # Each conflict is counted twice (once for each node)

def decentralized_graph_coloring(graph, colors):
  
    num_iterations = 10  # Number of iterations
    conflicts_over_time = []
    for _ in range(num_iterations):
        conflicts = count_conflicts(graph, colors)
        conflicts_over_time.append(conflicts)

        for node in graph.nodes():
            neighbor_colors = [colors[neighbor] for neighbor in graph.neighbors(node)]
            available_colors = [color for color in range(1, len(graph.nodes()) + 1) if color not in neighbor_colors]

            if colors[node] in neighbor_colors:  # If the node has a conflict
                print(f"Conflict at node {node}, with neighbors {list(graph.neighbors(node))}.")
                colors[node] = random.choice(available_colors)  # Change its color to a random available color
                conflicts_over_time.append(count_conflicts(graph, colors))

    num_colors = len(set(colors.values()))  # Count the number of unique colors used
    print("Number of colors used:", num_colors)

    return colors, conflicts_over_time

def plot_conflicts_over_time(conflicts_over_time):

    plt.plot(range(len(conflicts_over_time)), conflicts_over_time, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Number of Conflicts')
    plt.title('Number of Conflicts Over Time')
    plt.grid(True)
    plt.show()

def plot_graph_with_colors(graph, colors=None, pos=None):
    
    if colors is None:
        node_colors = [random.randint(1, len(graph.nodes())) for _ in graph.nodes()]
    else:
        node_colors = [colors[node] for node in graph.nodes()]
    if pos is None:
        pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)
    plt.show()  


def main():
    num_nodes = 20
    edge_probability = 1
    color_cap = 5

    # Generate a random graph
    random_graph = generate_random_graph(num_nodes, edge_probability)

    # Compute layout for the graph
    pos = nx.spring_layout(random_graph)
   
    # Assign random colors to nodes
    initial_colors = assign_random_colors(random_graph, color_cap)

    plt.figure()
    plt.title('Initial Graph')
    plot_graph_with_colors(random_graph, initial_colors, pos= pos)

    # Perform decentralized graph coloring
    final_colors, conflicts_over_time = decentralized_graph_coloring(random_graph, initial_colors)
    

    print("Final colors assigned to nodes:")
    print(final_colors)

    # Plot the number of conflicts over time
    plot_conflicts_over_time(conflicts_over_time)

    # Plot the final graph with colors
    plt.figure()
    plt.title('Final Graph')
    plot_graph_with_colors(random_graph, final_colors, pos=pos)

if __name__ == "__main__":
    main()
