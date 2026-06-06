"""
A_Star_Python.py
===============
A* pathfinding on the Romania road map – pure Python, no external
dependencies.  Great starting point for students who want to:
  • Understand A* step-by-step
  • Add new cities / roads (just edit the dicts below)
  • Compare different heuristics

City code → full name quick reference
--------------------------------------
a=Arad      b=Bucharest   c=Craiova   d=Dobreta    e=Eforie
f=Fagaras   g=Giurgiu     h=Hirsova   i=Iasi        l=Lugoj
m=Mehadia   n=Neamt       o=Oradea    p=Pitesti    r=Rimnicu Vilcea
s=Sibiu     t=Timisoara   u=Urziceni  v=Vaslui      z=Zerind
"""

# ════════════════════════════════════════════════════════════════════════════
#  DATA  –  edit this section to add your own cities and roads
# ════════════════════════════════════════════════════════════════════════════

# City codes mapped to their full names (for pretty output).
CITY_NAMES: dict[str, str] = {
    "a": "Arad",          "b": "Bucharest",   "c": "Craiova",
    "d": "Dobreta",       "e": "Eforie",      "f": "Fagaras",
    "g": "Giurgiu",       "h": "Hirsova",     "i": "Iasi",
    "l": "Lugoj",         "m": "Mehadia",     "n": "Neamt",
    "o": "Oradea",        "p": "Pitesti",     "r": "Rimnicu Vilcea",
    "s": "Sibiu",         "t": "Timisoara",   "u": "Urziceni",
    "v": "Vaslui",        "z": "Zerind",
}

# ── Heuristic values ──────────────────────────────────────────────────────
# h(n) = straight-line (Euclidean) distance from city n to Bucharest.
# A heuristic must be *admissible*: it must NEVER overestimate the true
# remaining cost.  Straight-line distance satisfies this for road maps.
#
# ➕ To add a city: add a line   "x": <distance_to_bucharest>
HEURISTIC: dict[str, int] = {
    "a": 366,   # Arad
    "b":   0,   # Bucharest  ← goal (h=0 because we're already there)
    "c": 160,   # Craiova
    "d": 242,   # Dobreta
    "e": 161,   # Eforie
    "f": 178,   # Fagaras
    "g":  77,   # Giurgiu
    "h": 151,   # Hirsova
    "i": 226,   # Iasi
    "l": 244,   # Lugoj
    "m": 241,   # Mehadia
    "n": 234,   # Neamt
    "o": 380,   # Oradea
    "p":  98,   # Pitesti
    "r": 193,   # Rimnicu Vilcea
    "s": 253,   # Sibiu
    "t": 329,   # Timisoara
    "u":  80,   # Urziceni
    "v": 199,   # Vaslui
    "z": 374,   # Zerind
}

# ── Adjacency list ────────────────────────────────────────────────────────
# Each city maps to a list of (neighbor_code, road_distance_km) tuples.
# The graph is UNDIRECTED: every road appears in both directions.
#
# ➕ To add a road between city "x" and city "y" with cost 50 km:
#     "x": [..., ("y", 50)],
#     "y": [..., ("x", 50)],
ROADS: dict[str, list[tuple[str, int]]] = {
    "a": [("z", 75),  ("s", 140), ("t", 118)],
    "b": [("f", 211), ("p", 101), ("g",  90), ("u", 85)],
    "c": [("d", 120), ("r", 146), ("p", 138)],
    "d": [("m",  75), ("c", 120)],
    "e": [("h",  86)],
    "f": [("s",  99), ("b", 211)],
    "g": [("b",  90)],
    "h": [("e",  86), ("u",  98)],
    "i": [("n",  87), ("v",  92)],
    "l": [("m",  70), ("t", 111)],
    "m": [("l",  70), ("d",  75)],
    "n": [("i",  87)],
    "o": [("z",  71), ("s", 151)],
    "p": [("b", 101), ("c", 138), ("r",  97)],
    "r": [("s",  80), ("p",  97), ("c", 146)],
    "s": [("f",  99), ("r",  80), ("o", 151), ("a", 140)],
    "t": [("l", 111), ("a", 118)],
    "u": [("h",  98), ("v", 142), ("b",  85)],
    "v": [("i",  92), ("u", 142)],
    "z": [("o",  71), ("a",  75)],
}


# ════════════════════════════════════════════════════════════════════════════
#  GRAPH CLASS  –  holds data + A* logic
# ════════════════════════════════════════════════════════════════════════════

