import networkx as nx
import matplotlib.pyplot as plt

FILEPATH = 'test.edgelist'


def main():

    #G = generate_test_graph1()
    G = read_graph(FILEPATH)

    draw_graph(G)

    write_graph(G, FILEPATH)


# Create a test knowledge graph
def generate_test_graph1():
    edge_dict = {}
    edge_dict['JavaScript'] = ['Job1', 'Job2', 'Job3', 'Job4', 'Job5']
    edge_dict['CSS'] = ['Job1', 'Job3', 'Job5']
    edge_dict['Python'] = ['Job2', 'Job4']

    return create_graph(edge_dict)


# Create a Knowledge Graph, provided a dictionary of nodes and edges
#   - e_dict: a dictionary of skill-job (key-value) pairs
def create_graph(e_dict):
    return nx.from_dict_of_lists(e_dict, create_using=nx.DiGraph())


# Visualize a Knowledge Graph
#   - G: a networkx MultiDiGraph
def draw_graph(G):
    sources = []
    for e in G.edges():
        source, target = e
        sources.append(source)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G,
                     pos=nx.drawing.layout.bipartite_layout(G, nodes=sources),
                     width=2)
    plt.show()


# Read and return a Knowledge Graph from a file path
def read_graph(path):
    return nx.read_edgelist(path, create_using=nx.DiGraph, nodetype=str)


# Write a Knowledge Graph to a file path
def write_graph(G, path):
    nx.write_edgelist(G, path)


if __name__ == '__main__':
    main()