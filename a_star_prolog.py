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
    y = edge_facts[i]
    Y = list(y.values()) # Extract values from the query result
    J1 = Y[0] # Source node
    # Convert cost to integer and create a tuple (DestinationNode, Cost)
    edge_data = (Y[1], int(Y[2]))
    if J1 in prolog_adjacency_list:
        prolog_adjacency_list[J1].append(edge_data)
    else:
        prolog_adjacency_list[J1] = [edge_data]

# Process heuristic facts to populate prolog_heuristic_values
for i in range(A2):
    Z = heuristic_facts[i]
    Z1 = list(Z.values()) # Extract values from the query result
    J2 = Z1[0] # Node
    prolog_heuristic_values[J2] = int(Z1[1]) # Heuristic value

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
        # In this open_lst is a lisy of nodes which have been visited, but who's
        # neighbours haven't all been always inspected, It starts off with the start
        # node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])

        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0

        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start

        while len(open_lst) > 0:
            n = None

            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        print('Path does not exist!')
        return None
graph1 = Graph(prolog_adjacency_list) # Use the renamed variable for instantiation
source=input('Enter the Source name:').lower()
destination=input('Enter the Desitination Name:').lower()
graph1.a_star_algorithm(source,destination)

