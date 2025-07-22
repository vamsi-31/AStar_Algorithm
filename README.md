# ✨ A* Search Algorithm

## 💡 Introduction
This project provides a comprehensive demonstration of the A* search algorithm, a cornerstone of pathfinding and graph traversal in artificial intelligence. The A* algorithm is renowned for its ability to find the shortest path between two points in a graph by intelligently evaluating nodes based on two key metrics:

*   **g-score:** The actual cost of the path from the starting node to the current node.
*   **h-score:** A heuristic estimate of the cost from the current node to the goal node.

This project offers two distinct implementations of the A* algorithm, each highlighting a different approach to managing the underlying knowledge base (the graph's structure and heuristic data). This dual-implementation approach is designed for educational purposes, providing a clear comparison of data management techniques in software development.

## 🚀 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed on your system:

*   **Python 3.x:** This project is written in Python and requires a modern version of the interpreter.
*   **SWI-Prolog:** The `A_Star_Prolog.py` script relies on SWI-Prolog to manage its knowledge base. You can download it from the official [SWI-Prolog website](https://www.swi-prolog.org/download/stable).

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/A-Star-Search-Algorithm.git
   cd A-Star-Search-Algorithm
   ```

2. **Create a virtual environment:**
   It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   The `requirements.txt` file contains all the necessary Python packages for this project.
   ```bash
   pip install -r requirements.txt
   ```

## 🗂️ Files in This Project
-   `knowledge_base.pl` 🧠: A Prolog file containing the graph's structure, including edges, their associated costs, and the heuristic values for each node.
-   `A_Star_Prolog.py` 🧐: An implementation of the A* algorithm that dynamically loads its knowledge base from the `knowledge_base.pl` file using the `pyswip` library.
-   `A_Star_Python.py` 🐍: A self-contained implementation of the A* algorithm where the knowledge base is defined directly within the Python script.
-   `Map.png` 🗺️: A visual representation of the graph, providing a helpful reference for understanding the search space.
-   `requirements.txt` 📄: A file that lists the Python dependencies required to run the project.

## `knowledge_base.pl` 🧠
This file serves as the external knowledge base for the `A_Star_Prolog.py` script. It uses Prolog's declarative syntax to define the graph's properties:

-   **`edges(Node1, Node2, Cost).`**: This fact defines a directed edge from `Node1` to `Node2` with a specific `Cost`.
-   **`hs(Node, HeuristicValue).`**: This fact assigns a `HeuristicValue` to a given `Node`, which is used by the A* algorithm to estimate the distance to the goal.

By separating the knowledge base from the application logic, we can easily modify the graph's structure without making any changes to the Python code.

## `A_Star_Prolog.py` 🧐
This script showcases how to integrate Python with Prolog to create a powerful and flexible system.

-   **Knowledge Base:** The script uses the `pyswip` library to load and query the `knowledge_base.pl` file. This allows the A* algorithm to access the graph's data dynamically at runtime.
-   **Implementation Details:**
    1.  The script initializes a `Prolog` object from the `pyswip` library.
    2.  It then calls `prolog.consult("knowledge_base.pl")` to load the Prolog file.
    3.  The script queries for all `edges/3` and `hs/2` facts and stores them in Python dictionaries.
    4.  The A* algorithm is then executed using this dynamically loaded data.
-   **How to Run:**
    ```bash
    python A_Star_Prolog.py
    ```
    The script will prompt you to enter the source and destination nodes for the pathfinding operation.

## `A_Star_Python.py` 🐍
This script provides a more traditional, self-contained implementation of the A* algorithm.

-   **Knowledge Base:** The graph's adjacency list and heuristic values are defined directly within the script as Python dictionaries. This approach is simpler for smaller projects or when the graph data is static.
-   **How to Run:**
    ```bash
    python A_Star_Python.py
    ```
    The script will prompt you to enter the source and destination nodes.

## `Map.png` 🗺️
This image provides a visual representation of the graph used in both implementations of the A* algorithm. It can be a helpful tool for visualizing the search process and understanding the paths chosen by the algorithm.

![Map](./Map.png)

## 🎓 Educational Insights
This project offers a wealth of learning opportunities for students and developers interested in AI, algorithms, and software design:

-   **A* Algorithm:** Gain a deep understanding of the A* algorithm's core mechanics, including the roles of the open and closed lists, the calculation of g-scores and h-scores, and the process of path reconstruction.
-   **Knowledge Representation:** Explore the trade-offs between two different approaches to knowledge representation:
    -   **Declarative (Prolog):** Storing data in a separate, human-readable file promotes a clean separation of concerns and makes it easier to manage large and complex knowledge bases.
    -   **Programmatic (Python):** Embedding data directly in the code is a simpler and more straightforward approach for smaller or more tightly integrated systems.
-   **Python-Prolog Integration:** Discover how to bridge the gap between Python and Prolog using the `pyswip` library, enabling you to leverage the strengths of both languages in your applications.
-   **Code Reusability:** Observe how the core logic of the A* algorithm remains consistent across both implementations, with the primary difference being the method of data access. This highlights the importance of modular design and a clear separation of concerns.

By studying and experimenting with both `A_Star_Prolog.py` and `A_Star_Python.py`, you can develop a more nuanced understanding of these fundamental concepts and their practical applications.
