''' generate_IBMdevice_partition.py
    
    * Functions to take an IBM device and generate useful partitions of its coupling map
    * Assumes that coupling map is part of a Heavy-Hex Lattice
    * Uses networkx


    Usage:
    - import as a module
    - from terminal, e.g. 
      $ python generate_IBMdevice_partition.py ibm_washington
'''
import sys
import networkx as nx
import matplotlib.pyplot as plt


from qiskit import IBMQ
IBMQ.load_account()
provider = IBMQ.get_provider(hub='', group='', project='')




''' Backend Coupling Map to Networkx Graph
'''
def get_backend_graph(device="ibmq_brooklyn"):
    backend = provider.get_backend(device)
    config = backend.configuration()
    G = nx.Graph(config.coupling_map)
    assert nx.is_connected(G), "backend {} seems to have disconnected coupling map".format(device)
    return G
    

''' BIPARTITION of heavy-hex graph G into
    - deg2_nodes: Set of degree-2 nodes (degree assuming that graph is embedded into lattice)
    - deg3_nodes: Set of degree-3 nodes (degree assuming that graph is embedded into lattice)
    
    Sets corresponding node attribute "mydeg"
'''
def get_degree_nodes(G):
    ## check pre-conditions
    assert nx.algorithms.bipartite.is_bipartite(G), "graph is not bipartite"
    assert max([d for n,d in G.degree()]) == 3, "maxdegree of graph is not 3"
    ## compute sets
    deg2_nodes, deg3_nodes = nx.algorithms.bipartite.sets(G)
    if (any([G.degree[node] > 2 for node in deg2_nodes])):
        deg2_nodes, deg3_nodes = deg3_nodes, deg2_nodes
    ## post-conditions
    assert (all([G.degree[node] in [1,2] for node in deg2_nodes])), "deg2_nodes contains nodes of degree > 2"
    assert (any([G.degree[node] == 3 for node in deg3_nodes])), "deg3_nodes contains no node of degree 3"
    nx.set_node_attributes(G, dict.fromkeys(deg2_nodes,2), "mydeg") 
    nx.set_node_attributes(G, dict.fromkeys(deg3_nodes,3), "mydeg") 
    ## sets corresponding node attributes
    return [deg2_nodes, deg3_nodes]


''' Order Functions
    - order nodes inside edges / connected triples
    - "target node" first
'''
#   edge = (tdeg_node, neighbor)
def order_edge(edge, G, tdeg=2):
    # ensure degree categorization
    if (len(nx.get_node_attributes(G, "mydeg")) != G.number_of_nodes()):
        get_degree_nodes(G)
    # ensure node of mydeg tdeg is first
    if (G.nodes[edge[1]]["mydeg"] == tdeg):
        edge = (edge[1], edge[0])
    return edge

#   triple = (tdeg_node, smaller neighbor, larger neighbor)
def order_triple(triple, G, tdeg=2):
    # ensure degree categorization
    if (len(nx.get_node_attributes(G, "mydeg")) != G.number_of_nodes()):
        get_degree_nodes(G)
    # ensure node of mydeg tdeg is first
    target = [node for node in triple if G.nodes[node]["mydeg"] == tdeg][0]
    neighbors = [node for node in triple if G.nodes[node]["mydeg"] == 5-tdeg]
    small = min(neighbors)
    large = max(neighbors)
    return target, small, large



''' 3 edge partition gives valied 3 edge coloring of heavy-hex graph
    - Returns edge_coloring = [col1_list, col2_list, col3_list] of lists of ordered edges

    Sets corresponding edge attribute "color"
'''
def get_3_edge_partition(G):
    # Color Edges by a BFS-Greedy 3-Coloring of the Line Graph of G
    L = nx.line_graph(G)
    colors = nx.coloring.greedy_color(L, strategy="connected_sequential_bfs")
    edge_partition = [[], [], []]
    # key is node in L.nodes() = edge in G.edges(), val is color
    for key, val in colors.items():  
        edge = order_edge(key, G)
        edge_partition[val].append(edge)
        G.edges[edge]["color"] = val
    return edge_partition
  

