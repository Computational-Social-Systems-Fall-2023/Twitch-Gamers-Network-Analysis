# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import networkx as nx
import random
import pandas as pd

# Read the edges CSV file
edges_df = pd.read_csv('large_twitch_edges.csv')

# Create a graph from the edges
g = nx.from_pandas_edgelist(edges_df, source='numeric_id_1', target='numeric_id_2')
# g = nx.read_edgelist(Data, create_using=nx.DiGraph(), delimiter=',', nodetype=None, data=True, edgetype=None,
#                      encoding='utf-8')

# Identify connected components in the graph
connected_components = list(nx.connected_components(g))

# Find the largest connected component
largest_component = max(connected_components, key=len)

# Create a subgraph from the largest connected component
largest_subgraph = g.subgraph(largest_component)


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


# Parameters
n = largest_subgraph.order()  # Number of nodes
k = largest_subgraph.size()  # Each node is connected to k nearest neighbors
p = 0.2  # Probability of rewiring each edge

# Calculating Original Network size, degree, average path length, and clustering
print("Nodes: ", n)
print("Edges (Size): ", k)
print("Average degree: ", float(k) / n)
print("Average clustering: ", nx.average_clustering(largest_subgraph))
print("Average path length: ", nx.average_shortest_path_length(largest_subgraph))

# Create a Watts-Strogatz model network
watts_strogatz_graph = create_watts_strogatz_graph(n, k, p)

# Calculating average path length, and clustering of the watts_strogatz graph
print("Watts Strogatz Graph")
print("Average clustering: ", nx.average_clustering(watts_strogatz_graph))
print("Average path length: ", nx.average_shortest_path_length(watts_strogatz_graph))


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
