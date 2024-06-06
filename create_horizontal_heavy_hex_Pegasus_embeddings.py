from itertools import cycle
import dwave_networkx as dnx
from dwave_networkx.drawing.pegasus_layout import draw_pegasus
import matplotlib.pyplot as plt
import networkx as nx


other_cell_coordinates2 = [(2, 0, 2), (1, 0, 3), (0, 0, 4), (2, 1, 4), (1, 1, 5), (0, 1, 6), (2, 2, 6), (1, 2, 7), (0, 2, 8), (2, 3, 8)]


def extract_pegasus_coords(data):
	out = {}
	for element in data:
		coord = element[0]
		qubit = element[1]["linear_index"]
		out[coord] = qubit
	return out

def get_pegasus_cell_coordinates_horizontal_heavy_hex(N, initial_cell):
	new_cells = [initial_cell]
	if initial_cell[0] == 2:
		pool = cycle([1, 0, 2])
	elif initial_cell[0] == 1:
		pool = cycle([0, 2, 1])
	elif initial_cell[0] == 0:
		pool = cycle([2, 1, 0])
	index_zero_list = [next(pool) for a in range(N)]
	
	index_two_list = []
	MOD = initial_cell[2]%2
	assert MOD==1, "To make things simple, we enfore that the first coordinate has an odd number in the 3rd index coordinate"
	offset = initial_cell[2]
	while len(index_two_list) < N:
		if MOD == 0:
			index_two_list.append(offset+1)
			MOD = 1
		elif MOD == 1:
			index_two_list.append(offset+1)
			index_two_list.append(offset+1)
			MOD = 0
		offset = offset+1
	
	index_one_list = []
	offset = initial_cell[1]
	COUNT = 0
	while len(index_one_list) < N:
		COUNT += 1
		if COUNT == 1:
			index_one_list.append(offset)
		else:
			index_one_list.append(offset)
			index_one_list.append(offset)
			index_one_list.append(offset)
		offset += 1
	
	for i in range(N-1):
		new_cells.append((index_zero_list[i], index_one_list[i], index_two_list[i]))	
	return new_cells
def get_pegasus_cell_coordinates_horizontal_heavy_hex_version2(N, initial_cell):
	new_cells = [initial_cell]
	if initial_cell[0] == 2:
		pool = cycle([1, 0, 2])
	elif initial_cell[0] == 1:
		pool = cycle([0, 2, 1])
	elif initial_cell[0] == 0:
		pool = cycle([2, 1, 0])
	index_zero_list = [next(pool) for a in range(N)]
	
	index_two_list = []
	MOD = initial_cell[2]%2
	assert MOD==0, "To make things simple, we enfore that the first coordinate has an even number in the 3rd index coordinate"
	offset = initial_cell[2]
	while len(index_two_list) < N:
		if MOD == 0:
			index_two_list.append(offset+1)
			index_two_list.append(offset+1)
			MOD = 1
		elif MOD == 1:
			index_two_list.append(offset+1)
			MOD = 0
		offset = offset+1
	
	index_one_list = []
	offset = initial_cell[1]
	COUNT = 0
	while len(index_one_list) < N:
		COUNT += 1
		if COUNT == 1:
			index_one_list.append(offset)
		else:
			index_one_list.append(offset)
			index_one_list.append(offset)
			index_one_list.append(offset)
		offset += 1
	
	for i in range(N-1):
		new_cells.append((index_zero_list[i], index_one_list[i], index_two_list[i]))	
	return new_cells
def get_pegasus_cell_coordinates_horizontal_heavy_hex_version3(N, initial_cell):
	new_cells = [initial_cell]
	if initial_cell[0] == 2:
		pool = cycle([1, 0, 2])
	elif initial_cell[0] == 1:
		pool = cycle([0, 2, 1])
	elif initial_cell[0] == 0:
		pool = cycle([2, 1, 0])
	index_zero_list = [next(pool) for a in range(N)]
	
	index_two_list = []
	MOD = initial_cell[2]%2
	assert MOD==0, "To make things simple, we enfore that the first coordinate has an even number in the 3rd index coordinate"
	offset = initial_cell[2]
	while len(index_two_list) < N:
		if MOD == 0:
			index_two_list.append(offset+1)
			index_two_list.append(offset+1)
			MOD = 1
		elif MOD == 1:
			index_two_list.append(offset+1)
			MOD = 0
		offset = offset+1
	
	index_one_list = []
	offset = initial_cell[1]
	COUNT = 0
	while len(index_one_list) < N:
		COUNT += 1
		if COUNT == 1:
			index_one_list.append(offset)
			index_one_list.append(offset)
		else:
			index_one_list.append(offset)
			index_one_list.append(offset)
			index_one_list.append(offset)
		offset += 1
	
	for i in range(N-1):
		new_cells.append((index_zero_list[i], index_one_list[i], index_two_list[i]))	
	return new_cells

