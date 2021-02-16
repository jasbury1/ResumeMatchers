import networkx as nx
import matplotlib.pyplot as plt


# Create a Knowledge Graph
#   - e_dict: a dictionary of skill-job (key-value) pairs
def create_graph(e_dict):
    return nx.from_dict_of_lists(e_dict, create_using=nx.MultiDiGraph())


# Visualize a Knowledge Graph
#   - G: a networkx MultiDiGraph
#   - keys: list of skills, signifies skills to be on left side of bipartite graph
def draw_graph(G, keys):
    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G,
                     pos=nx.drawing.layout.bipartite_layout(G, nodes=keys),
                     width=2)
    plt.show()


edge_dict = {}
edge_dict['JavaScript'] = ['Job1', 'Job2', 'Job3', 'Job4', 'Job5']
edge_dict['CSS'] = ['Job1', 'Job3', 'Job5']
edge_dict['Python'] = ['Job2', 'Job4']

G = create_graph(edge_dict)
draw_graph(G, edge_dict.keys())