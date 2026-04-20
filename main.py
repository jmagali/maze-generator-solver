import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from generator import (
    generate_maze_dfs,
    generate_maze_prims,
    generate_maze_binary_tree
)

from solver import solve
from render import draw_maze_base

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze-Generator-Solver")
        self.root.geometry("1000x600")

        self.grid = None
        self.width = None
        self.height = None
        self.steps = None
        self.path = None

        self.anim_index = 0
        self.solve_index = 0

        self.gen_after_id = None
        self.solve_after_id = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=0)  # controls
        self.main_frame.columnconfigure(1, weight=1)  # canvas
        self.main_frame.rowconfigure(0, weight=1)

        control_frame = tk.Frame(self.main_frame, width=400, padx=15, pady=15)
        control_frame.grid(row=0, column=0, sticky="ns")
        control_frame.grid_propagate(False)

        self.algorithm = ttk.Combobox(
            control_frame,
            values=["DFS", "Prim's", "Binary Tree"],
            state="readonly"
        )
        self.algorithm.current(0)
        self.algorithm.pack(pady=10, fill="x")

        tk.Label(control_frame, text="Width").pack()
        self.width_entry = tk.Entry(control_frame)
        self.width_entry.pack(fill="x", padx=5)

        tk.Label(control_frame, text="Height").pack()
        self.height_entry = tk.Entry(control_frame)
        self.height_entry.pack(fill="x", padx=5)

        tk.Button(
            control_frame,
            text="Generate Maze",
            command=self.generate_maze
        ).pack(pady=10, fill="x")

        tk.Button(
            control_frame,
            text="Solve Maze",
            command=self.solve_maze
        ).pack(pady=5, fill="x")

        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    def on_close(self):
        if self.gen_after_id:
            self.root.after_cancel(self.gen_after_id)

        if self.solve_after_id:
            self.root.after_cancel(self.solve_after_id)

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
        self.render_grid()

    def solve_maze(self):
        if not self.grid:
            return

        self.path = solve(self.grid, self.width, self.height)
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
        self.solve_after_id = self.root.after(20, self.animate_solution_step)

    def render_grid(self):
        self.ax.clear()

        if self.grid:
            draw_maze_base(self.ax, self.grid, self.width, self.height)

        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()