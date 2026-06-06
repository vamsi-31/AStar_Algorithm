# ✨ A* Search Algorithm: Prolog vs. Python Knowledge Base

## 💡 Introduction
This project demonstrates the A* search algorithm implemented in Python. The A* algorithm is a popular pathfinding algorithm that efficiently finds the shortest path between a start node and an end node in a graph. It achieves this by considering both the actual cost from the start (g-score) and an estimated heuristic cost to the end (h-score). This project showcases two approaches for managing the knowledge base (the graph data and heuristic values) and is designed for educational purposes to illustrate these concepts and data management techniques.

## 🗂️ Files in This Project
-   `knowledge_base.pl` 🧠: Contains the graph's edges, weights, and heuristic values in Prolog syntax.
-   `A_Star_Prolog.py` 🧐: Implements the A* algorithm, loading its knowledge base from `knowledge_base.pl`.
-   `A_Star_Python.py` 🐍: Implements the A* algorithm, with the knowledge base defined directly in Python.
-   `Map.png` 🗺️: A visual representation of the graph used by the algorithms.

## `knowledge_base.pl` 🧠
This file defines the graph structure and heuristic information using Prolog facts.
-   **`edges(Node1, Node2, Cost).`**: Represents a directed edge from `Node1` to `Node2` with a given `Cost`.
-   **`hs(Node, HeuristicValue).`**: Represents the heuristic value (estimated cost to goal) for a given `Node`.

This separation of the knowledge base allows for easy modification of the graph data without altering the Python code.

## `A_Star_Prolog.py` 🧐
This Python script implements the A* algorithm.
-   **Knowledge Base:** It dynamically loads the graph data and heuristics by consulting `knowledge_base.pl` at runtime using the `pytholog` library.
-   **Dependencies:**
    -   Python 3.x
    -   `pytholog` library (`pip install pytholog`)
    -   A Prolog interpreter (e.g., SWI-Prolog). Ensure it's installed and accessible in your system's PATH.
-   **How to Run:**
    ```bash
    python A_Star_Prolog.py
    ```
    The script will then prompt you to enter the source and destination nodes.

## `A_Star_Python.py` 🐍
This Python script also implements the A* algorithm.
-   **Knowledge Base:** The graph data (adjacency list) and heuristic values are defined directly within the script as Python dictionaries. This makes the script self-contained but requires code modification to change the graph.
-   **Dependencies:**
    -   Python 3.x
-   **How to Run:**
    ```bash
    python A_Star_Python.py
    ```
    The script will then prompt you to enter the source and destination nodes.

## `Map.png` 🗺️
This image file provides a visual representation of the graph used in both A* implementations. It helps in understanding the connections between nodes and the overall layout of the search space.

[Link to Map](./Map.png)

*(You can also embed the image directly if preferred, e.g., `![Map](./Map.png)`)*

## 🎓 Educational Insights
This project offers several learning opportunities:
-   **A* Algorithm:** Understand the core logic of the A* search algorithm, including concepts like open/closed lists, g-scores, h-scores, and f-scores.
-   **Knowledge Representation:** Compare two distinct methods of representing graph data:
    -   **Declarative (Prolog):** Data is stored as facts in a separate `.pl` file, promoting separation of data and logic. This is useful for larger, more complex knowledge bases that might be used by multiple applications or require frequent updates by non-programmers.
    -   **Programmatic (Python):** Data is embedded directly in the code using Python dictionaries. This is simpler for smaller graphs or when the graph is tightly coupled with the specific program.
-   **Prolog Integration:** See a practical example of how Python can interface with a Prolog knowledge base using libraries like `pytholog`.
-   **Code Reusability:** Notice how the core A* algorithm logic in the `Graph` class is largely the same in both Python scripts, with the main difference being how the graph data and heuristics are accessed.

By studying and comparing `A_Star_Prolog.py` and `A_Star_Python.py`, you can gain a deeper understanding of these different software design choices and their implications.
