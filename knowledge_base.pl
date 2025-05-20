% This file contains the knowledge base for the A* algorithm.
% It defines the heuristic values for each node and the edges between nodes with their respective costs.

% Heuristic values (hs) for each node
% hs(Node, HeuristicValue).
hs(a,366).
hs(b,0).
hs(c,160).
hs(d,242).
hs(e,161).
hs(f,178).
hs(g,77).
hs(h,151).
hs(i,226).
hs(l,244).
hs(m,241).
hs(n,234).
hs(o,380).
hs(p,98).
hs(r,193).
hs(s,253).
hs(t,329).
hs(u,80).
hs(v,199).
hs(z,374).

% Edges between nodes and their costs
% edges(SourceNode, DestinationNode, Cost).
edges(a,z,75).
edges(a,s,140).
edges(a,t,118).
edges(b,f,211).
edges(b,p,101).
edges(b,g,90).
edges(b,u,85).
edges(c,d,120).
edges(c,r,146).
edges(c,p,138).
edges(d,m,75).
edges(d,c,120).
edges(e,h,86).
edges(f,s,99).
edges(f,b,211).
edges(g,b,90).
edges(h,e,86).
edges(h,u,98).
edges(i,n,87).
edges(i,v,92).
edges(l,m,70).
edges(l,t,111).
edges(m,l,70).
edges(m,d,75).
edges(n,i,87).
edges(o,z,71).
edges(o,s,151).
edges(p,b,101).
edges(p,c,138).
edges(p,r,97).
edges(r,s,80).
edges(r,p,97).
edges(r,c,146).
edges(s,f,99).
edges(s,r,80).
edges(s,o,151).
edges(s,a,140).
edges(t,l,111).
edges(t,a,118).
edges(u,h,98).
edges(u,v,142).
edges(u,b,85).
edges(l,t,111).
edges(v,i,92).
edges(v,u,142).
edges(z,o,71).
edges(z,a,75).
