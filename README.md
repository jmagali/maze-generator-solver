# maze-generator-solver

<i>A procedural maze generator and solver with animated visualization using graph traversal algorithms.</i>

This project generates perfect mazes using Depth-First Search (DFS), Prim’s algorithm, and a Binary Tree algorithm, and solves them using Breadth-First Search (BFS), Depth-First Search (DFS), and A* search. Both processes are visualized step-by-step and can be exported as GIF animations.

<p align="center">
  <img src="exports\solving\solve_20260422_103304.gif" alt="Maze Solver Animation"/>
  <img src="exports\generation\gen_20260422_103225.gif" alt="Maze Generation Animation"/>
<img src="exports\images\Screenshot 2026-04-22 224310.png" alt="Application UI"/>
</p>

---

## Features

- Procedural generation of perfect mazes (no cycles, fully connected graph)
- Maze generation algorithms:
  - Depth-First Search (recursive backtracking)
  - Randomized Prim’s algorithm
  - Binary Tree algorithm (fast, biased structure)
- Pathfinding algorithms:
  - Breadth-First Search (optimal shortest path)
  - Depth-First Search (non-optimal exploration)
  - A* search (heuristic-guided shortest path)
- Real-time visualization of:
  - Maze generation process
  - Pathfinding exploration and solution path
- Animated rendering with exploration and solution overlays
- Export of generation and solving animations as GIFs
- Adjustable animation speed based on maze size
  
## Installation
### Requirements
- **Python 3.10 — 3.12** recommended
- **pip** installed

### 1.  Clone the repo
   ```sh
   git clone https://github.com/jmagali/maze-generator-solver.git
   cd maze-generator-solver
   ```

### 2.  Install the required Python libraries
   ```sh
   pip install -r requirements.txt # This installs the required libraries
   ```

### 3.  Run the program
   ```sh
   python main.py
   ```
