from itertools import cycle
import dwave_networkx as dnx
from dwave_networkx.drawing.pegasus_layout import draw_pegasus
import matplotlib.pyplot as plt
import networkx as nx
import ast
from dwave_networkx.drawing.pegasus_layout import pegasus_layout

def compute_consistent_vertical_qubit_connectors(qubit_to_coord, minimum_paths,  n_source, n_target):
		for path in minimum_paths:
			vert_qubit_pegasus = list(set(path) - set([n_source, n_target]))[0]
			pegasus_coordinate = qubit_to_coord[vert_qubit_pegasus]
			if pegasus_coordinate[3] == 1:
				if pegasus_coordinate[4] == 1:
					return path
def extract_pegasus_coords(data):
	out = {}
	qubit_to_coord = {}
	for element in data:
		coord = element[0]
		qubit = element[1]["linear_index"]
		out[coord] = qubit
		qubit_to_coord[qubit] = coord
	return out, qubit_to_coord
def draw_pegasus_embedding(edges_subgraph, pegasus_qubits, pegasus_vertical_qubits, vertical_qubit_edges_subg):
	G = dnx.pegasus_graph(16)
	node_colors = []
	node_alpha = []
	node_sizes = []
	for a in list(G.nodes()):
		if a in pegasus_qubits:
			node_colors.append("red")
			node_alpha.append(1)
			node_sizes.append(28)
		elif a in pegasus_vertical_qubits:
			node_colors.append("cyan")
			node_alpha.append(1)
			node_sizes.append(28)
		else:
			node_colors.append("grey")
			node_alpha.append(0.1)
			node_sizes.append(12)
	edge_colors = []
	edge_alpha = []
	for e in list(G.edges()):
		if edges_subgraph.has_edge(*e) == True:
			edge_colors.append("red")
			edge_alpha.append(1)
		elif vertical_qubit_edges_subg.has_edge(*e) == True:
			edge_colors.append("cyan")
			edge_alpha.append(1)
		else:
			edge_colors.append("grey")
			edge_alpha.append(0.1)
	G_other = dnx.pegasus_graph(16, nice_coordinates=True)
	_, coordinates = extract_pegasus_coords(list(G_other.nodes(data=True)))
	labeldict = {}
	for a in list(G.nodes()):
		try:
			labeldict[a] = str(coordinates[a])
		except Exception as e:
			#print(e)
			labeldict[a] = ""
	nx.draw_networkx_nodes(G, pos=pegasus_layout(G), alpha=node_alpha, node_color=node_colors, linewidths=0.0, node_size=node_sizes)
	nx.draw_networkx_edges(G, pos=pegasus_layout(G), alpha=edge_alpha, edge_color=edge_colors, width=0.8)
	fig = plt.gcf()
	fig.set_size_inches(40, 40)
	plt.savefig("figures/heavy_hex_embedding_ibm_washington.pdf", bbox_inches='tight', pad_inches=-3.5, dpi=300)
	plt.close()
def remove_edge_qubits(embedding):
	for qubit in list(embedding.keys()):
		if type(qubit) is str:
			if "pre-" in qubit:
				del embedding[qubit]
			if "post-" in qubit:
				del embedding[qubit]
	return embedding
def remove_unused_edges(heavy_hex_to_remove, subgraph, ibm_to_dwave_qubit_embedding):
	for e in heavy_hex_to_remove:
		e_dwave = (ibm_to_dwave_qubit_embedding[e[0]], ibm_to_dwave_qubit_embedding[e[1]])
		assert subgraph.has_edge(*e_dwave) == True
		subgraph.remove_edge(*e_dwave)
	for e in heavy_hex_to_remove:
		e_dwave = (ibm_to_dwave_qubit_embedding[e[0]], ibm_to_dwave_qubit_embedding[e[1]])
		assert subgraph.has_edge(*e_dwave) == False
	return subgraph

#Logical Pegasus graph to use
G = dnx.pegasus_graph(16)
pegasus = dnx.pegasus_graph(16, nice_coordinates=True)
pegasus_coordinates = pegasus.nodes(data=True)
coord_to_qubit, qubit_to_coord = extract_pegasus_coords(pegasus_coordinates)

qubits = []
all_edges = []
pegasus_vertical_qubits = []
vertical_qubit_edges = []

parallel_QA_cells = [[(1, 0, 3), (0, 0, 3), (2, 1, 2), (1, 1, 2), (0, 1, 2), (2, 2, 1), (1, 2, 1)], 
[(2, 3, 8), (1, 3, 8), (0, 3, 8), (2, 4, 7), (1, 4, 7), (0, 4, 7), (2, 5, 6)], 
[(0, 3, 3), (2, 4, 2), (1, 4, 2), (0, 4, 2), (2, 5, 1), (1, 5, 1), (0, 5, 1)], 
[(1, 6, 8), (0, 6, 8), (2, 7, 7), (1, 7, 7), (0, 7, 7), (2, 8, 6), (1, 8, 6)], 
[(1, 7, 3), (0, 7, 3), (2, 8, 2), (1, 8, 2), (0, 8, 2), (2, 9, 1), (1, 9, 1)], 
[(2, 10, 8), (1, 10, 8), (0, 10, 8), (2, 11, 7), (1, 11, 7), (0, 11, 7), (2, 12, 6)]]


