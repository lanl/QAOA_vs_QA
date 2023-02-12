''' generate_problem_instance.py
    
    * Functions to turn problem instances given by generate_problem_instance.py
    * into a circuit for the corresponding device
'''
import sys

import networkx as nx
import numpy as np
import generate_IBMdevice_partition

from qiskit import IBMQ
from qiskit import QuantumCircuit
IBMQ.load_account()
provider = IBMQ.get_provider(hub='', group='', project='')




''' generates QAOA circuit with
    * phase separator H_P (angles gamma)
      = cost function H_C consisting of:
        - linear terms:     node_values = [deg2_nodes_dict, deg3_nodes_dict]
        - quadratic terms:  edge_values = [col1_dict, col2_dict, col3_dict]
        - cubic terms:      triple_values = [deg2_triples_dict] # no hard instances, otherwise [deg2_triples_dict, deg3_triples_dict]
    * mixer SUM X_i (angles beta)
'''

def generate_QAOA(node_values, edge_values, triple_values, beta, gamma):
    assert (len(beta) == len(gamma)), "Number of rounds not uniquely defined"
    assert (len(triple_values) <= 1), "Currently no circuits for hard instances"
 
    node_list = list(set(node_values[0].keys()) | set(node_values[1].keys()))
    #print(node_list)
    num_levels = len(beta)
    num_nodes = max(node_list)+1 # allows for non-used qubits

    ## Circ Init
    circ = QuantumCircuit(num_nodes)
    circ.h(node_list)
    # QAOA rounds
    for level in range(num_levels):
        ## Phase Separator
        # -> linear terms
        #circ.barrier()
        for node_values_dict in node_values:
            for qubit, linear_term in node_values_dict.items():
                circ.rz(2*gamma[level]*linear_term, qubit)
        # -> quadratic terms, compute parity
        #circ.barrier()
        marked_nodes = np.zeros(num_nodes)
        colors = [0,1,2]
        for color in colors: 
            for edge, quadratic_term in edge_values[color].items():
                (target, control) = edge
                circ.cnot(control, target)
                if (marked_nodes[target] == 0):
                    circ.rz(2*gamma[level]*quadratic_term, target)
                    marked_nodes[target] = 1
        # -> cubic terms, deg2 nodes only
        #circ.barrier()
        if len(triple_values) > 0:
            for triple, cubic_term in triple_values[0].items():
                (target, _, _) = triple
                circ.rz(2*gamma[level]*cubic_term, target)
        # -> quadratic terms, uncompute parity
        #circ.barrier()
        marked_nodes = np.zeros(num_nodes)
        colors = [0,1,2]
        for color in colors:
            for edge, quadratic_term in edge_values[color].items():
                (target, control) = edge
                if (marked_nodes[target] == 1):
                    circ.rz(2*gamma[level]*quadratic_term, target)
                elif (marked_nodes[control] == 0):                    
                    marked_nodes[target] = 1
                circ.cnot(control, target)                
        ## Mixer
        #circ.barrier()
        circ.rx(2*beta[level], node_list)

    ## Measure
    circ.measure_all()
    return circ



