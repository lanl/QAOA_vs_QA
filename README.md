# QAOA_vs_QA
This repository contains the code and data associated with the paper [Quantum Annealing vs. QAOA: 127 Qubit Higher-Order Ising Problems on NISQ Computers](https://arxiv.org/abs/2301.00520)
Along with the extended paper [Short-Depth QAOA Circuits and Quantum Annealing on Higher-Order Ising Models](https://www.nature.com/articles/s41534-024-00825-w)

- `generate_QAOA_circuit.py` This python script contains the code methods which generate the QAOA circuits using Qiskit. This script can generate a QAOA circuit for cubic or quadratic problem instances. 
- `generate_problem_instance.py` can generate these problem instances, defined in the heavy hex graph of an IBMQ device. 
   - `problem_instances/` contains 100 fixed problem instances (defined on the ibm_washington hardware graph, at some point in the past meaning the active CNOTs and qubits may be slightly different). The first 10 of these problems define the instances used in the papers. 
- `generate_IBMdevice_partition.py` contains additional functions used for generating a QAOA circuit. 
- `create_medium_instance_ibm_washington_parallel.py` generates the tiled parallel quantum annealing embeddings for the problem instances with cubic terms. The problem instanes with those cubic terms removed can also be embedded using these computed embeddings. 
   - `parallel_embeddings/` contains the tiled embeddings for a logical Pegasus P_16 QA hardware graph. 
- `figures/` contains QA embedding figures
- `QAOA_2_round_DD_volumetric_plots/` and `QAOA_2_round_volumetric_plots` contains 2-round QAOA 3-d volumetric isomorphic surface heatmap plots, which show the searched parameter space of the QAOA angles. Each plot comes as both a pdf and an html which helps for 3d viewing. The filename format is `problem_idx_beta`. `problem` is either cubic or quadratic. `idx` is the 0-9 problem index. `beta` is the beta angle 0-4 index (each 2-round QAOA search space is represented by 5 of these 3d plots). 
- `execute_quadratic_instance_quantum_annealing.py` uses a set of fixed Pegasus embeddings, defined in `parallel_embeddings/`, in order to embed and run one of the heavy-hex Ising models on aa D-Wave quantum annealer. 
Note that this code is an example where a single set of anneal parameters are used, and the results are written to a single JSON file. 


### Workflow

The general workflow to generate and run a problem on a D-Wave quantum annealer is as follows. 
- Run `generate_problem_instance.py` on the specific heavy-hex hardware you may wish to define new problem instances on. In this case, we have many instances stored in `problem_instances/` and `additional_heavy_hex_higher_order_Ising_models/`.

- Run `create_cubic_instance_ibm_washington_parallel.py` for one of the problem instances with cubic terms.  
This code creates parallel embeddings of the problem insance, on a logical Pegasus graph. This code then saves that data as a text file, such as `parallel_embeddings/medium_1.txt`. 
The code `create_quadratic_instance_ibm_washington_parallel.py` does the same thing, but for the problem instances with no cubic terms. Importantly, for the quadratic problem instances, 
we only need one set of these embeddings. For the cubic terms, because of the order reduction, we need a different embedding for each problem instance. 
The script `create_horizontal_heavy_hex_Pegasus_embeddings.py` is required to run either of these embedding scripts, but the output from that is already saved in `horizontal_line_embeddings`, so unless you are running this on a new D-Wave device, this step is not required. 

- Run `execute_quadratic_instance_quantum_annealing.py` to sample one of the quadratic problem instances. 
Run `execute_cubic_instance_quantum_annealing.py` to sample one of the problem instances with cubic terms. 


# Scaling Whole-Chip QAOA for Higher-Order Ising Spin Glass Models on Heavy-Hex Graphs
The class of Ising models that contain geometrically local cubic terms and are defined on heavy-hex graphs was then used in a subsequent study titled 
[Scaling Whole-Chip QAOA for Higher-Order Ising Spin Glass Models on Heavy-Hex Graphs](https://arxiv.org/abs/2312.00997)

This study used several additional hardware graph defined Ising models on 16, 27, 127, and 414 qubit heavy hex graphs. 
- `additional_heavy_hex_higher_order_Ising_models/` contains the Ising models used in this study. Note that the study also does report results from `ibm_washington` hardware graph defined Ising models (run on `ibm_washington`). 


## How to Cite?
QAOA vs. QA studies bibtex:
```latex
@article{QA_vs_QAOA_127,
  author        = {Pelofske, Elijah and B{\"{a}}rtschi, Andreas and Eidenbenz, Stephan},
  booktitle     = {International Conference on High Performance Computing ISC HPC'23},
  title         = {{Quantum Annealing vs. QAOA: 127 Qubit Higher-Order Ising Problems on NISQ Computers}},
  year          = {2023},
  month         = may,
  pages         = {240--258},
  archiveprefix = {arXiv},
  doi           = {10.1007/978-3-031-32041-5_13},
  eprint        = {2301.00520},
}

@article{Short_Depth_QAOA_QA,
  author   = {Pelofske, Elijah and B{\"{a}}rtschi, Andreas and Eidenbenz, Stephan},
  journal  = {npj Quantum Information},
  title    = {{Short-Depth QAOA Circuits and Quantum Annealing on Higher-Order Ising Models}},
  year     = {2024},
  month    = march,
  doi      = {10.1038/s41534-024-00825-w},
}
```

Scaling QAOA study bibtex entry:
```
@article{QAOA_heavy_hex_scaling,
      title={{Scaling Whole-Chip QAOA for Higher-Order Ising Spin Glass Models on Heavy-Hex Graphs}}, 
      author={Elijah Pelofske and Andreas Bärtschi and Lukasz Cincio and John Golden and Stephan Eidenbenz},
      year={2023},
      eprint={2312.00997},
      archivePrefix={arXiv},
      primaryClass={quant-ph}
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
