from render import draw_maze, animate_solution
from solver import solve
from generator import generate_maze_dfs, generate_maze_prims
        
while True:
    generation = input("Enter 1/2 for DFS or Prims: ")
    mode = input("Enter 1/2 for Draw Mode or Solve Mode: ")
    
    if mode in ["1", "2"] and generation in ["1", "2"]:
        break

if generation == "1":
    grid, width, height = generate_maze_dfs()
else:
    grid, width, height = generate_maze_prims()

if mode == "1":
    draw_maze(grid, width, height)
else:
    path = solve(grid, width, height)
    animate_solution(grid, width, height, path)
                
