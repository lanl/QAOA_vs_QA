# Problem instances

This directory contains 100 problem instances, defined on the hardware graph of ibm_washington

Each instance is different, and the coefficients of +1/-1 were randomly chosen. 

For the papers that used these instances, we used the first 10. The rest are mostly for reference in case anyone is interested in using them. 

The problem instances with quadratic terms only (no cubic terms) were formed by simply using the linear and quadratic terms of these instances, and not using the cubic terms. 

The format of these instances is defined as follows. Index 0 is the linear terms, index 1 is the quadratic terms, and index 2 is the cubic terms. 
The linear terms are split into two separate dictionaries, corresponding to the bipartition of the heavy-hex graph. 
The quadratic terms are split into three separate dictionaries, corresponding to a 3 edge coloring of the heavy-hex graph. 
