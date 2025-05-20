import pytholog as pl
from collections import deque
pro_kb = pl.KnowledgeBase("Project")
# Load Prolog facts from the external knowledge base file
pro_kb.consult("knowledge_base.pl")

prolog_adjacency_list = {} # Dictionary to store graph structure (edges and costs) from Prolog facts
prolog_heuristic_values = {} # Dictionary to store heuristic values for nodes from Prolog facts

# Populate prolog_adjacency_list (graph structure) and prolog_heuristic_values (heuristic values) from the knowledge base
# Query for all edge facts
edge_facts = pro_kb.query(pl.Expr("edges(X,Y,Z)"))
# Query for all heuristic facts
heuristic_facts = pro_kb.query(pl.Expr("hs(X,Y)"))

A1 = len(edge_facts)
A2 = len(heuristic_facts)

# Process edge facts to populate prolog_adjacency_list
for i in range(A1):
    edge_fact_dict = edge_facts[i] # Each fact is a dictionary, e.g., {'X': 'a', 'Y': 'z', 'Z': 75}
    edge_values_list = list(edge_fact_dict.values()) # Extract values: ['a', 'z', 75]
    source_node_from_fact = edge_values_list[0] # Source node (e.g., 'a')
    # Convert cost to integer and create a tuple (DestinationNode, Cost)
    edge_data = (edge_values_list[1], int(edge_values_list[2]))
    if source_node_from_fact in prolog_adjacency_list:
        prolog_adjacency_list[source_node_from_fact].append(edge_data)
    else:
        prolog_adjacency_list[source_node_from_fact] = [edge_data]

# Process heuristic facts to populate prolog_heuristic_values
for i in range(A2):
    heuristic_fact_dict = heuristic_facts[i] # Each fact is a dictionary, e.g., {'X': 'a', 'Y': 366}
    heuristic_values_list = list(heuristic_fact_dict.values()) # Extract values: ['a', 366]
    node_from_fact = heuristic_values_list[0] # Node (e.g., 'a')
    prolog_heuristic_values[node_from_fact] = int(heuristic_values_list[1]) # Heuristic value

#print("Graph Structure (prolog_adjacency_list):", prolog_adjacency_list)
#print("Heuristic Values (prolog_heuristic_values):", prolog_heuristic_values)
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    def h(self, n):
        return prolog_heuristic_values[n] # Accessing the global prolog_heuristic_values

    def a_star_algorithm(self, start, stop):
        # open_lst: Set of nodes that have been visited but not all their neighbors have been inspected.
        # Starts initialized with the start node.
        open_lst = set([start])
        # closed_lst: Set of nodes that have been visited and all their neighbors have been inspected.
        closed_lst = set([])

        # g_scores: Stores the actual cost (g-value) from the start_node to any given node.
        g_scores = {}
        g_scores[start] = 0 # Cost from start to start is 0.

        # parents: Maps a node to its predecessor in the path from the start_node.
        # Used for reconstructing the path once the goal is reached.
        parents = {}
        parents[start] = start # The start node has no predecessor.

        while len(open_lst) > 0:
            current_node = None

            # Select node from open_lst with the lowest f-score (f = g + h).
            # This is the core of the A* algorithm's greedy but informed search.
            for candidate_node in open_lst:
                if current_node is None or g_scores[candidate_node] + self.h(candidate_node) < g_scores[current_node] + self.h(current_node):
                    current_node = candidate_node

            if current_node is None:
                # This should not happen if a path exists and open_lst was not empty.
                # Indicates an issue or that the graph is disconnected and goal is unreachable.
                print('Path does not exist!')
                return None

            # If the current_node is the stop_node, reconstruct and return the path.
            if current_node == stop:
                reconstructed_path = []
                # Trace back from stop_node to start_node using the parents map.
                while parents[current_node] != current_node:
                    reconstructed_path.append(current_node)
                    current_node = parents[current_node]
                reconstructed_path.append(start) # Add the start_node itself.
                reconstructed_path.reverse() # The path was traced backwards, so reverse it.
                print('Path found: {}'.format(reconstructed_path))
                return reconstructed_path

            # Process neighbors of the current_node.
            for (neighbor_node, weight) in self.get_neighbors(current_node):
                # If neighbor_node has not been visited (i.e., not in open_lst or closed_lst):
                # Add it to open_lst for future exploration.
                # Record current_node as its parent and calculate its g_score.
                if neighbor_node not in open_lst and neighbor_node not in closed_lst:
                    open_lst.add(neighbor_node)
                    parents[neighbor_node] = current_node
                    g_scores[neighbor_node] = g_scores[current_node] + weight
                # Else, if neighbor_node has been visited (is in open_lst or potentially closed_lst):
                # Check if the path through current_node offers a shorter g_score to reach neighbor_node.
                else:
                    # If a shorter path to neighbor_node is found via current_node:
                    if g_scores.get(neighbor_node, float('inf')) > g_scores[current_node] + weight:
                        g_scores[neighbor_node] = g_scores[current_node] + weight
                        parents[neighbor_node] = current_node
                        # If neighbor_node was in closed_lst, it means we found a better path to it.
                        # So, it needs to be re-evaluated; move it back to open_lst.
                        if neighbor_node in closed_lst:
                            closed_lst.remove(neighbor_node)
                            open_lst.add(neighbor_node)

            # Move current_node from open_lst to closed_lst:
            # All its neighbors have been inspected.
            open_lst.remove(current_node)
            closed_lst.add(current_node)

        print('Path does not exist!')
        return None
graph1 = Graph(prolog_adjacency_list) # Use the renamed variable for instantiation
source=input('Enter the Source name:').lower()
destination=input('Enter the Desitination Name:').lower()
graph1.a_star_algorithm(source,destination)

