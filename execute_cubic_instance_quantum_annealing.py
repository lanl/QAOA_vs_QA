import json
import networkx as nx
from dwave.cloud import Client
import time
import ast
import copy
from dwave import embedding

def Start_DWave_connection(device):
    client = Client.from_config()
    DWave_solver = client.get_solver(device)
    A = DWave_solver.undirected_edges
    connectivity_graph = nx.Graph(list(A))
    return connectivity_graph, DWave_solver
def run(h, j, params):
	while (True):
		try:
			sampleset = solver.sample_ising(h, j, answer_mode='raw', **params)
			return sampleset.samples
		except Exception as e:
			print(e)
			time.sleep(1)
			continue
def adapt_native_embedding(embedding_dict_in):
	embedding_dict = copy.deepcopy(embedding_dict_in)
	out = {}
	for a in embedding_dict:
		out[a] = [embedding_dict[a]]
	return out
def remove_zero_terms(h, J):
	to_remove = []
	for n in h:
		if h[n] == 0.0:
			to_remove.append(n)
	to_remove_J = []
	for e in J:
		if J[e] == 0.0:
			to_remove_J.append(e)
	for n in to_remove:
		del h[n]
	for e in to_remove_J:
		del J[e]
	return h, J
def merge_cubic_terms(h_easy_parallel, J_easy_parallel, medium_parallel, Target, used_embeddings):
	filtered_used_embeddings = []
	for (parallel_emb_index, parallel_Ising) in enumerate(medium_parallel):
		pre_h_easy_parallel = copy.deepcopy(h_easy_parallel)
		pre_J_easy_parallel = copy.deepcopy(J_easy_parallel)
		missing_nodes = []
		missing_edges = []
		valid_INDICATOR = True
		for I in parallel_Ising:
			lin = I[0]
			quad = I[1]
			modified_h = {}
			for k in lin:
				modified_h[k[0]] = lin[k]
			for var in modified_h:
				if Target.has_node(var) == False:
					valid_INDICATOR = False
					missing_nodes.append(var)
				if var in h_easy_parallel:
					weight = h_easy_parallel[var]
					h_easy_parallel[var] = weight+modified_h[var]
				else:
					h_easy_parallel[var] = modified_h[var]
			for edge in quad:
				if Target.has_edge(*edge) == False:
					valid_INDICATOR = False
					missing_edges.append(edge)
				IND1 = edge in J_easy_parallel
				edge_flipped = tuple(reversed(edge))
				IND2 = edge_flipped in J_easy_parallel
				if IND1 == True:
					weight = J_easy_parallel[edge]
					J_easy_parallel[edge] = quad[edge]+weight
				elif IND2 == True:
					weight = J_easy_parallel[edge_flipped]
					J_easy_parallel[edge_flipped] = quad[edge]+weight
				else:
					J_easy_parallel[edge] = quad[edge]
		node_fails = []
		edge_fails = []
		for node in missing_nodes:
			if h_easy_parallel[node] != 0:
				node_fails.append(node)
		for edge in missing_edges:
			edge_flipped = tuple(reversed(edge))
			IND1 = edge in J_easy_parallel
			IND2 = edge_flipped in J_easy_parallel
			if IND1 == True:
				if J_easy_parallel[edge] != 0:
					edge_fails.append(edge)
			elif IND2 == True:
				if J_easy_parallel[edge_flipped] != 0:
					edge_fails.append(edge_flipped)
		if len(node_fails+edge_fails) != 0:
			valid_INDICATOR = False
		else:
			valid_INDICATOR = True
		if valid_INDICATOR == False:
			h_easy_parallel = pre_h_easy_parallel
			J_easy_parallel = pre_J_easy_parallel
		if valid_INDICATOR == True:
			filtered_used_embeddings.append([used_embeddings[parallel_emb_index], medium_parallel[parallel_emb_index]])
	h_easy_parallel, J_easy_parallel = remove_zero_terms(h_easy_parallel, J_easy_parallel)
	return h_easy_parallel, J_easy_parallel, filtered_used_embeddings

file = open("parallel_embeddings/easy.txt", "r")
parallel_embeddings = ast.literal_eval(file.read())
file.close()

QA_device = "Advantage_system4.1"
Target, solver = Start_DWave_connection(QA_device)

#Annealing time and anneal schedule
AT = 100
s = 0.5
duration_frac = 0.5
heavy_hex_rep_idx = 0


duration = AT*duration_frac
start = (AT-duration)/2.0
end = ((AT-duration)/2.0)+duration
anneal_schedule = [[0, 0], [start, s], [end, s], [AT, 1]]

params = {"num_reads": 1000, "anneal_schedule": anneal_schedule}
IBMQ_device = "ibm_washington"

file = open("fixed_problems/"+IBMQ_device+"_"+str(heavy_hex_rep_idx)+".txt", "r")
instance = ast.literal_eval(file.read())
file.close()

h = {}
for a in instance[0]:
	h = {**h, **a}
J = {}
for a in instance[1]:
	J = {**J, **a}

file = open("parallel_embeddings/medium_"+str(heavy_hex_rep_idx)+".txt", "r")
cubic_term_reductions = ast.literal_eval(file.read())[0]
file.close()

used_embeddings = []
parallel_embedded_ising_j = {}
parallel_embedded_ising_h = {}
for embedding_dict in parallel_embeddings:
		try:
			embedding_dict_adapt = adapt_native_embedding(embedding_dict)
			embedded_h, embedded_j = embedding.embed_ising(h, J, embedding_dict_adapt, Target)
			used_embeddings.append(embedding_dict)
			parallel_embedded_ising_j = {**parallel_embedded_ising_j, **embedded_j}
			parallel_embedded_ising_h = {**parallel_embedded_ising_h, **embedded_h}
		except Exception as e:
			pass

parallel_embedded_ising_h, parallel_embedded_ising_j, filtered_used_embeddings = merge_cubic_terms(parallel_embedded_ising_h, parallel_embedded_ising_j, cubic_term_reductions, Target, parallel_embeddings)

samples = run(parallel_embedded_ising_h, parallel_embedded_ising_j, params)

file = open("results.json", "w")
json.dump(samples, file)
file.close()

