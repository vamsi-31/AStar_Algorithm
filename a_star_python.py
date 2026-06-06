# No pytholog import needed as we are using Python native data structures.
# from collections import deque # deque is not used in the Graph class.

# Heuristic values for each node (equivalent to hs/2 facts in Prolog)
# h_scores[node] = heuristic_value
heuristic_values = {
    'a': 366, 'b': 0,   'c': 160, 'd': 242, 'e': 161,
    'f': 178, 'g': 77,  'h': 151, 'i': 226, 'l': 244,
    'm': 241, 'n': 234, 'o': 380, 'p': 98,  'r': 193,
    's': 253, 't': 329, 'u': 80,  'v': 199, 'z': 374
}

# Adjacency list representing the graph structure (equivalent to edges/3 facts in Prolog)
# graph_edges[node] = [(neighbor1, cost1), (neighbor2, cost2), ...]
adjacency_list = {
    'a': [('z', 75), ('s', 140), ('t', 118)],
    'b': [('f', 211), ('p', 101), ('g', 90), ('u', 85)],
    'c': [('d', 120), ('r', 146), ('p', 138)],
    'd': [('m', 75), ('c', 120)],
    'e': [('h', 86)],
    'f': [('s', 99), ('b', 211)],
    'g': [('b', 90)],
    'h': [('e', 86), ('u', 98)],
    'i': [('n', 87), ('v', 92)],
    'l': [('m', 70), ('t', 111)], # Corrected duplicate l,t edge from original data
    'm': [('l', 70), ('d', 75)],
    'n': [('i', 87)],
    'o': [('z', 71), ('s', 151)],
    'p': [('b', 101), ('c', 138), ('r', 97)],
    'r': [('s', 80), ('p', 97), ('c', 146)],
    's': [('f', 99), ('r', 80), ('o', 151), ('a', 140)],
    't': [('l', 111), ('a', 118)],
    'u': [('h', 98), ('v', 142), ('b', 85)],
    'v': [('i', 92), ('u', 142)],
    'z': [('o', 71), ('a', 75)]
}

class Graph:
    """
    Represents a graph and provides the A* search algorithm.
    """
    def __init__(self, adj_list, h_vals):
        """
        Initializes the graph.
        :param adj_list: The adjacency list of the graph.
        :param h_vals: A dictionary of heuristic values for each node.
        """
        self.adjac_lis = adj_list
        self.heuristic_values = h_vals

    def get_neighbors(self, v_node):
        """
        Gets the neighbors of a given node.
        :param v_node: The node to get neighbors for.
        :return: A list of (neighbor, cost) tuples.
        """
        return self.adjac_lis.get(v_node, []) # Return empty list if node not in adj_list to prevent KeyError

    def h(self, node_name):
        """
        Gets the heuristic value for a given node.
        :param node_name: The name of the node.
        :return: The heuristic value (integer).
        """
        return self.heuristic_values.get(node_name, float('inf')) # Return infinity if node has no heuristic

    def a_star_algorithm(self, start_node, stop_node):
        """
        Performs the A* search algorithm to find the shortest path from start_node to stop_node.
        :param start_node: The starting node.
        :param stop_node: The destination node.
        :return: A list representing the path from start_node to stop_node, or None if no path exists.
        """
        # open_lst: set of nodes which have been visited, but whose neighbors haven't all been inspected.
        # Starts with the start_node.
        open_lst = {start_node}
        # closed_lst: set of nodes which have been visited and whose neighbors have been inspected.
        closed_lst = set()

        # g_scores: present distances from start_node to all other nodes. Default is +infinity.
        g_scores = {start_node: 0}

        # parents: mapping of all nodes to their parent node in the path.
        parents = {start_node: start_node}

        while len(open_lst) > 0:
            current_node = None

            # Find a node in open_lst with the lowest value of f(n) = g(n) + h(n)
            for v_node in open_lst:
                if current_node is None or g_scores[v_node] + self.h(v_node) < g_scores[current_node] + self.h(current_node):
                    current_node = v_node

            if current_node is None:
                print('Path does not exist!')
                return None

            # If the current_node is the stop_node, reconstruct and return the path.
            if current_node == stop_node:
                reconst_path = []
                while parents[current_node] != current_node:
                    reconst_path.append(current_node)
                    current_node = parents[current_node]
                reconst_path.append(start_node)
                reconst_path.reverse()
                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # For all neighbors of the current_node:
            for (neighbor_node, weight) in self.get_neighbors(current_node):
                # If the neighbor is not in open_lst and not in closed_lst,
                # add it to open_lst and set current_node as its parent.
                if neighbor_node not in open_lst and neighbor_node not in closed_lst:
                    open_lst.add(neighbor_node)
                    parents[neighbor_node] = current_node
                    g_scores[neighbor_node] = g_scores[current_node] + weight
                # Otherwise, if it's quicker to first visit current_node, then neighbor_node:
                # update parent and g_scores data.
                # If neighbor_node was in closed_lst, move it to open_lst.
                else:
                    if g_scores.get(neighbor_node, float('inf')) > g_scores[current_node] + weight:
                        g_scores[neighbor_node] = g_scores[current_node] + weight
                        parents[neighbor_node] = current_node
                        if neighbor_node in closed_lst:
                            closed_lst.remove(neighbor_node)
                            open_lst.add(neighbor_node)

            # Remove current_node from open_lst and add it to closed_lst
            # because all its neighbors were inspected.
            open_lst.remove(current_node)
            closed_lst.add(current_node)

        print('Path does not exist!')
        return None

# --- Main execution part ---
if __name__ == '__main__':
    # Instantiate the graph with the Python-defined adjacency list and heuristic values
    graph = Graph(adjacency_list, heuristic_values)

    # Get user input for source and destination nodes
    source_node_input = input('Enter the Source name:').lower()
    destination_node_input = input('Enter the Destination Name:').lower()

    # Run the A* algorithm
    graph.a_star_algorithm(source_node_input, destination_node_input)
