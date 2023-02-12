''' generate_problem_instance.py
    
    * Functions to generate problem instances from partitions given by generate_IBMdevice_partition.py
'''
import sys

import networkx as nx
import numpy as np
import generate_IBMdevice_partition

from qiskit import IBMQ
IBMQ.load_account()
provider = IBMQ.get_provider(hub='', group='', project='')




''' rlist(n, options)
    Returns a list of length n with random values from options
'''
def rlist(n, options=[-1,1]):
    return [np.random.choice(options) for _ in range(n)]


''' generates list of dictionaries for linear, quadratic and cubic terms, 
    based on input partition
'''
def generate_terms(partition):
    terms = []
    for lst in partition:
        terms.append(dict(zip(lst, rlist(len(lst)))))
    return terms




''' generates IBM instance for
    * device    e.g. "ibmq_brooklyn", "ibm_washington"
    * category  of problem instance
                - easy:     only linear + quadratic terms
                - medium:   easy    + 1 cubic term per central deg2-node
                - hard:     medium  + 1 cubic term per central deg3-node

    * Retrieves partitions using module generate_IBMdevice_partition
    - Node partition:   node_partition = [deg2_nodes, deg3_nodes]
    - Edge partition:   edge_partition = [col1_list, col2_list, col3_list]
    - Triple partit.:   triple_partition = [deg2_triples, deg3_triples]  
'''
def generate_IBMinstance(device="ibm_washington", category="medium"):
    # Get the partitions from generate_IBMdevice_partition
    G, node_partition, edge_partition, triple_partition = generate_IBMdevice_partition.generate_partition(device)

    ## Edit Partitions based on Problem Category
    if (category == "easy"):
        triple_partition = []
    elif (category == "medium"):
        triple_partition = [triple_partition[0]]
    elif (category == "hard"):
        # per deg3 node, remove all except one of the deg3 triples
        deg3_triples = []
        for deg3_node in node_partition[1]:
            options = [(u,v,w) for u,v,w in triple_partition[1] if u == deg3_node]
            deg3_triples.append(options[np.random.choice(range(len(options)))])
        triple_partition[1] = deg3_triples
    else:
        assert False, "Problem instance category '{}' not known".format(category)
        
    node_values = generate_terms(node_partition)
    edge_values = generate_terms(edge_partition)
    triple_values = generate_terms(triple_partition)

    return node_values, edge_values, triple_values
