'''
Kosaraju's algorithm to find the connected components in a directed graph
Prints the leader and the length of its respective connected component,
They are printed in decreasing order according to the length of the scc
'''

# Using a min_heap (we use it as max) is an efficient way to get the k max elements of a list
# in k * O(log(n)) complexity
import heapq



def read_graph(file_name, number_of_vertices, invert_edges=False):
    """
    Read graph into the text file, inverting edges or not
    :param file_name: name of the file text file to read from
    :param number_of_vertices: necessary because the txt file omits lonely vertices instead of listing them like v1: []
    :param invert_edges: set to True to read the edge direction from right to left
    :return: a dict representing an adjacent list of the graph
    """
    graph = {i:[] for i in range(1, number_of_vertices+1)}
    with open(file_name) as file:
        for line in file:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            v1 = int(line_list[0])
            v2 = int(line_list[1])
            if not invert_edges:
                graph[v1].append(v2)
            else:
                graph[v2].append(v1)
    return graph


def dfs_scoring_or_scc(graph, vertex, curr_score, seen, scores, number_of_vertices_in_scc, scoring):
    """
    Do a post-order depth first search. The last action before returning to the parent is to set scores
    if scoring is set to True, or to record the leader and number of vertex in the strong connected component
    if scoring is set to False
    :param graph: the graph to search in
    :param vertex: vertex from which to start the search
    :param curr_score: reference to a list used as a global variable to store the current score
    :param seen: reference to a set used to avoid visiting the same vertex again
    :param scores: reference to a list used to store the score of each vertex
    :param number_of_vertices_in_scc: reference to a list used as a global variable to store the number of vertex in the current scc
    :param scoring: boolean used to specify if the user wants the dfs to do the scoring or the scc routine
    :return: nothing, all information is stored in the global variables provided
    """

    # Iterative DFS routine
    stack = []
    stack.append((vertex, 0))
    seen.add(vertex)
    while stack:
        curr, next_neighbor_index = stack.pop()
        number_of_neighbors = len(graph[curr])
        if number_of_neighbors == 0 or next_neighbor_index >= number_of_neighbors:
            if scoring:
                scores[curr_score[0]] = curr
                curr_score[0] += 1
            else:
                number_of_vertices_in_scc[0] += 1
            continue
        next_neighbor = graph[curr][next_neighbor_index]
        while next_neighbor in seen:
            next_neighbor_index += 1
            if next_neighbor_index < number_of_neighbors:
                next_neighbor = graph[curr][next_neighbor_index]
            else:
                break
        if next_neighbor_index >= number_of_neighbors:
            if scoring:
                scores[curr_score[0]] = curr
                curr_score[0] += 1
            else:
                number_of_vertices_in_scc[0] += 1
            continue
        seen.add(next_neighbor)
        stack.append((curr, next_neighbor_index + 1))
        stack.append((next_neighbor, 0))

# Read graph with edges direction from left to right
file_name = 'graph.txt'
number_of_vertices = 875714
graph = read_graph(file_name, number_of_vertices, invert_edges=True)
seen = set()
curr_score = [0]
number_of_vertices_in_scc = [0]
scores = [0 for _ in range(len(graph))]

# Run the DFS scoring routine starting from every vertex of the graph, avoiding visiting already visited vertices
for vertex in graph:
    if vertex not in seen:
        dfs_scoring_or_scc(graph, vertex, curr_score, seen, scores, number_of_vertices_in_scc, scoring=True)


# Read the same graph from the file, but in reverse order
# The file I/O time is slower than if read from RAM.
# But I made this choice to avoid storing 2 graphs in RAM at the same time
# That would happen if I had used the first graph already in RAM to create the second
# If the graph is so massive that it can't fit in the RAM, the dfs_scoring_scc function
# would need to be modified in order to read from disk everytime there's a need to access the graph.

graph = read_graph(file_name, number_of_vertices)
heap = []
seen = set()
number_of_vertices_in_scc = [0]

# Run the DFS routine to find the strong connected components
# by calling dfs_scoring_scc on every vertex without revisiting
for vertex in reversed(scores):
    if vertex not in seen:

        # used to count the number of vertices in the current scc
        len_seen = len(seen)

        dfs_scoring_or_scc(graph, vertex, curr_score, seen, scores, number_of_vertices_in_scc, scoring=False)
        num_vertices_scc = len(seen) - len_seen

        # the Python heapq offers a min heap.
        # As we want a max-heap, saving the negative of the value
        # and retrieving its negative value after is a trick to simulate a max-heap
        heap.append((-num_vertices_scc, vertex))

# Transform the list heap into a properly minimal heap in O(n) time
heapq.heapify(heap)

# Number of scc's to display (change in order to print more components)
number_of_scc_to_display = 5

for _ in range(number_of_scc_to_display):
    if not heap:
        print('Finished')
        break
    negative_size, leader = heapq.heappop(heap)
    size = - negative_size
    print(f'Leader: {leader}, Size: {size}')