#Because of the two missing CNOT gates on ibm_washington
heavy_hex_to_remove = [(109, 114), (8, 9)]

parallel_QA_embeddings = []

for initial_cells in parallel_QA_cells:
	heavy_hex_h_line_1 = [i for i in range(0, 13+1)]+["post-13"]#The post-13 strings are just to track the slightly non-repeating way the heavy-hex graph is defined. 
	heavy_hex_h_line_2 = [i for i in range(18, 32+1)]
	heavy_hex_h_line_3 = [i for i in range(37, 51+1)]
	heavy_hex_h_line_4 = [i for i in range(56, 70+1)]
	heavy_hex_h_line_5 = [i for i in range(75, 89+1)]
	heavy_hex_h_line_6 = [i for i in range(94, 108+1)]
	heavy_hex_h_line_7 = ["pre-113"]+[i for i in range(113, 126+1)]
	all_heavy_hex_lines = [heavy_hex_h_line_1, heavy_hex_h_line_2, heavy_hex_h_line_3, heavy_hex_h_line_4, heavy_hex_h_line_5, heavy_hex_h_line_6, heavy_hex_h_line_7]

	vertical_qubit_mapping_1_2 = {14: [0, 18], 15: [4, 22], 16: [8, 26], 17: [12, 30]}
	vertical_qubit_mapping_2_3 = {33: [20, 39], 34: [24, 43], 35: [28, 47], 36: [32, 51]}
	vertical_qubit_mapping_3_4 = {52: [37, 56], 53: [41, 60], 54: [45, 64], 55: [49, 68]}
	vertical_qubit_mapping_4_5 = {71: [58, 77], 72: [62, 81], 73: [66, 85], 74: [70, 89]}
	vertical_qubit_mapping_5_6 = {90: [75, 94], 91: [79, 98], 92: [83, 102], 93: [87, 106]}
	vertical_qubit_mapping_6_7 = {109: [96, 114], 110: [100, 118], 111: [104, 122], 112: [108, 126]}

	vertical_qubit_mappings = {**vertical_qubit_mapping_1_2, **vertical_qubit_mapping_2_3, **vertical_qubit_mapping_3_4, **vertical_qubit_mapping_4_5, 
	**vertical_qubit_mapping_5_6, **vertical_qubit_mapping_6_7}

	file = open("horizontal_line_embeddings/embeddings.txt", "r")
	data = ast.literal_eval(file.read())
	file.close()

	combined_horizontal_pegasus_cells = data[0]
	combined_horizontal_qubit_pegasus_coordinates = data[1]
	combined_horizontal_qubit_numbers = data[2]

	horizontal_lines = []

	ibm_to_dwave_qubit_embedding = {}
	cell_line_index = -1
	for cell in initial_cells:
		cell_line_index += 1
		line_index = -1
		for line in combined_horizontal_pegasus_cells:
			line_index += 1
			if cell in line:
				temp_line = line
				idx = line.index(cell)
				del temp_line[0:idx]
				temp_pegasus_coordinates = combined_horizontal_qubit_pegasus_coordinates[line_index]
				del temp_pegasus_coordinates[0:idx*2]
				horiz_line = len(heavy_hex_h_line_1)
				pegasus_coordinates = temp_pegasus_coordinates[0:horiz_line]
				print(pegasus_coordinates)
				pegasus_qubits1 = [coord_to_qubit[a] for a in pegasus_coordinates]
				edges_subgraph1 = list(G.subgraph(pegasus_qubits1).edges())
				qubits += pegasus_qubits1
				all_edges += edges_subgraph1
				COUNT = -1
				for qu in all_heavy_hex_lines[cell_line_index]:
					COUNT += 1
					ibm_to_dwave_qubit_embedding[qu] = pegasus_qubits1[COUNT]
	
	for vertical_qubit in vertical_qubit_mappings:
		horizontal_qubits = vertical_qubit_mappings[vertical_qubit]
	
		n_source = ibm_to_dwave_qubit_embedding[horizontal_qubits[0]]
		n_target = ibm_to_dwave_qubit_embedding[horizontal_qubits[1]]
		min_paths = [p for p in nx.all_shortest_paths(G,source=n_source,target=n_target)]
	
		path = compute_consistent_vertical_qubit_connectors(qubit_to_coord, min_paths, n_source, n_target)
		vert_qubit_pegasus = list(set(path) - set([n_source, n_target]))
		ibm_to_dwave_qubit_embedding[vertical_qubit] = vert_qubit_pegasus[0]
		pegasus_vertical_qubits.append(vert_qubit_pegasus[0])
		H = G.subgraph(path)
		H = H.edges()
		vertical_qubit_edges += H
	ibm_to_dwave_qubit_embedding = remove_edge_qubits(ibm_to_dwave_qubit_embedding)
	parallel_QA_embeddings.append(ibm_to_dwave_qubit_embedding)

file = open("parallel_embeddings/easy.txt", "w")
file.write(str(parallel_QA_embeddings))
file.close()

draw_pegasus_embedding(nx.Graph(all_edges), qubits, pegasus_vertical_qubits, nx.Graph(vertical_qubit_edges))

