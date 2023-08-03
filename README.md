# Kosarajus-Algorithm
An algorithm to find all the strong connected components (leader and size) of a directed graph in O(n + m) time.

Each line of the input text file should represent an edge as 'v1 v2'.

### The algorithm has 2 phases:
-  1- DFS is run on every vertex of the reverse graph (each edge is inverted), giving a unique score to each vertex (from 1 to the number of vertices of the graph)
-  2- DFS is run again, this time on every vertex of the original graph, from the top scorer to the lowest scorer, avoiding revisiting, and recovering the
  leader and size of every strong connected component

*The graph and reverse graph of 1 and 2 can be interchanged without affecting the result, because the structure of the scc's are preserved*
