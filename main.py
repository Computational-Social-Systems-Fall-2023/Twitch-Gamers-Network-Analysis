#############################################################
# Twitch Gamers Network Analysis
# Author: Nhat Tran
#
#############################################################
import networkx as nx
import random
import pandas as pd

# Read the edges CSV file
edges_df = pd.read_csv('large_twitch_edges.csv')

# Create a graph from the edges
g = nx.from_pandas_edgelist(edges_df, source='numeric_id_1', target='numeric_id_2')

# Identify connected components in the graph
connected_components = list(nx.connected_components(g))

# Find the largest connected component
largest_component = max(connected_components, key=len)

# Create a subgraph from the largest connected component
largest_subgraph = g.subgraph(largest_component)


# define Watts Strogatz graph
def create_watts_strogatz_graph(num_nodes, mean_degree, probability):
    graph = nx.Graph()

    # A ring lattice with num_nodes and degree
    for node in range(num_nodes):
        for neighbor in range(1, mean_degree // 2 + 1):
            graph.add_edge(node, (node + neighbor) % num_nodes)

    # Rewire edges with probability p
    for node in range(num_nodes):
        for neighbor in graph.neighbors(node):
            if random.random() < probability:
                new_neighbor = random.choice(list(graph.nodes()))
                while new_neighbor == node or graph.has_edge(node, new_neighbor):
                    new_neighbor = random.choice(list(graph.nodes()))
                graph.remove_edge(node, neighbor)
                graph.add_edge(node, new_neighbor)

    return graph


# Number of nodes
n = largest_subgraph.order()

# Each node is connected to k nearest neighbors
k = largest_subgraph.size()

# Probability of rewiring each edge
p = 0.2

# Calculating Original Network size, degree, average path length, and clustering
print("Nodes: ", n)
print("Edges (Size): ", k)
print("Average degree: ", float(k * 2) / n)
print("Average clustering: ", nx.average_clustering(largest_subgraph))
print("Average path length: ", nx.average_shortest_path_length(largest_subgraph))

# Create a Watts-Strogatz model network
watts_strogatz_graph = create_watts_strogatz_graph(n, k, p)

# Calculating average path length, and clustering of the watts_strogatz graph
print("Watts Strogatz Graph")
print("Average clustering: ", nx.average_clustering(watts_strogatz_graph))
print("Average path length: ", nx.average_shortest_path_length(watts_strogatz_graph))


# define Barabasi-Albert method
def create_barabasi_albert_graph(initial_number_of_nodes, number_of_expected_connections, time_to_run):
    # check if m <= m0
    if initial_number_of_nodes < number_of_expected_connections:
        return 0

    # Initial graph with m0 nodes and degrees of at least 1
    graph = nx.complete_graph(initial_number_of_nodes)

    if graph.degree() < 1:
        return 0

    for time in range(time_to_run):
        # Add new node
        new_node = graph.number_of_nodes()
        graph.add_node(new_node)

        # Connect the new node to a random node of the existing nodes
        while graph.degree(new_node) < number_of_expected_connections:
            # calculate probability
            sum_degree = sum(graph.degree(v) for v in graph)
            probability = [graph.degree(v) / sum_degree for v in graph.nodes()]
            # select a random node
            list_of_nodes = list(graph.nodes())
            random_node = random.choices(list_of_nodes, weights=probability, k=1)[0]
            # connect vj to a random node
            graph.add_edge(new_node, random_node)
    return graph


# Initial number of nodes
m0 = largest_subgraph.order()

# Number of expected connections
m = largest_subgraph.size()

# Time to run
t = 1000

# Generate a scale-free network using Preferential Attachment
barabasi_albert_graph = create_barabasi_albert_graph(m0, m, t)

# Calculating average path length, and clustering of the watts_strogatz graph
print("Barabasi Albert Graph")
print("Average clustering: ", nx.average_clustering(barabasi_albert_graph))
print("Average path length: ", nx.average_shortest_path_length(barabasi_albert_graph))


# ===============================================================================================================
# Visualize the network
# pos = nx.circular_layout(watts_strogatz_graph)  # Circular layout for visualization
# nx.draw(watts_strogatz_graph, pos, with_labels=True, node_size=300, node_color='skyblue')
# plt.title("Watts-Strogatz Model")
# plt.show()


# plt.savefig('graph.png')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
