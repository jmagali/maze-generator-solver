import matplotlib.pyplot as plt
import matplotlib.animation as animation
from generator import remove_walls

def draw_maze(grid, width, height):
    # Figure: window; Axes: plot for drawing
    fig, ax = plt.subplots()
    
    draw_maze_base(ax, grid, width, height)
    
    ax.set_aspect("equal")
    ax.axis("off")
    
    # Displays the window until user closes it
    plt.show(block=True)

def draw_maze_base(
    ax,
    grid,
    width,
    height,
    wall_color="black",
    entrance_color="green",
    exit_color="red",
    wall_width=2
):
    wall_lines = {}
    
    # Loops through each cell in the grid
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            
            # Since the matplotlib origin is in the bottom-left and not top-left
            # y-values must be inverted. Maybe I can just use negative indices?
            draw_y = height - 1 - y

            # Draws the walls for each cell
            wall_lines[(x, y)] = {}

            if cell.walls["top"]:
                line, = ax.plot([x, x+1], [draw_y+1, draw_y+1], color=wall_color, lw=wall_width)
                wall_lines[(x, y)]["top"] = line

            if cell.walls["bottom"]:
                line, = ax.plot([x, x+1], [draw_y, draw_y], color=wall_color, lw=wall_width)
                wall_lines[(x, y)]["bottom"] = line

            if cell.walls["left"]:
                line, = ax.plot([x, x], [draw_y, draw_y+1], color=wall_color, lw=wall_width)
                wall_lines[(x, y)]["left"] = line

            if cell.walls["right"]:
                line, = ax.plot([x+1, x+1], [draw_y, draw_y+1], color=wall_color, lw=wall_width)
                wall_lines[(x, y)]["right"] = line

    # Entrance (top-left)
    ax.plot([0, 0], [height-1, height], color=entrance_color, linewidth=wall_width)

    # Exit (bottom-right)
    ax.plot([width, width], [0, 1], color=exit_color, linewidth=wall_width)
    
    return wall_lines