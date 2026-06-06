import pytholog as pl
from collections import deque
pro_kb = pl.KnowledgeBase("Project")
D1 = {}
D2 = {}
pro_kb([
    "hs(a,366)",
    "hs(b,0)",
    "hs(c,160)",
    "hs(d,242)",
    "hs(e,161)",
    "hs(f,178)",
    "hs(g,77)",
    "hs(h,151)",
    "hs(i,226)",
    "hs(l,244)",
    "hs(m,241)",
    "hs(n,234)",
    "hs(o,380)",
    "hs(p,98)",
    "hs(r,193)",
    "hs(s,253)",
    "hs(t,329)",
    "hs(u,80)",
    "hs(v,199)",
    "hs(z,374)",
    "edges(a,z,75)",
    "edges(a,s,140)",
    "edges(a,t,118)",
    "edges(b,f,211)",
    "edges(b,p,101)",
    "edges(b,g,90)",
    "edges(b,u,85)",
    "edges(c,d,120)",
    "edges(c,r,146)",
    "edges(c,p,138)",
    "edges(d,m,75)",
    "edges(d,c,120)",
    "edges(e,h,86)",
    "edges(f,s,99)",
    "edges(f,b,211)",
    "edges(g,b,90)",
    "edges(h,e,86)",
    "edges(h,u,98)",
    "edges(i,n,87)",
    "edges(i,v,92)",
    "edges(l,m,70)",
    "edges(l,t,111)",
    "edges(m,l,70)",
    "edges(m,d,75)",
    "edges(n,i,87)",
    "edges(o,z,71)",
    "edges(o,s,151)",
    "edges(p,b,101)",
    "edges(p,c,138)",
    "edges(p,r,97)",
    "edges(r,s,80)",
    "edges(r,p,97)",
    "edges(r,c,146)",
    "edges(s,f,99)",
    "edges(s,r,80)",
    "edges(s,o,151)",
    "edges(s,a,140)",
    "edges(t,l,111)",
    "edges(t,a,118)",
    "edges(u,h,98)",
    "edges(u,v,142)",
    "edges(u,b,85)",
    "edges(l,t,111)",
    "edges(v,i,92)",
    "edges(v,u,142)",
    "edges(z,o,71)",
    "edges(z,a,75)",
])
A1 = len(pro_kb.query(pl.Expr("edges(X,Y,Z)")))
A2 = len(pro_kb.query(pl.Expr("hs(X,Y)")))
for i in range(A1):
    y = pro_kb.query(pl.Expr("edges(X,Y,Z)"))[i]
    Y = y.values()
    Y = list(Y)
    J1 = Y[0]
    if J1 in D1:
        Y.remove(J1)
        Y[1] = int(Y[1])
        Y = tuple(Y)
        D1[J1].append(Y)
    else:
        Y.remove(J1)
        Y[1] = int(Y[1])
        D1[J1] = [tuple(Y)]
    if i < A2:
        Z = pro_kb.query(pl.Expr("hs(X,Y)"))[i]
        Z1 = Z.values()
        Z1 = list(Z1)
        J2 = Z1[0]
        Z1.remove(J2)
        D2[J2] = int(Z1[0])
#print(D1)
#print(D2)
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    def h(self, n):
        return D2[n]

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
graph1 = Graph(D1)
source=input('Enter the Source name:').lower()
destination=input('Enter the Desitination Name:').lower()
graph1.a_star_algorithm(source,destination)

