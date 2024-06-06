"""
Run quadratic heavy-hex Ising models on a D-Wave quantum annealer
"""

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

samples = run(parallel_embedded_ising_h, parallel_embedded_ising_j, params)

file = open("results.json", "w")
json.dump(samples, file)
file.close()

