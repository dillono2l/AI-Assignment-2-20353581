import networkx as nx
import random
import matplotlib.pyplot as plt

def generate_random_graph(num_nodes, probability):
 
    G = nx.erdos_renyi_graph(num_nodes, probability)
    return G

def assign_random_colors(graph, color_cap):

    colors = {}
    num_colors = 0
    for node in graph.nodes():
        color = random.randint(1, color_cap)
        colors[node] = color
        if color > num_colors:
            num_colors = color
    return colors, num_colors

def greedy_coloring(graph, colors, num_colors, distinct_colors_over_time):

    while True:
        improved = False
        for node in graph.nodes():
            neighbor_colors = set(colors[neighbor] for neighbor in graph.neighbors(node))
            for color in range(1, num_colors + 1):
                if color not in neighbor_colors:
                    colors[node] = color
                    distinct_colors_over_time.append(len(set(colors.values())))  
                    break
            else:
                new_color = random.randint(1, num_colors)
                colors[node] = new_color
                improved = True
        if not improved:
            break
    return colors

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
    num_nodes = 50
    edge_probability = 0.3
    color_cap = 20

    # Generate a random graph
    random_graph = generate_random_graph(num_nodes, edge_probability)

    # Compute layout for the graph
    pos = nx.spring_layout(random_graph)

    # Randomly assign colors to all nodes
    colors, num_colors = assign_random_colors(random_graph, color_cap)

    # Plot the initial graph before coloring
    plt.figure()
    plt.title('Initial Graph')
    initial_graph = random_graph
    plot_graph_with_colors(initial_graph, pos=pos)

    # Print the number of colors used in the initial coloring
    print("Initial Chromatic Number", num_colors)

    # Store the number of distinct colors used over time
    distinct_colors_over_time = [num_colors]  

    # Improve coloring using greedy algorithm
    while True:
        colors = greedy_coloring(random_graph, colors, num_colors, distinct_colors_over_time)
        distinct_colors = len(set(colors.values()))
        if distinct_colors == num_colors:
            break
        num_colors = distinct_colors

    # Plot the number of distinct colors used over time
    plt.plot(range(len(distinct_colors_over_time)), distinct_colors_over_time)
    plt.xlabel('Steps')
    plt.ylabel('Chromatic Number')
    plt.title('Chromatic Number Over Time')
    plt.show()

    # Plot the final graph with colors using the same layout
    plt.figure()
    plt.title('Final Graph')
    plot_graph_with_colors(random_graph, colors, pos=pos)

    # Print the number of colors used after the final coloring
    print("Final Chromatic number :", num_colors)


if __name__ == "__main__":
    main()
