from render import draw_maze, animate_solution, animate_generation
from solver import solve
from generator import generate_maze_dfs, generate_maze_prims

while True:
    print("----------------------------------------------------------------------")
    generation = input("Enter 1/2 for DFS or Prims: ")
    visualize_generation = input("Visualize generation? (Y/N): ")
    mode = input("Enter 'D' for Draw Mode or 'S' for Solve Mode: ")
    print("----------------------------------------------------------------------")

    if generation in ["1", "2"] and mode.upper() in ["D", "S"]:
        break

# ---------------- GENERATION ----------------
if generation == "1":
    grid, width, height, steps = generate_maze_dfs()
else:
    grid, width, height, steps = generate_maze_prims()


# OPTIONAL: animate generation
if visualize_generation.upper() == "Y":
    from render import animate_generation
    animate_generation(grid, width, height, steps)

# ---------------- RENDERING ----------------
if mode.upper() == "D":
    draw_maze(grid, width, height)

else:
    path = solve(grid, width, height)
    animate_solution(grid, width, height, path)