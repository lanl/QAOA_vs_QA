# QAOA_vs_QA
This repository contains the code and data associated with the paper [Quantum Annealing vs. QAOA: 127 Qubit Higher-Order Ising Problems on NISQ Computers](https://arxiv.org/abs/2301.00520)

- `generate_QAOA_circuit.py` This python script contains the code methods which generate the QAOA circuits using Qiskit. This script can generate a QAOA circuit for cubic or quadratic problem instances. 
- `generate_problem_instance.py` can generate these problem instances, defined in the heavy hex graph of an IBMQ device. 
   - `problem_instances/` contains 100 fixed problem instances (defined on the ibm_washington hardware graph, at some point in the past meaning the active CNOTs and qubits may be slightly different). The first 10 of these problems define the instances used in the papers. 
- `generate_IBMdevice_partition.py` contains additional functions used for generating a QAOA circuit. 
- `create_medium_instance_ibm_washington_parallel.py` generates the tiled parallel quantum annealing embeddings for the problem instances with cubic terms. The problem instanes with those cubic terms removed can also be embedded using these computed embeddings. 
   - `parallel_embeddings/` contains the tiled embeddings for a logical Pegasus P_16 QA hardware graph. 


## How to Cite?
bibtex:
```latex
@misc{QAOA_vs_QA_127,
  doi = {10.48550/ARXIV.2301.00520},
  url = {https://arxiv.org/abs/2301.00520},
  author = {Pelofske, Elijah and Bärtschi, Andreas and Eidenbenz, Stephan},
  title = {Quantum Annealing vs. QAOA: 127 Qubit Higher-Order Ising Problems on NISQ Computers},
  year = {2023},
}
```

## Authors
- [Elijah Pelofske](mailto:epelofske@lanl.gov): Information Sciences, Los Alamos National Laboratory
- [Andreas Bärtschi](mailto:baertschi@lanl.gov): Information Sciences, Los Alamos National Laboratory
- Stephan Eidenbenz: Information Sciences, Los Alamos National Laboratory

## Copyright Notice:
© 2022. Triad National Security, LLC. All rights reserved.
This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos
National Laboratory (LANL), which is operated by Triad National Security, LLC for the U.S.
Department of Energy/National Nuclear Security Administration. All rights in the program are
reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear
Security Administration. The Government is granted for itself and others acting on its behalf a
nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare
derivative works, distribute copies to the public, perform publicly and display publicly, and to permit
others to do so.

**LANL C Number: C22038**

## License:
This program is open source under the BSD-3 License.
Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and
the following disclaimer.
 
2.Redistributions in binary form must reproduce the above copyright notice, this list of conditions
and the following disclaimer in the documentation and/or other materials provided with the
distribution.
 
3.Neither the name of the copyright holder nor the names of its contributors may be used to endorse
or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
