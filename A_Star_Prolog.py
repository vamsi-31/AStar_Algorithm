"""
A_Star_Prolog.py
===============
A* pathfinding using a Prolog knowledge base as the data source.

Requirements
------------
    pip install pyswip

pyswip is a Python wrapper around SWI-Prolog. You must have
SWI-Prolog installed on your system first:
  • Windows : https://www.swi-prolog.org/download/stable
  • Ubuntu  : sudo apt install swi-prolog
  • macOS   : brew install swi-prolog

After installing SWI-Prolog, install the Python wrapper:
    pip install pyswip

How it works
------------
1. Prolog loads knowledge_base.pl (cities + road costs + heuristics).
2. Python queries Prolog to build an adjacency list and heuristic dict.
3. The A* algorithm runs entirely in Python using those structures.

Why use Prolog at all?
----------------------
Keeping facts in a .pl file separates *data* from *logic*. You can
edit knowledge_base.pl to add cities/roads without touching the Python
algorithm code.
"""

# ── Standard library ────────────────────────────────────────────────────────
import sys

# ── Third-party ──────────────────────────────────────────────────────────────
try:
    from pyswip import Prolog
except ImportError:
    sys.exit(
        "\n[ERROR] pyswip is not installed.\n"
        "Run:  pip install pyswip\n"
        "Also make sure SWI-Prolog is installed: https://www.swi-prolog.org/\n"
    )


# ════════════════════════════════════════════════════════════════════════════
#  STEP 1 – Load the Prolog knowledge base
# ════════════════════════════════════════════════════════════════════════════

prolog = Prolog()

try:
    prolog.consult("knowledge_base.pl")
except Exception as exc:
    sys.exit(
        f"\n[ERROR] Could not load knowledge_base.pl.\n"
        f"Make sure the file is in the same folder as this script.\n"
        f"Details: {exc}\n"
    )


# ════════════════════════════════════════════════════════════════════════════
#  STEP 2 – Build Python data structures from Prolog facts
# ════════════════════════════════════════════════════════════════════════════

def load_graph_from_prolog() -> tuple[dict, dict]:
    """
    Query Prolog for all edges/3 and hs/2 facts, then return:
        adjacency_list  – { node: [(neighbor, cost), ...] }
        heuristic_values – { node: h_value }
    """
    adjacency_list: dict[str, list[tuple[str, int]]] = {}
    heuristic_values: dict[str, int] = {}

    # ── edges/3 ──────────────────────────────────────────────────────────────
    for fact in prolog.query("edges(X, Y, Z)"):
        src  = str(fact["X"])
        dest = str(fact["Y"])
        cost = int(fact["Z"])
        adjacency_list.setdefault(src, []).append((dest, cost))

    # ── hs/2 ─────────────────────────────────────────────────────────────────
    for fact in prolog.query("hs(X, Y)"):
        node = str(fact["X"])
        h    = int(fact["Y"])
        heuristic_values[node] = h

    return adjacency_list, heuristic_values


# ════════════════════════════════════════════════════════════════════════════
#  STEP 3 – A* Algorithm
# ════════════════════════════════════════════════════════════════════════════

class Graph:
    """
    Undirected weighted graph with an A* search method.

    Parameters
    ----------
    adj_list : dict
        { node: [(neighbor, cost), ...] }
    h_vals : dict
        { node: heuristic_value }
    """

    def __init__(self, adj_list: dict, h_vals: dict) -> None:
        self.adj_list = adj_list
        self.h_vals   = h_vals

    # ── helpers ──────────────────────────────────────────────────────────────

    def neighbors(self, node: str) -> list[tuple[str, int]]:
        """Return [(neighbor, cost), ...] for *node*."""
        return self.adj_list.get(node, [])

    def h(self, node: str) -> float:
        """Heuristic h(n): straight-line distance to goal."""
        return self.h_vals.get(node, float("inf"))

    # ── A* ───────────────────────────────────────────────────────────────────

    def a_star(self, start: str, goal: str) -> list[str] | None:
        """
        Find the lowest-cost path from *start* to *goal* using A*.

        Returns the path as a list of node names, or None if unreachable.

        A* overview
        -----------
        We maintain two sets:
          open_set   – nodes discovered but not yet fully explored.
          closed_set – nodes already fully explored.

        For each node we track:
          g[n] – exact cost from start to n found so far.
          f[n] = g[n] + h(n)  – estimated total cost through n.

        At every step we expand the node with the lowest f-score.
        """

        if start not in self.adj_list and start not in self.h_vals:
            print(f"[ERROR] Start node '{start}' not found in the graph.")
            return None
        if goal not in self.h_vals:
            print(f"[ERROR] Goal node '{goal}' not found in the graph.")
            return None

        open_set: set[str]    = {start}
        closed_set: set[str]  = set()

        g: dict[str, float]   = {start: 0}     # g-score  (actual cost)
        parent: dict[str, str] = {start: start} # for path reconstruction

        while open_set:
            # Pick the open node with the smallest f = g + h
            current = min(open_set, key=lambda n: g[n] + self.h(n))

            # ── Goal reached ─────────────────────────────────────────────────
            if current == goal:
                path: list[str] = []
                node = current
                while parent[node] != node:
                    path.append(node)
                    node = parent[node]
                path.append(start)
                path.reverse()
                return path

            # ── Expand current ───────────────────────────────────────────────
            open_set.discard(current)
            closed_set.add(current)

            for neighbor, cost in self.neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g = g[current] + cost

                if tentative_g < g.get(neighbor, float("inf")):
                    g[neighbor]      = tentative_g
                    parent[neighbor] = current
                    open_set.add(neighbor)

        return None   # No path found


# ════════════════════════════════════════════════════════════════════════════
#  STEP 4 – Interactive CLI
# ════════════════════════════════════════════════════════════════════════════

def print_city_list(adj_list: dict) -> None:
    """Print all known cities so the user knows what to type."""
    cities = sorted(adj_list.keys())
    print("\nAvailable cities:")
    print("  " + ", ".join(cities))
    print()


def main() -> None:
    adj_list, h_vals = load_graph_from_prolog()
    graph = Graph(adj_list, h_vals)

    print("=" * 50)
    print("   A* Pathfinder  –  Romania Road Map")
    print("   (data loaded from knowledge_base.pl)")
    print("=" * 50)
    print_city_list(adj_list)

    source = input("Enter source city (letter code): ").strip().lower()
    dest   = input("Enter destination city (letter code): ").strip().lower()

    path = graph.a_star(source, dest)

    if path:
        total_cost = 0
        for i in range(len(path) - 1):
            for nbr, cost in graph.neighbors(path[i]):
                if nbr == path[i + 1]:
                    total_cost += cost
                    break
        print(f"\n✔  Path found : {' → '.join(path)}")
        print(f"   Total cost : {total_cost} km\n")
    else:
        print(f"\n✘  No path exists between '{source}' and '{dest}'.\n")


if __name__ == "__main__":
    main()