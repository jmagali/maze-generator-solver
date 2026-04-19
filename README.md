# maze-generator-solver

<i>A procedural maze generation and solving visualizer using classic graph traversal algorithms.</i>

Generate randomized mazes using depth-first search (DFS) and solve them using breadth-first search (BFS), with animated visualization of the solution path.

<p align="center">  <img src="img/maze_solver.gif" alt="Maze Solver Animation"/> <img src="img/maze3.png" alt="Generated Maze"/> </p>

## Features
- Maze generation using Depth-First Search (DFS) with backtracking
- Guaranteed solvable "perfect" mazes (exactly one path between any two cells)
- Maze solving using Breadth-First Search (BFS) for shortest path
- Animated path visualization using Matplotlib
- Adaptive animation speed based on maze size

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
