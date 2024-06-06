from itertools import cycle
import dwave_networkx as dnx
from dwave_networkx.drawing.pegasus_layout import draw_pegasus
import matplotlib.pyplot as plt
import networkx as nx
import ast
import dimod
from dwave_networkx.drawing.zephyr_layout import zephyr_layout
from dwave_networkx.drawing.pegasus_layout import pegasus_layout

def create_graph(lt, qt): 
    G = nx.Graph()
    for key, val in lt.items():
        G.add_node(key[0], weight=val)
    for key, val in qt.items():
        G.add_edge(key[0], key[1], weight=val)
    return G
def extract_pegasus_coords(data):
	out = {}
	qubit_to_coord = {}
	for element in data:
		coord = element[0]
		qubit = element[1]["linear_index"]
		out[coord] = qubit
		qubit_to_coord[qubit] = coord
	return out, qubit_to_coord
def draw_pegasus_embedding(edges_subgraph, pegasus_qubits, pegasus_vertical_qubits, vertical_qubit_edges_subg, cubic_qubits, cubic_graph):
	G = dnx.pegasus_graph(16)
	labeldict = {}
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
		elif a in cubic_qubits:
			node_colors.append("green")
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
		elif cubic_graph.has_edge(*e) == True:
			edge_colors.append("green")
			edge_alpha.append(1)
		else:
			edge_colors.append("grey")
			edge_alpha.append(0.1)
	nx.draw_networkx_nodes(G, pos=pegasus_layout(G), alpha=node_alpha, node_size=node_sizes, node_color=node_colors)
	nx.draw_networkx_edges(G, pos=pegasus_layout(G), alpha=edge_alpha, edge_color=edge_colors, width=0.8)
	fig = plt.gcf()
	fig.set_size_inches(40, 40)
	plt.savefig("figures/cubic_terms_heavy_hex_embedding_ibm_washington_parallel.pdf", bbox_inches='tight', pad_inches=-3.5, dpi=300)
	plt.close()
def pull_out_deg2_qubits(cubic_terms):
	out = {}
	for a in cubic_terms:
		out[a[0]] = a
	return out
def compute_consistent_vertical_qubit_connectors(qubit_to_coord, minimum_paths,  n_source, n_target):
	for path in minimum_paths:
		vert_qubit_pegasus = list(set(path) - set([n_source, n_target]))[0]
		pegasus_coordinate = qubit_to_coord[vert_qubit_pegasus]
		if pegasus_coordinate[3] == 1:
			if pegasus_coordinate[4] == 1:
				return path
def invert_ibm_to_dwave_qubit_embedding(ibm_to_dwave_qubit_embedding):
	out = {}
	for a in ibm_to_dwave_qubit_embedding:
		out[ibm_to_dwave_qubit_embedding[a]] = a
	return out
def remove_edge_qubits(embedding):
	for qubit in list(embedding.keys()):
		if type(qubit) is str:
			if "pre-" in qubit:
				del embedding[qubit]
			if "post-" in qubit:
				del embedding[qubit]
	return embedding

G = dnx.pegasus_graph(16)
pegasus = dnx.pegasus_graph(16, nice_coordinates=True)
pegasus_coordinates = pegasus.nodes(data=True)
coord_to_qubit, qubit_to_coord = extract_pegasus_coords(pegasus_coordinates)

#initial_cells = [(1, 0, 3), (0, 0, 3), (2, 1, 2), (1, 1, 2), (0, 1, 2), (2, 2, 1), (1, 2, 1)]

parallel_QA_cells = [[(1, 0, 3), (0, 0, 3), (2, 1, 2), (1, 1, 2), (0, 1, 2), (2, 2, 1), (1, 2, 1)],
[(2, 3, 8), (1, 3, 8), (0, 3, 8), (2, 4, 7), (1, 4, 7), (0, 4, 7), (2, 5, 6)],
[(0, 3, 3), (2, 4, 2), (1, 4, 2), (0, 4, 2), (2, 5, 1), (1, 5, 1), (0, 5, 1)],
[(1, 6, 8), (0, 6, 8), (2, 7, 7), (1, 7, 7), (0, 7, 7), (2, 8, 6), (1, 8, 6)],
[(1, 7, 3), (0, 7, 3), (2, 8, 2), (1, 8, 2), (0, 8, 2), (2, 9, 1), (1, 9, 1)],
[(2, 10, 8), (1, 10, 8), (0, 10, 8), (2, 11, 7), (1, 11, 7), (0, 11, 7), (2, 12, 6)]]

