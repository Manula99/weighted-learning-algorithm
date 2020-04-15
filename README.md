# weighted-learning-algorithm
## Problem Description:
A known number of bots are lost in a weighted graph. The goal is to locate and return the bots to the designated home vertex. A set of one-hundred scouts are given to locate the bots. Each scout called on a given vertex returns true if they believe a bot is present. However, each scout provides false information on some unknown subset of the vertices. Two functions are provided to interact with the graph: 
### Scout(v, s):
Given a vertex v and a set of scouts s, the fucntion scouts the vertex with each scout. The function returns a dictionary matching each scout to their response. The cost of this function is equal to the size set s.
### Remote(v1, v2):
Given two vertices v1 and v2, this function moves any bots in v1 to v2 and returns the number of bots moved. The function cost is the edge weight of v1 -> v2. The cost will incur even if zero bots are moved.
### Algorithm Evaluation:
The overall efficiency of an algorithm is measured by the cumulative cost of its function calls. 