def extend_intercell_coordinates(new_cells):
	qubit_coordinates = []
	for coord in new_cells:
		new_coord = (coord[0], coord[1], coord[2], 0, 0)
		qubit_coordinates.append(new_coord)
		new_coord = (coord[0], coord[1], coord[2], 1, 3)
		qubit_coordinates.append(new_coord)
	return qubit_coordinates
def draw_pegasus_embedding(edges_subgraph, pegasus_qubits):
	G = dnx.pegasus_graph(16)
	labeldict = {}
	node_colors = []
	for a in list(G.nodes()):
		if a in pegasus_qubits:
			node_colors.append("orange")
		else:
			node_colors.append("gray")
	edge_colors = []
	for e in list(G.edges()):
		if edges_subgraph.has_edge(*e) == True:
			edge_colors.append("orange")
		else:
			edge_colors.append("gray")
	draw_pegasus(G, with_labels=True, font_size=1, node_size=14, node_color=node_colors, edge_color=edge_colors, width=0.2, alpha=1)#, labels=labeldict)
	fig = plt.gcf()
	fig.set_size_inches(40, 40)
	plt.savefig("figures/heavy_hex_embedding.pdf", bbox_inches='tight', pad_inches=-1.5, dpi=300)
	plt.close()

combined_horizontal_pegasus_cells = []
combined_horizontal_qubit_pegasus_coordinates = []
combined_horizontal_qubit_numbers = []

G = dnx.pegasus_graph(16)

pegasus = dnx.pegasus_graph(16, nice_coordinates=True)
pegasus_coordinates = pegasus.nodes(data=True)
coord_to_qubit = extract_pegasus_coords(pegasus_coordinates)


initial_cells = []
for vertical_index in range(14):
	initial_cells.append((1, vertical_index, 1))

initial_cells += [(1, 0, 3), (1, 0, 5), (1, 0, 7), (1, 0, 9), (1, 0, 11), (1, 0, 13)]

qubits = []
all_edges = []

for cell in initial_cells:
	horizontal_length = 21
	while True:
		try:
			new_cells = get_pegasus_cell_coordinates_horizontal_heavy_hex(horizontal_length, cell)
			qubit_coordinates = extend_intercell_coordinates(new_cells)
			pegasus_qubits1 = [coord_to_qubit[a] for a in qubit_coordinates]
			break
		except:
			horizontal_length = horizontal_length-1
			continue
	print(new_cells)
	edges_subgraph1 = list(G.subgraph(pegasus_qubits1).edges())
	qubits += pegasus_qubits1
	all_edges += edges_subgraph1
	combined_horizontal_pegasus_cells.append(new_cells)
	combined_horizontal_qubit_pegasus_coordinates.append(qubit_coordinates)
	combined_horizontal_qubit_numbers.append(qubits)


initial_cells = []

for vertical_index in range(14):
	initial_cells.append((1, vertical_index, 0))


initial_cells += [(1, 0, 2)]

for cell in initial_cells:
	horizontal_length = 22
	while True:
		try:
			new_cells = get_pegasus_cell_coordinates_horizontal_heavy_hex_version2(horizontal_length, cell)
			qubit_coordinates = extend_intercell_coordinates(new_cells)
			pegasus_qubits1 = [coord_to_qubit[a] for a in qubit_coordinates]
			break
		except Exception as e:
			#print(e)
			horizontal_length = horizontal_length-1
			continue
	print(cell, "==", new_cells)
	edges_subgraph1 = list(G.subgraph(pegasus_qubits1).edges())
	qubits += pegasus_qubits1
	all_edges += edges_subgraph1
	combined_horizontal_pegasus_cells.append(new_cells)
	combined_horizontal_qubit_pegasus_coordinates.append(qubit_coordinates)
	combined_horizontal_qubit_numbers.append(qubits)


comb = nx.Graph(all_edges)

draw_pegasus_embedding(comb, qubits)

unique = []
non_unique = []
for term in combined_horizontal_pegasus_cells:
	for a in term:
		non_unique.append(a)
		if a not in unique:
			unique.append(a)

print(len(non_unique), len(unique))

file = open("horizontal_line_embeddings/embeddings.txt", "w")
file.write(str([combined_horizontal_pegasus_cells, combined_horizontal_qubit_pegasus_coordinates, combined_horizontal_qubit_numbers]))
file.close()