qubits = []
all_edges = []
pegasus_vertical_qubits = []
vertical_qubit_edges = []
cubic_qubit = []
cubic_edges = []

heavy_hex_to_remove = [(109, 114), (8, 9)]

PROBLEM_INDEX = 4

parallel_QA_embeddings = []

parallel_cubic_term_embedding_pegasus = []
parallel_cubic_IBMQ_pegasus_variable_mapping = []

for initial_cells in parallel_QA_cells:
	cubic_term_embedding_pegasus = []
	cubic_IBMQ_pegasus_variable_mapping = []
	
	heavy_hex_h_line_1 = [i for i in range(0, 13+1)]+["post-13"]
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
	horizontal_pegasus_lines_for_cubic = []
	
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
				print(cell, temp_pegasus_coordinates)
				pegasus_qubits1 = [coord_to_qubit[a] for a in pegasus_coordinates]
				print(pegasus_qubits1)
				horizontal_pegasus_lines_for_cubic.append(pegasus_qubits1)
				edges_subgraph1 = list(G.subgraph(pegasus_qubits1).edges())
				qubits += pegasus_qubits1
				all_edges += edges_subgraph1
				COUNT = -1
				for qu in all_heavy_hex_lines[cell_line_index]:
					COUNT += 1
					ibm_to_dwave_qubit_embedding[qu] = pegasus_qubits1[COUNT]
	
	for vertical_qubit in vertical_qubit_mappings:
		print(vertical_qubit)
		horizontal_qubits = vertical_qubit_mappings[vertical_qubit]
		n_source = ibm_to_dwave_qubit_embedding[horizontal_qubits[0]]
		n_target = ibm_to_dwave_qubit_embedding[horizontal_qubits[1]]
		min_paths = [p for p in nx.all_shortest_paths(G,source=n_source,target=n_target)]
		
		path = compute_consistent_vertical_qubit_connectors(qubit_to_coord, min_paths, n_source, n_target)
		vert_qubit_pegasus = list(set(path) - set([n_source, n_target]))
		ibm_to_dwave_qubit_embedding[vertical_qubit] = vert_qubit_pegasus[0]
		pegasus_vertical_qubits.append(vert_qubit_pegasus[0])
		H = G.subgraph(path).edges()
		vertical_qubit_edges += H
	
	file = open("problem_instances/ibm_washington_"+str(PROBLEM_INDEX)+".txt", "r")
	problems = ast.literal_eval(file.read())
	file.close()
	
	print("====")
	
	cubic_terms = problems[2][0]
	deg2_map = pull_out_deg2_qubits(cubic_terms)
	
	vertical_pegasus_cubic_qubits = []
	vertical_pegasus_cubic_edges = []
	
	for vertical_qubit in vertical_qubit_mappings:
		try:
			cubic_term = deg2_map[vertical_qubit]
		except:
			continue
		print(cubic_term)
		heavy_hex_top_qubit = cubic_term[1]
		deg2_central_qubit = cubic_term[0]
		heavy_hex_bottom_qubit = cubic_term[2]
		Pegasus_deg2_central_qubit = ibm_to_dwave_qubit_embedding[deg2_central_qubit]
		Pegasus_heavy_hex_top_qubit = ibm_to_dwave_qubit_embedding[heavy_hex_top_qubit]
		Pegasus_heavy_hex_bottom_qubit = ibm_to_dwave_qubit_embedding[heavy_hex_bottom_qubit]
		
		#middle:
		aux_qubit1_pegasus = Pegasus_deg2_central_qubit-15
		#top:
		aux_qubit2_pegasus = Pegasus_heavy_hex_top_qubit+15
		aux_qubit1_pegasus_name = str(heavy_hex_top_qubit)+"*"+str(deg2_central_qubit)+"*"+str(heavy_hex_bottom_qubit)
		aux_qubit2_pegasus_name = str(heavy_hex_top_qubit)+"*"+str(deg2_central_qubit)
		
		ibm_to_dwave_qubit_embedding[aux_qubit1_pegasus_name] = aux_qubit1_pegasus
		ibm_to_dwave_qubit_embedding[aux_qubit2_pegasus_name] = aux_qubit2_pegasus
		
		vertical_pegasus_cubic_qubits.append(aux_qubit1_pegasus)
		vertical_pegasus_cubic_qubits.append(aux_qubit2_pegasus)
		
		vertical_pegasus_cubic_edges.append((Pegasus_deg2_central_qubit, Pegasus_heavy_hex_top_qubit))
		vertical_pegasus_cubic_edges.append((aux_qubit1_pegasus, aux_qubit2_pegasus))
		vertical_pegasus_cubic_edges.append((Pegasus_heavy_hex_bottom_qubit, aux_qubit1_pegasus))
		vertical_pegasus_cubic_edges.append((aux_qubit1_pegasus, Pegasus_heavy_hex_top_qubit))
		vertical_pegasus_cubic_edges.append((aux_qubit1_pegasus, Pegasus_deg2_central_qubit))
		vertical_pegasus_cubic_edges.append((aux_qubit2_pegasus, Pegasus_heavy_hex_top_qubit))
		vertical_pegasus_cubic_edges.append((aux_qubit2_pegasus, Pegasus_deg2_central_qubit))
		
		var_1 = Pegasus_heavy_hex_top_qubit
		var_2 = Pegasus_deg2_central_qubit
		var_3 = Pegasus_heavy_hex_bottom_qubit
		aux_three = aux_qubit1_pegasus
		aux_two = aux_qubit2_pegasus
		IBMQ_to_pegasus = {heavy_hex_top_qubit: var_1, deg2_central_qubit: var_2, heavy_hex_bottom_qubit: var_3, 
			aux_qubit1_pegasus_name: aux_three, aux_qubit2_pegasus_name: aux_two}
		print("vertical cubic term. Clique reduction")
		if cubic_terms[cubic_term] == 1.0:
			print("plus")
			pegasus_plus_r2_lt = {(var_1,): -1, (var_2,): -1, (var_3,): 0, (aux_three,): -1, (aux_two,): -2}
			pegasus_plus_r2_qt = {(var_1, var_2): 1, (aux_three, var_1): 1, (aux_three, var_2): 1, (aux_three, var_3): 1,
				(aux_two, var_1): 2, (aux_two, var_2): 2, (aux_two, aux_three): 2}
			cubic_term_embedding_pegasus.append([pegasus_plus_r2_lt, pegasus_plus_r2_qt])
			poly = dimod.BinaryPolynomial({**pegasus_plus_r2_lt, **pegasus_plus_r2_qt}, dimod.SPIN)
			print(dimod.ExactPolySolver().sample_poly(poly))
		elif cubic_terms[cubic_term] == -1.0:
			print("minus")
			pegasus_minus_r2_lt = {(var_1,): -1, (var_2,): -1, (var_3,): 0, (aux_three,): -1, (aux_two,): -2}
			pegasus_minus_r2_qt = {(var_1, var_2): 1, (aux_three, var_1): 1, (aux_three, var_2): 1, (aux_three, var_3): -1,
				(aux_two, var_1): 2, (aux_two, var_2): 2, (aux_two, aux_three): 2}
			cubic_term_embedding_pegasus.append([pegasus_minus_r2_lt, pegasus_minus_r2_qt])
			poly = dimod.BinaryPolynomial({**pegasus_minus_r2_lt, **pegasus_minus_r2_qt}, dimod.SPIN)
			print(dimod.ExactPolySolver().sample_poly(poly))
	
	pegasus_to_ibm_embedding = invert_ibm_to_dwave_qubit_embedding(ibm_to_dwave_qubit_embedding)
	print(pegasus_to_ibm_embedding)
	
	horizontal_pegasus_cubic_qubits = []
	horizontal_pegasus_cubic_edges = []
	
	for (h_index, horizontal_line) in enumerate(horizontal_pegasus_lines_for_cubic):
		if h_index == 0:
			cubic_form_index = -1
		else:
			cubic_form_index = 0
		for (idx, pegasus_qubit) in enumerate(horizontal_line):
			try:
				cubic_term = deg2_map[pegasus_to_ibm_embedding[pegasus_qubit]]
			except:
				continue
			print(idx, pegasus_qubit)
			if idx%2 == 1:
				cubic_form_index += 1
				if cubic_form_index%2 == 0:
					# This cubic form is the one without the 4-clique
					aux_pegasus_qubit_1 = pegasus_qubit-15
					aux_pegasus_qubit_2 = aux_pegasus_qubit_1-15
					
					var_1 = horizontal_line[idx-1]
					var_2 = pegasus_qubit
					var_3 = horizontal_line[idx+1]
					
					horizontal_pegasus_cubic_edges.append((var_2, aux_pegasus_qubit_1))
					horizontal_pegasus_cubic_edges.append((var_1, aux_pegasus_qubit_1))
					horizontal_pegasus_cubic_edges.append((var_3, aux_pegasus_qubit_1))
					horizontal_pegasus_cubic_edges.append((var_1, aux_pegasus_qubit_2))
					horizontal_pegasus_cubic_edges.append((var_3, aux_pegasus_qubit_2))
					aux_pegasus_qubit_1_name = str(pegasus_to_ibm_embedding[pegasus_qubit])+"*"+str(pegasus_to_ibm_embedding[horizontal_line[idx-1]])+"*"+str(pegasus_to_ibm_embedding[horizontal_line[idx+1]])
					aux_pegasus_qubit_2_name = str(pegasus_to_ibm_embedding[horizontal_line[idx-1]])+"*"+str(pegasus_to_ibm_embedding[horizontal_line[idx+1]])
					ibm_to_dwave_qubit_embedding[aux_pegasus_qubit_1_name] = aux_pegasus_qubit_1
					ibm_to_dwave_qubit_embedding[aux_pegasus_qubit_2_name] = aux_pegasus_qubit_2
					
					IBMQ_to_pegasus = {pegasus_to_ibm_embedding[var_1]: var_1, 
							pegasus_to_ibm_embedding[var_2]: var_2,
							pegasus_to_ibm_embedding[var_3]: var_3,  
							aux_pegasus_qubit_1_name: aux_pegasus_qubit_1,
							aux_pegasus_qubit_2_name: aux_pegasus_qubit_2}
					cubic_IBMQ_pegasus_variable_mapping.append(IBMQ_to_pegasus)
					print("without 4-clique:")
					print(aux_pegasus_qubit_1_name, aux_pegasus_qubit_1)
					print(aux_pegasus_qubit_2_name, aux_pegasus_qubit_2)
					if cubic_terms[cubic_term] == 1.0:
						print("plus")
						plus_r1_lt = {(var_1,): -3, (var_2,): -3, (var_3,): 1, (aux_pegasus_qubit_1,): 6, (aux_pegasus_qubit_2,): 0}
						plus_r1_qt = {(var_1, var_2): 1, (var_2, var_3): -1, (aux_pegasus_qubit_1, var_1): -4, (aux_pegasus_qubit_1, var_2): -4, (aux_pegasus_qubit_1, var_3): 2, 
							(aux_pegasus_qubit_2, var_1): -1, (aux_pegasus_qubit_2, var_3): -1}
						cubic_term_embedding_pegasus.append([plus_r1_lt, plus_r1_qt])
						poly = dimod.BinaryPolynomial({**plus_r1_lt, **plus_r1_qt}, dimod.SPIN)
						print(dimod.ExactPolySolver().sample_poly(poly))
					elif cubic_terms[cubic_term] == -1.0:
						print("minus")
						minus_r1_lt = {(var_1,): -1, (var_2,): -1, (var_3,): -1, (aux_pegasus_qubit_1,): 2, (aux_pegasus_qubit_2,): 0}
						minus_r1_qt = {(var_1, var_2): 3, (var_2, var_3): 1, (aux_pegasus_qubit_1, var_1): -4, (aux_pegasus_qubit_1, var_2): -4, (aux_pegasus_qubit_1, var_3): -2, 
							(aux_pegasus_qubit_2, var_1): -1, (aux_pegasus_qubit_2, var_3): 1}
						#G = create_graph(minus_r1_lt, minus_r1_qt)
						#nx.draw(G, with_labels=True)
						#plt.show()

						cubic_term_embedding_pegasus.append([minus_r1_lt, minus_r1_qt])
						poly = dimod.BinaryPolynomial({**minus_r1_lt, **minus_r1_qt}, dimod.SPIN)
						print(dimod.ExactPolySolver().sample_poly(poly))
				elif cubic_form_index%2 == 1:
					# This cubic form is the one with the 4-clique
					aux_pegasus_qubit_1 = pegasus_qubit-15
					aux_pegasus_qubit_2 = horizontal_line[idx-1]+15
					var_1 = horizontal_line[idx-1]
					var_2 = pegasus_qubit
					var_3 = horizontal_line[idx+1]
					
					horizontal_pegasus_cubic_edges.append((aux_pegasus_qubit_1, var_2))
					horizontal_pegasus_cubic_edges.append((aux_pegasus_qubit_2, var_2))
					horizontal_pegasus_cubic_edges.append((aux_pegasus_qubit_2, var_1))
					horizontal_pegasus_cubic_edges.append((var_1, aux_pegasus_qubit_1))
					horizontal_pegasus_cubic_edges.append((var_3, aux_pegasus_qubit_1))
					horizontal_pegasus_cubic_edges.append((aux_pegasus_qubit_2, aux_pegasus_qubit_1))
					
					aux_pegasus_qubit_1_name = str(pegasus_to_ibm_embedding[horizontal_line[idx-1]])+"*"+str(pegasus_to_ibm_embedding[horizontal_line[idx+1]])+"*"+str(pegasus_to_ibm_embedding[pegasus_qubit])
					aux_pegasus_qubit_2_name = str(pegasus_to_ibm_embedding[pegasus_qubit])+"*"+str(pegasus_to_ibm_embedding[horizontal_line[idx-1]])
					ibm_to_dwave_qubit_embedding[aux_pegasus_qubit_1_name] = aux_pegasus_qubit_1
					ibm_to_dwave_qubit_embedding[aux_pegasus_qubit_2_name] = aux_pegasus_qubit_2
					
					IBMQ_to_pegasus = {pegasus_to_ibm_embedding[var_1]: var_1, 
							pegasus_to_ibm_embedding[var_2]: var_2,
							pegasus_to_ibm_embedding[var_3]: var_3,  
							aux_pegasus_qubit_1_name: aux_pegasus_qubit_1,
							aux_pegasus_qubit_2_name: aux_pegasus_qubit_2}
					cubic_IBMQ_pegasus_variable_mapping.append(IBMQ_to_pegasus)
					print(aux_pegasus_qubit_1_name, aux_pegasus_qubit_1)
					print(aux_pegasus_qubit_2_name, aux_pegasus_qubit_2)
					print("4-clique:")
					if cubic_terms[cubic_term] == 1.0:
						print("plus")
						plus_r1_lt = {(var_1,): -1, (var_2,): -1, (var_3,): 0, (aux_pegasus_qubit_1,): -1, (aux_pegasus_qubit_2,): -2}
						plus_r1_qt = {(var_1, var_2): 1, (aux_pegasus_qubit_1, var_1): 1, (aux_pegasus_qubit_1, var_2): 1, (aux_pegasus_qubit_1, var_3): 1, 
							(aux_pegasus_qubit_2, var_1): 2, (aux_pegasus_qubit_2, var_2): 2, (aux_pegasus_qubit_2, aux_pegasus_qubit_1): 2}
						cubic_term_embedding_pegasus.append([plus_r1_lt, plus_r1_qt])
						poly = dimod.BinaryPolynomial({**plus_r1_lt, **plus_r1_qt}, dimod.SPIN)
						print(dimod.ExactPolySolver().sample_poly(poly))
					elif cubic_terms[cubic_term] == -1.0:
						print("minus")
						minus_r1_lt = {(var_1,): -1, (var_2,): -1, (var_3,): 0, (aux_pegasus_qubit_1,): -1, (aux_pegasus_qubit_2,): -2}
						minus_r1_qt = {(var_1, var_2): 1, (aux_pegasus_qubit_1, var_1): 1, (aux_pegasus_qubit_1, var_2): 1, (aux_pegasus_qubit_1, var_3): -1, 
							(aux_pegasus_qubit_2, var_1): 2, (aux_pegasus_qubit_2, var_2): 2, (aux_pegasus_qubit_2, aux_pegasus_qubit_1): 2}
						cubic_term_embedding_pegasus.append([minus_r1_lt, minus_r1_qt])
						poly = dimod.BinaryPolynomial({**minus_r1_lt, **minus_r1_qt}, dimod.SPIN)
						print(dimod.ExactPolySolver().sample_poly(poly))
				horizontal_pegasus_cubic_qubits.append(aux_pegasus_qubit_1)
				horizontal_pegasus_cubic_qubits.append(aux_pegasus_qubit_2)
	
	cubic_qubit += vertical_pegasus_cubic_qubits+horizontal_pegasus_cubic_qubits
	cubic_edges += vertical_pegasus_cubic_edges+horizontal_pegasus_cubic_edges
	
	ibm_to_dwave_qubit_embedding = remove_edge_qubits(ibm_to_dwave_qubit_embedding)
	print(ibm_to_dwave_qubit_embedding)
	parallel_QA_embeddings.append(ibm_to_dwave_qubit_embedding)
	
	parallel_cubic_term_embedding_pegasus.append(cubic_term_embedding_pegasus)
	parallel_cubic_IBMQ_pegasus_variable_mapping.append(cubic_IBMQ_pegasus_variable_mapping)

file = open("parallel_embeddings/medium_"+str(PROBLEM_INDEX)+".txt", "w")
file.write(str([parallel_cubic_term_embedding_pegasus, parallel_cubic_IBMQ_pegasus_variable_mapping]))
file.close()

draw_pegasus_embedding(nx.Graph(all_edges), qubits, pegasus_vertical_qubits, nx.Graph(vertical_qubit_edges), cubic_qubit, nx.Graph(cubic_edges))
