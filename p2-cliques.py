import matplotlib.pyplot as plt
import networkx as nx
import re

# GOAL: find the groups of entangled qubits and possibly separate them
entanglements = []
with open("P2_swift_rise.qasm", "r") as f:
    entanglements = [tuple(map(int, re.findall(r'\d+', l) + [i])) for i, l in enumerate(f.readlines()) if "cz" in l]

# build a digraph representing entanglements
G = nx.DiGraph()
for tup in entanglements:
    G.add_edge(*tup[0:2], line_num = tup[2])

# print the adjacency matrix
print(nx.adjacency_matrix(G).toarray())

# draw the graph with node labels as numbers
nx.draw(G, labels = dict(zip(G.nodes, G.nodes)), font_color = "whitesmoke")
plt.show()