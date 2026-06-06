% ============================================================
%  knowledge_base.pl  –  Romania Road Map (A* Knowledge Base)
%  Source: Russell & Norvig, "Artificial Intelligence: A Modern
%          Approach" (the classic Romania problem).
%
%  HOW TO READ THIS FILE
%  ---------------------
%  hs(Node, H)          – straight-line distance from Node to
%                         Bucharest (our heuristic / h-value).
%  edges(From, To, Cost) – a road from city From to city To
%                         with distance Cost km.
%  All edges are stored in BOTH directions so the graph is
%  undirected (you can travel either way on every road).
%
%  HOW TO ADD YOUR OWN CITY
%  ------------------------
%  1. Add its heuristic:   hs(mycity, 123).
%  2. Add roads to/from it: edges(mycity, sibiu, 50).
%                           edges(sibiu, mycity, 50).
%  That's it – the Python A* code will pick it up automatically.
% ============================================================


% ------------------------------------------------------------
%  HEURISTIC VALUES  (straight-line distance to Bucharest)
%  Node abbreviations used in the code:
%    a=Arad   b=Bucharest  c=Craiova   d=Dobreta   e=Eforie
%    f=Fagaras  g=Giurgiu  h=Hirsova   i=Iasi      l=Lugoj
%    m=Mehadia  n=Neamt    o=Oradea    p=Pitesti   r=Rimnicu Vilcea
%    s=Sibiu    t=Timisoara u=Urziceni  v=Vaslui    z=Zerind
% ------------------------------------------------------------
hs(a, 366).   % Arad
hs(b,   0).   % Bucharest  ← goal node (h=0)
hs(c, 160).   % Craiova
hs(d, 242).   % Dobreta
hs(e, 161).   % Eforie
hs(f, 178).   % Fagaras
hs(g,  77).   % Giurgiu
hs(h, 151).   % Hirsova
hs(i, 226).   % Iasi
hs(l, 244).   % Lugoj
hs(m, 241).   % Mehadia
hs(n, 234).   % Neamt
hs(o, 380).   % Oradea
hs(p,  98).   % Pitesti
hs(r, 193).   % Rimnicu Vilcea
hs(s, 253).   % Sibiu
hs(t, 329).   % Timisoara
hs(u,  80).   % Urziceni
hs(v, 199).   % Vaslui
hs(z, 374).   % Zerind


% ------------------------------------------------------------
%  EDGES  edges(From, To, CostInKm)
%  Every road appears twice (A→B and B→A) for an undirected graph.
% ------------------------------------------------------------

% --- Arad (a) ---
edges(a, z, 75).    edges(z, a, 75).
edges(a, s, 140).   edges(s, a, 140).
edges(a, t, 118).   edges(t, a, 118).

% --- Zerind (z) ---
edges(z, o, 71).    edges(o, z, 71).

% --- Oradea (o) ---
edges(o, s, 151).   edges(s, o, 151).

% --- Sibiu (s) ---
edges(s, f, 99).    edges(f, s, 99).
edges(s, r, 80).    edges(r, s, 80).

% --- Timisoara (t) ---
edges(t, l, 111).   edges(l, t, 111).

% --- Lugoj (l) ---
edges(l, m, 70).    edges(m, l, 70).

% --- Mehadia (m) ---
edges(m, d, 75).    edges(d, m, 75).

% --- Dobreta (d) ---
edges(d, c, 120).   edges(c, d, 120).

% --- Craiova (c) ---
edges(c, r, 146).   edges(r, c, 146).
edges(c, p, 138).   edges(p, c, 138).

% --- Rimnicu Vilcea (r) ---
edges(r, p, 97).    edges(p, r, 97).

% --- Fagaras (f) ---
edges(f, b, 211).   edges(b, f, 211).

% --- Pitesti (p) ---
edges(p, b, 101).   edges(b, p, 101).

% --- Bucharest (b) ---
edges(b, g, 90).    edges(g, b, 90).
edges(b, u, 85).    edges(u, b, 85).

% --- Urziceni (u) ---
edges(u, h, 98).    edges(h, u, 98).
edges(u, v, 142).   edges(v, u, 142).

% --- Hirsova (h) ---
edges(h, e, 86).    edges(e, h, 86).

% --- Vaslui (v) ---
edges(v, i, 92).    edges(i, v, 92).

% --- Iasi (i) ---
edges(i, n, 87).    edges(n, i, 87).