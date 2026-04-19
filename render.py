import matplotlib.pyplot as plt

def draw_maze(grid, width, height):
    fig, ax = plt.subplots()
    
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            draw_y = height - 1 - y
            
            # If there is a wall in any direction, draw it
            if cell.walls["top"]:
                ax.plot([x, x+1], [draw_y+1, draw_y+1], "k")
            if cell.walls["bottom"]:
                ax.plot([x, x+1], [draw_y, draw_y], "k")
            if cell.walls["left"]:
                ax.plot([x, x], [draw_y, draw_y+1], "k")
            if cell.walls["right"]:
                ax.plot([x+1, x+1], [draw_y, draw_y+1], "k")
                
    ax.plot([0, 0], [height-1, height], color="green", linewidth=3)
    ax.plot([width, width], [0, 1], color="red", linewidth=3)
    
    ax.set_aspect("equal")
    ax.axis("off")
    
    plt.show()
    