''' Triple partition function
    - Returns [deg2_triples, deg3_triples] of lists of ordered triples, with central nodes of logical degree 2 / 3
'''
def get_triple_partition(G):
    # ensure degree categorization
    if (len(nx.get_node_attributes(G, "mydeg")) != G.number_of_nodes()):
        get_degree_nodes(G)
    # find all triples with 
    triple_partition = [[], []]
    for node in G.nodes():
        mydeg = G.nodes[node]["mydeg"]
        neighbors = [n for n in G.neighbors(node)]
        if (len(neighbors) == 2):
            triple = (node, *neighbors)
            triple_partition[mydeg-2].append(order_triple(triple, G, mydeg))
        if (len(neighbors) == 3):
            for n in neighbors:
                subset = [v for v in neighbors if v != n]
                triple = (node, *subset)
                triple_partition[mydeg-2].append(order_triple(triple, G, mydeg))
    return triple_partition


''' Plot partition of nodes and of edges
    Computed positions assume that nodes are labeled 
    - consecutively in rows 
    - from top left to bottom right
'''
def plot_partition(G):
    # ensure degree categorization
    if (len(nx.get_node_attributes(G, "mydeg")) != G.number_of_nodes()):
        get_degree_nodes(G)
    # ensure degree categorization
    if (len(nx.get_edge_attributes(G, "colors")) != G.number_of_edges()):
        get_3_edge_partition(G)

    # positions
    pos = [(0,0)]*G.number_of_nodes()    
    edges = nx.bfs_edges(G, 0)
    for u,v in edges:
        if (v == u+1):
            pos[v] = (pos[u][0]+1,pos[u][1])
        elif (v == u-1):
            pos[v] = (pos[u][0]-1,pos[u][1])
        elif (v > u):
            pos[v] = (pos[u][0],pos[u][1]-1)
        else:
            pos[v] = (pos[u][0],pos[u][1]+1)

    # visual coloring
    cmap = ["lightgray", "gray", "blue", "green", "red"]
    node_colors = []
    edge_colors = []
    mydegs = nx.get_node_attributes(G, "mydeg")
    mycols = nx.get_edge_attributes(G, "color")
    for key, val in mydegs.items():
        node_colors.append(cmap[val-2])
    for key, val in mycols.items():
        edge_colors.append(cmap[val+2])
    
    nx.draw(G, pos, node_color=node_colors, edge_color=edge_colors, width=5.0, with_labels=True)
    plt.show()



''' Generate Partition of device connectivity:
    - Coupling graph:   G
    - Node partition:   node_partition = [deg2_nodes, deg3_nodes]
    - Edge partition:   edge_partition = [col1_list, col2_list, col3_list]
    - Triple partit.:   triple_partition = [deg2_triples, deg3_triples]  

    with G having properties corresponding to the partitions in 
    - G.nodes[node]["mydeg"]
    - G.edges[edge]["color"]
'''
def generate_partition(device="ibmq_brooklyn"):
    G = get_backend_graph(device)
    node_partition = get_degree_nodes(G)
    edge_partition = get_3_edge_partition(G)
    triple_partition = get_triple_partition(G)

    return G, node_partition, edge_partition, triple_partition



''' When executed from Terminal
    - Generate device partition
    - Plot partition
'''
def main():
    device = "ibmq_brooklyn"
    if (len(sys.argv) > 1):
        device = sys.argv[1]
    
    G, node_partition, edge_partition, triple_partition = generate_partition(device)

    print("Nodes of logical degree 2:", node_partition[0])
    print("Nodes of logical degree 3:", node_partition[1])
    print("'Blue' edges:", edge_partition[0])
    print("'Green' edges:", edge_partition[1])
    print("'Red' edges:", edge_partition[2])
    print("Triples with central deg-2 node:",triple_partition[0])
    print("Triples with central deg-3 node:",triple_partition[1])

    plot_partition(G)

if __name__ == "__main__":
    main()