class Graph:
    """
    A weighted undirected graph that can run the A* search algorithm.

    Attributes
    ----------
    roads      : adjacency list  { city: [(neighbor, cost), ...] }
    heuristic  : h-values        { city: estimated_cost_to_goal }
    city_names : display names   { code: full_name }
    """

    def __init__(
        self,
        roads: dict[str, list[tuple[str, int]]],
        heuristic: dict[str, int],
        city_names: dict[str, str] | None = None,
    ) -> None:
        self.roads      = roads
        self.heuristic  = heuristic
        self.city_names = city_names or {}

    # ── convenience helpers ──────────────────────────────────────────────────

    def neighbors(self, city: str) -> list[tuple[str, int]]:
        """Return all (neighbor, road_cost) pairs for *city*."""
        return self.roads.get(city, [])

    def h(self, city: str) -> float:
        """
        Heuristic h(n): straight-line distance to the goal.
        Returns ∞ for unknown cities so they are never preferred.
        """
        return self.heuristic.get(city, float("inf"))

    def name(self, code: str) -> str:
        """Return the full city name for a code, or the code itself."""
        return self.city_names.get(code, code.upper())

    # ── A* ───────────────────────────────────────────────────────────────────

    def a_star(self, start: str, goal: str, verbose: bool = False) -> list[str] | None:
        """
        Find the shortest path from *start* to *goal* with A*.

        Parameters
        ----------
        start   : source city code
        goal    : destination city code
        verbose : if True, print each expansion step (great for learning!)

        Returns
        -------
        List of city codes forming the optimal path, or None if unreachable.

        How A* works (plain English)
        -----------------------------
        We maintain a "frontier" (open_set) of cities we've discovered
        but not yet fully explored.  Each city n tracks two scores:

          g(n)  – the ACTUAL cost of the best path found so far from
                  start to n.
          h(n)  – a HEURISTIC ESTIMATE of the remaining cost from n to
                  the goal (here: straight-line distance).
          f(n)  = g(n) + h(n)  – estimated total cost through n.

        We always expand the frontier city with the lowest f-score.
        Because h(n) never overestimates, the first time we reach the
        goal we are guaranteed to have found the optimal path.
        """

        # ── Validate inputs ──────────────────────────────────────────────────
        if start not in self.roads and start not in self.heuristic:
            print(f"[ERROR] '{start}' is not a known city code.")
            return None
        if goal not in self.heuristic:
            print(f"[ERROR] '{goal}' is not a known city code.")
            return None

        # ── Initialise data structures ───────────────────────────────────────
        open_set: set[str]     = {start}   # cities to explore
        closed_set: set[str]   = set()     # cities already explored

        # g[city] = cheapest known path cost from start to city
        g: dict[str, float] = {start: 0}

        # parent[city] = the city we came from on the best path to city
        # (start points to itself – used as a sentinel when reconstructing)
        parent: dict[str, str] = {start: start}

        if verbose:
            print(f"\n[A*] Searching  {self.name(start)} → {self.name(goal)}")
            print("-" * 44)

        # ── Main loop ────────────────────────────────────────────────────────
        while open_set:

            # Choose the open city with the lowest f = g + h
            current = min(open_set, key=lambda n: g[n] + self.h(n))

            if verbose:
                f_scores = {n: g[n] + self.h(n) for n in open_set}
                print(
                    f"  Expanding : {self.name(current):20s}  "
                    f"g={g[current]:>4}  h={self.h(current):>4}  "
                    f"f={g[current]+self.h(current):>4}"
                )

            # ── Goal check ───────────────────────────────────────────────────
            if current == goal:
                # Reconstruct path by following parent pointers back to start
                path: list[str] = []
                node = current
                while parent[node] != node:
                    path.append(node)
                    node = parent[node]
                path.append(start)
                path.reverse()
                return path

            # ── Move to closed set ───────────────────────────────────────────
            open_set.discard(current)
            closed_set.add(current)

            # ── Explore neighbours ───────────────────────────────────────────
            for neighbor, road_cost in self.neighbors(current):

                if neighbor in closed_set:
                    continue   # already fully explored – skip

                tentative_g = g[current] + road_cost

                # If this path to neighbor is better than any known path:
                if tentative_g < g.get(neighbor, float("inf")):
                    g[neighbor]      = tentative_g
                    parent[neighbor] = current
                    open_set.add(neighbor)   # add or re-add to frontier

        return None   # open_set exhausted – goal unreachable


# ════════════════════════════════════════════════════════════════════════════
#  HELPER – compute total path cost
# ════════════════════════════════════════════════════════════════════════════

def path_cost(graph: Graph, path: list[str]) -> int:
    """Sum up road costs along *path*."""
    total = 0
    for i in range(len(path) - 1):
        for nbr, cost in graph.neighbors(path[i]):
            if nbr == path[i + 1]:
                total += cost
                break
    return total


# ════════════════════════════════════════════════════════════════════════════
#  CLI  –  interactive console interface
# ════════════════════════════════════════════════════════════════════════════

def print_city_table(city_names: dict[str, str]) -> None:
    """Pretty-print a two-column table of available city codes."""
    items = sorted(city_names.items())
    print("\n  Available cities")
    print("  ┌──────┬─────────────────────┐")
    for i in range(0, len(items), 2):
        code1, name1 = items[i]
        if i + 1 < len(items):
            code2, name2 = items[i + 1]
            print(f"  │  {code1}   │ {name1:<20s}│  {code2}   │ {name2:<20s}│")
        else:
            print(f"  │  {code1}   │ {name1:<20s}│      │                     │")
    print("  └──────┴─────────────────────┘\n")


def main() -> None:
    graph = Graph(ROADS, HEURISTIC, CITY_NAMES)

    print("=" * 52)
    print("   A* Pathfinder  –  Romania Road Map (pure Python)")
    print("=" * 52)
    print_city_table(CITY_NAMES)

    source = input("Enter source city code      : ").strip().lower()
    dest   = input("Enter destination city code : ").strip().lower()

    show_steps = input("Show step-by-step expansion? [y/N]: ").strip().lower() == "y"

    path = graph.a_star(source, dest, verbose=show_steps)

    print()
    if path:
        full_names = " → ".join(graph.name(c) for c in path)
        codes      = " → ".join(path)
        cost       = path_cost(graph, path)
        print(f"✔  Path   : {full_names}")
        print(f"   Codes  : {codes}")
        print(f"   Cost   : {cost} km\n")
    else:
        print(f"✘  No path exists between '{source}' and '{dest}'.\n")


if __name__ == "__main__":
    main()