import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from generator import (
    generate_maze_dfs,
    generate_maze_prims,
    generate_maze_binary_tree
)

from solver import solve_bfs
from render import draw_maze_base


class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator + Solver")
        self.root.geometry("1000x600")

        self.grid = None
        self.width = None
        self.height = None
        self.steps = None
        self.path = None

        self.solve_index = 0
        self.solve_after_id = None
        
        self.anim_grid = None
        self.anim_index = 0
        self.gen_after_id = None
        self.speed = 10
        
        self.animate_generation = tk.BooleanVar(value=True)
        self.animate_solution = tk.BooleanVar(value=True)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure("TEntry", padding=8)
        style.configure("TCombobox", padding=6)
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Section.TLabel", font=("Arial", 13, "bold"))

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        control_frame = tk.Frame(self.main_frame, width=240)
        control_frame.grid(row=0, column=0, sticky="ns")
        control_frame.grid_propagate(False)

        inner = tk.Frame(control_frame, padx=20, pady=20)
        inner.pack(fill="both", expand=True)

        ttk.Label(inner, text="Maze Size", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(inner, text="Width").pack(anchor="w")
        self.width_entry = ttk.Entry(inner)
        self.width_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(inner, text="Height").pack(anchor="w")
        self.height_entry = ttk.Entry(inner)
        self.height_entry.pack(fill="x", pady=(0, 20))

        ttk.Label(inner, text="Algorithm", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(inner, text="Maze Generation").pack(anchor="w")
        self.algorithm = ttk.Combobox(
            inner,
            values=["DFS", "Prim's", "Binary Tree"],
            state="readonly",
            font=("Arial", 11),
            width=18
        )
        self.algorithm.current(0)
        self.algorithm["height"] = 5
        self.algorithm.pack(fill="x", pady=(0, 20))

        ttk.Label(inner, text="Actions", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        
        ttk.Checkbutton(
            inner,
            text="Animate Generation",
            variable=self.animate_generation
        ).pack(anchor="w", pady=(10, 0))

        ttk.Checkbutton(
            inner,
            text="Animate Solution",
            variable=self.animate_solution
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            inner,
            text="Generate Maze",
            command=self.generate_maze
        ).pack(fill="x", pady=(0, 10))

        ttk.Button(
            inner,
            text="Solve Maze",
            command=self.solve_maze
        ).pack(fill="x")

        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    def on_close(self):
        if self.solve_after_id:
            self.root.after_cancel(self.solve_after_id)

        if self.gen_after_id:
            self.root.after_cancel(self.gen_after_id)

        self.root.quit()
        self.root.destroy()

    def generate_maze(self):
        algo = self.algorithm.get()

        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            return

        if algo == "DFS":
            self.grid, self.width, self.height, self.steps = generate_maze_dfs(width, height)
        elif algo == "Prim's":
            self.grid, self.width, self.height, self.steps = generate_maze_prims(width, height)
        else:
            self.grid, self.width, self.height, self.steps = generate_maze_binary_tree(width, height)

        self.path = None

        if self.animate_generation.get():
            self.start_generation_animation()
        else:
            self.anim_grid = None
            self.render_grid()
        
    def create_empty_grid(self):
        new_grid = []

        for x in range(self.width):
            column = []
            for y in range(self.height):
                cell = self.grid[x][y].__class__(x, y)
                column.append(cell)
            new_grid.append(column)

        return new_grid
    
    def start_generation_animation(self):
        if self.gen_after_id:
            self.root.after_cancel(self.gen_after_id)

        self.anim_grid = self.create_empty_grid()
        self.anim_index = 0

        self.animate_generation_step()
        
    def animate_generation_step(self):
        if self.anim_index >= len(self.steps):
            # Finish -> switch to real grid
            self.anim_grid = None
            self.render_grid()
            return

        current, neighbor = self.steps[self.anim_index]

        c = self.anim_grid[current.x][current.y]
        n = self.anim_grid[neighbor.x][neighbor.y]

        dx = current.x - neighbor.x
        dy = current.y - neighbor.y

        if dx == 1:
            c.walls["left"] = False
            n.walls["right"] = False
        elif dx == -1:
            c.walls["right"] = False
            n.walls["left"] = False

        if dy == 1:
            c.walls["top"] = False
            n.walls["bottom"] = False
        elif dy == -1:
            c.walls["bottom"] = False
            n.walls["top"] = False

        self.anim_index += 1

        self.render_grid()

        self.gen_after_id = self.root.after(self.speed, self.animate_generation_step)

    def solve_maze(self):
        if not self.grid:
            return

        self.path = solve_bfs(self.grid, self.width, self.height)

        if not self.animate_solution.get():
            # Instant draw
            self.render_grid()

            for x, y in self.path:
                self.ax.add_patch(
                    plt.Rectangle(
                        (x, self.height - 1 - y),
                        1, 1,
                        color="red",
                        alpha=0.3
                    )
                )

            self.canvas.draw()
            return

        # Animate
        self.solve_index = 0

        if self.solve_after_id:
            self.root.after_cancel(self.solve_after_id)

        self.animate_solution_step()

    def animate_solution_step(self):
        if self.solve_index > len(self.path):
            return

        self.render_grid()

        for i in range(self.solve_index):
            x, y = self.path[i]
            self.ax.add_patch(
                plt.Rectangle(
                    (x, self.height - 1 - y),
                    1, 1,
                    color="red",
                    alpha=0.3
                )
            )

        self.canvas.draw()

        self.solve_index += 1
        self.solve_after_id = self.root.after(self.speed, self.animate_solution_step)

    def render_grid(self):
        self.ax.clear()

        grid_to_draw = self.anim_grid if self.anim_grid else self.grid

        if grid_to_draw:
            draw_maze_base(self.ax, grid_to_draw, self.width, self.height)

        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()