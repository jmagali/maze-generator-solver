import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

def draw_maze_base(ax, grid, width, height):
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


def animate_solution(grid, width, height, path):
    fig, ax = plt.subplots()

    draw_maze_base(ax, grid, width, height)

    # highlight layer (this is the key part)
    highlights = []

    def update(i):
        # remove old highlight patches
        for h in highlights:
            h.remove()
        highlights.clear()

        # draw path up to i
        for (x, y) in path[:i]:
            rect = plt.Rectangle(
                (x, height - 1 - y),
                1,
                1,
                color="red",
                alpha=0.25
            )
            ax.add_patch(rect)
            highlights.append(rect)

        return highlights
    
    cells = width * height

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(path) + 1,
        interval=max(0, min(120, 1000 / cells)),
        blit=True,
        repeat=False
    )

    ax.set_aspect("equal")
    ax.axis("off")

    plt.show()
    
