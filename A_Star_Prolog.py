from pyswip import Prolog

# Initialize the Prolog engine
prolog = Prolog()
# Load the knowledge base from the specified Prolog file
prolog.consult("knowledge_base.pl")

# --- Data Loading from Prolog ---

# Dictionary to store the graph's adjacency list (e.g., {'a': [('b', 10), ('c', 20)]})
prolog_adjacency_list = {}
# Dictionary to store the heuristic value for each node (e.g., {'a': 100, 'b': 50})
prolog_heuristic_values = {}

# Query the Prolog knowledge base for all edge facts (edges/3)
# The result is a list of dictionaries, where each dictionary represents a fact
edge_facts = list(prolog.query("edges(X, Y, Z)"))

# Process the edge facts to populate the adjacency list
for fact in edge_facts:
    source_node = fact['X']
    dest_node = fact['Y']
    cost = fact['Z']

    # If the source node is already in the adjacency list, append the new edge
    if source_node in prolog_adjacency_list:
        prolog_adjacency_list[source_node].append((dest_node, cost))
    # Otherwise, create a new entry for the source node
    else:
        prolog_adjacency_list[source_node] = [(dest_node, cost)]

# Query the Prolog knowledge base for all heuristic facts (hs/2)
heuristic_facts = list(prolog.query("hs(X, Y)"))

# Process the heuristic facts to populate the heuristic values dictionary
for fact in heuristic_facts:
    node = fact['X']
    heuristic_value = fact['Y']
    prolog_heuristic_values[node] = heuristic_value

# --- A* Algorithm Implementation ---

class Graph:
    """
    Represents a graph and contains the A* algorithm implementation.
    """
    def __init__(self, adjac_lis):
        """
        Initializes the graph with an adjacency list.
        :param adjac_lis: The adjacency list representing the graph's structure.
        """
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        """
        Retrieves the neighbors of a given node.
        :param v: The node to get the neighbors of.
        :return: A list of tuples, where each tuple contains a neighbor and the cost to reach it.
        """
        return self.adjac_lis.get(v, [])

    def h(self, n):
        """
        Retrieves the heuristic value for a given node.
        :param n: The node to get the heuristic value of.
        :return: The heuristic value of the node, or infinity if the node is not found.
        """
        return prolog_heuristic_values.get(n, float('inf'))

    def a_star_algorithm(self, start, stop):
        """
        Implements the A* search algorithm to find the shortest path from a start to a stop node.
        :param start: The starting node.
        :param stop: The target node.
        :return: A list representing the path from the start to the stop node, or None if no path is found.
        """
        # Set of nodes to be evaluated
        open_lst = {start}
        # Set of nodes already evaluated
        closed_lst = set()
        # Dictionary to store the cost from the start node to each node
        g_scores = {start: 0}
        # Dictionary to reconstruct the path
        parents = {start: start}

        while open_lst:
            # Get the node in the open list with the lowest f-score (g-score + h-score)
            current_node = min(open_lst, key=lambda n: g_scores[n] + self.h(n))

            # If the current node is the stop node, we have found the path
            if current_node == stop:
                reconstructed_path = []
                # Reconstruct the path by traversing from the stop node to the start node
                while parents[current_node] != current_node:
                    reconstructed_path.append(current_node)
                    current_node = parents[current_node]
                reconstructed_path.append(start)
                reconstructed_path.reverse()
                print(f'Path found: {reconstructed_path}')
                return reconstructed_path

            # Move the current node from the open list to the closed list
            open_lst.remove(current_node)
            closed_lst.add(current_node)

            # Explore the neighbors of the current node
            for neighbor_node, weight in self.get_neighbors(current_node):
                # If the neighbor has already been evaluated, skip it
                if neighbor_node in closed_lst:
                    continue

                # Calculate the tentative g-score for the neighbor
                tentative_g_score = g_scores[current_node] + weight

                # If the neighbor is not in the open list, or if the new path is better, update the neighbor's information
                if neighbor_node not in open_lst or tentative_g_score < g_scores.get(neighbor_node, float('inf')):
                    parents[neighbor_node] = current_node
                    g_scores[neighbor_node] = tentative_g_score
                    if neighbor_node not in open_lst:
                        open_lst.add(neighbor_node)

        # If the open list is empty and we have not reached the stop node, no path exists
        print('Path does not exist!')
        return None

# --- Main Execution ---

if __name__ == '__main__':
    # Create a graph object with the adjacency list loaded from Prolog
    graph1 = Graph(prolog_adjacency_list)
    # Get the source and destination nodes from the user
    source = input('Enter the Source name: ').lower()
    destination = input('Enter the Destination Name: ').lower()
    # Run the A* algorithm
    graph1.a_star_algorithm(source, destination)
