import tkinter as tk
from tkinter import ttk, messagebox # Modern widgect styling (better than standard tkinter)
import platform
import numpy as np

import os
import imageio.v2 as imageio
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Embeds matplotlib plots in tkinter windows
import matplotlib.backends.backend_tkagg as tkagg

from generator import (
    generate_maze_dfs,
    generate_maze_prims,
    generate_maze_binary_tree
)

from solver import (
    solve_bfs,
    solve_dfs,
    solve_a_star
)

from render import draw_maze_base

import math

# GUI logic for the entire application
class MazeApp:
    def __init__(self, root):
        # Set-up the window (root), title, window size
        self.root = root
        self.root.title("Maze Generator + Solver")
        
        if platform.system() == "Windows":
            root.state('zoomed')
        else:
            root.attributes('-zoomed', True)

        self.grid = None
        self.width = None
        self.height = None
        self.steps = None # List of wall removals for animation
        self.path = None # Solution coordincates
        self.solution_steps = []  # List of exploration/backtrack steps for solution animation

        self.solve_index = 0 # Current step within solution animation
        self.solve_after_id = None # Tkinter timer ID; allows for solution animation cancellation
        
        self.anim_grid = None # Grid being animated during generation
        self.anim_index = 0 # Step within generation animation
        self.gen_after_id = None
        self.speed = 10 # Animation delay (ms)
        self.wall_lines = None
        
        # Saving booleans
        self.save_generation = tk.BooleanVar(value=False)
        self.save_solving = tk.BooleanVar(value=False)
        self.save_maze = tk.BooleanVar(value=False)
        self.save_solution = tk.BooleanVar(value=False)
        
        # Track whether generation and solutions should be animated
        self.animate_generation = tk.BooleanVar(value=True)
        self.animate_solution = tk.BooleanVar(value=True)
        
        self.themes = {
            "light": {
                "bg": "#f5f5f5",
                "panel": "#ffffff",
                "text": "#000000",
                "actions_text": "#000000",
                "accent": "#4a90e2",
                "maze_bg": "#ffffff",
                "wall": "#000000",
                "path": "red"
            },
            "dark": {
                "bg": "#444444",
                "panel": "#2b2b2b",
                "actions_text": "#000000",
                "text": "#ffffff",
                "accent": "#6aa9ff",
                "maze_bg": "#1e1e1e",
                "wall": "#ffffff",
                "path": "#ff6b6b"
            }
        }

        # Current_theme is for rendering, dark_mode is for the checkbox UI
        self.current_theme = "light"
        self.dark_mode = tk.BooleanVar(value=False)

        # Terminate the program and cancel pending animation supon window deletion
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        style = ttk.Style() # STyle manages for ttk widgets
        
        # Clam is a more modern theme
        # Some OS cannot use theme; hence, encase in a try/except
        try:
            style.theme_use("clam")
        except:
            pass

        # Configure properties for the used widgets
        style.configure("TEntry", padding=8)
        style.configure("TCombobox", padding=6)
        style.configure("TButton", font=("Arial", 11), padding=6)
        style.configure("Section.TLabel", font=("Arial", 13, "bold")) # Custom class for section headers

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True) # Expands to fill root window

        # Left column remains fixed (control panel)
        self.main_frame.columnconfigure(0, weight=0)
        
        # Right column expands into extra space (maze display)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Create fixed control frame within the left column of the main frame
        control_frame = tk.Frame(self.main_frame, width=240)
        control_frame.grid(row=0, column=0, sticky="ns")
        control_frame.grid_propagate(False) # Prevent frame from shrinking to fit children

        # Adds 'breayjomg room' around controls
        inner = tk.Frame(control_frame, padx=20, pady=20)
        inner.pack(fill="both", expand=True)

        # Maze size sections
        # Ttk instead of standard tkinter for modern widgets that match clam
        ttk.Label(inner, text="Maze Size", style="Section.TLabel").pack(anchor="w", pady=(0, 5))

        # Entries allow user to type in values
        ttk.Label(inner, text="Width").pack(anchor="w")
        self.width_entry = ttk.Entry(inner)
        self.width_entry.pack(fill="x", pady=(0, 10))
        self.width_entry.bind("<Key>", lambda event: self.remove_error_styling(event, self.width_entry))

        ttk.Label(inner, text="Height").pack(anchor="w")
        self.height_entry = ttk.Entry(inner)
        self.height_entry.pack(fill="x", pady=(0, 20))
        self.height_entry.bind("<Key>", lambda event: self.remove_error_styling(event, self.height_entry))

        # Algorithm section
        ttk.Label(inner, text="Algorithm", style="Section.TLabel").pack(anchor="w", pady=(0, 5))

        # Dropdown menu to prevent manual typing inputs
        ttk.Label(inner, text="Maze Generation").pack(anchor="w")
        self.generation_algorithm = ttk.Combobox(
            inner,
            values=["DFS", "Prim's", "Binary Tree"],
            state="readonly", 
            font=("Arial", 11),
            width=18
        )
        
        # Set initial combo option
        self.generation_algorithm.current(0)
        
        # TODO: This is meant to expand the height of the dropdown. I don't think it did anything.
        self.generation_algorithm["height"] = 5
        self.generation_algorithm.pack(fill="x", pady=(0, 20))
        
        ttk.Label(inner, text="Solving").pack(anchor="w")
        self.solving_algorithm = ttk.Combobox(
            inner,
            values=["BFS", "DFS", "A*"],
            state="readonly",
            font=("Arial", 11),
            width=18
        )
        self.solving_algorithm.current(0)
        
        # Increase the font size of dropdown menu
        self.root.option_add("*TCombobox*Listbox*Font", ("Arial", 11))
        
        # TODO: This is meant to expand the height of the dropdown. I don't think it did anything.
        self.solving_algorithm["height"] = 5
        self.solving_algorithm.pack(fill="x", pady=(0, 20))

        # Actions sections
        ttk.Label(inner, text="Actions", style="Section.TLabel").pack(anchor="w", pady=(0, 5))
        
        # Checkbox widget for simplicity
        ttk.Checkbutton(
            inner,
            text="Animate Generation",
            variable=self.animate_generation # links to variable
        ).pack(anchor="w", pady=(5, 0))

        ttk.Checkbutton(
            inner,
            text="Animate Solution",
            variable=self.animate_solution
        ).pack(anchor="w", pady=(0, 5))

        ttk.Button(
            inner,
            text="Generate Maze",
            command=self.generate_maze # Callback function when clicked
        ).pack(fill="x", pady=(0, 5))

        ttk.Button(
            inner,
            text="Solve Maze",
            command=self.solve_maze
        ).pack(fill="x", pady=(0, 5))
        
        ttk.Label(inner, text="Aesthetics", style="Section.TLabel").pack(anchor="w", pady=(10, 5))
        
        ttk.Checkbutton(
            inner,
            text="Dark Mode",
            variable=self.dark_mode, # Sync to variable for state persistence
            command=self.toggle_theme # Has a callback function because everythign must be redrawn instantly
        ).pack(anchor="w", pady=(5, 5))
        
        # Commands sections
        ttk.Label(inner, text="Commands", style="Section.TLabel").pack(anchor="w")
        
        # Generation command check buttons
        command_info = [("Save Generation Animation", self.save_generation),
                        ("Save Solving Animation", self.save_solving),
                        ("Save Maze", self.save_maze),
                        ("Save Solution", self.save_solution)]
        
        for text, variable in command_info:
            ttk.Checkbutton(
                inner,
                text=text,
                variable=variable
            ).pack(anchor="w", pady=(0, 5))

        # Matplotlib integration: creates the figure (window) and axes (drawing plot)
        self.fig, self.ax = plt.subplots()

        # Embed the matplot figure within the tkinter main frame
        # Save the canvas for updating during animation
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        
        # Embed within the right column, allowing it to stretch in all directions
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        
        # Apply the initial theme (light mode) before display
        self.apply_theme()
        
        # Enable zoom
        tkagg.NavigationToolbar2Tk(self.canvas, self.root)
        
        # Establish export destinations
        self.export_base = "exports"
        self.gen_folder = os.path.join(self.export_base, "generation")
        self.solve_folder = os.path.join(self.export_base, "solving")
        self.img_folder = os.path.join(self.export_base, "images")

        # Create folders if they don't exist
        for folder in [self.gen_folder, self.solve_folder, self.img_folder]:
            os.makedirs(folder, exist_ok=True)
            
        # Animation frames
        self.gen_frames = []
        self.solve_frames = []
        
    def apply_theme(self):
        # Retrieve the colour dictionary for the current theme
        theme = self.themes[self.current_theme]

        # Set the background colours for the roots and main frame
        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])

        # Passes through all widgets in the frame, colouring their backgrounds
        for widget in [self.main_frame]:
            widget.configure(bg=theme["bg"])

        # All levels must be coloured (nested widgets)
        # TODOD: This rebuilts the tree each time the theme is applied; try caching
        def recursive_color(widget):
            # Since some widgets do not have a background, errors must be handled
            try:
                widget.configure(bg=theme["bg"])
            except:
                pass
            
            # Walk along the widget tree
            for child in widget.winfo_children():
                recursive_color(child)

        recursive_color(self.main_frame)

        # ttk styling; ttk is handles differently than tkinter
        style = ttk.Style()
        style.configure("TFrame", background=theme["bg"])
        style.configure("TLabel", background=theme["bg"], foreground=theme["text"])
        style.configure("TButton", foreground=theme["actions_text"])
        style.configure("TCheckbutton", background=theme["bg"], foreground=theme["text"])
        style.configure("TEntry", background=theme["panel"], foreground=theme["text"], fieldbackground=theme["panel"])
        style.configure("TCombobox", background=theme["panel"], foreground=theme["actions_text"], fieldbackground=theme["panel"])
        style.configure("Error.TEntry", background="#ff4b4b", foreground="#ffffff", fieldbackground="#ff4b4b")

        # Matplotlib
        self.fig.patch.set_facecolor(theme["maze_bg"])
        self.ax.set_facecolor(theme["maze_bg"])

        # Redraw the whole maze with new colours
        self.render_grid()
        
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        
    def toggle_theme(self):
        # Checks the dark mode boolean and sets the theme accordinly
        self.current_theme = "dark" if self.dark_mode.get() else "light"
        
        # Triggers window redrawing with new theme
        self.apply_theme()

    def on_close(self):
        # Cancels pending animations by id
        # Animations can persists after window closing without cancellation
        if self.solve_after_id:
            self.root.after_cancel(self.solve_after_id)

        if self.gen_after_id:
            self.root.after_cancel(self.gen_after_id)

        # Stops the event loop and destroys the window
        self.root.quit()
        self.root.destroy()
        
    def validate_dimensions(self):
        error_messages = []
        width, height = float('inf'), float('inf')
        
        # Check if entries are valid digits
        try:
            width = int(self.width_entry.get())
        except ValueError:
            self.width_entry.configure(style="Error.TEntry")
            error_messages.append("Width must be a numeric integer.\n")
            
        try:
            height = int(self.height_entry.get())
        except ValueError:
            self.height_entry.configure(style="Error.TEntry")
            error_messages.append("Height must be a numeric integer.\n")
            
        if width < 1 and height < 1:
            self.width_entry.configure(style="Error.TEntry")
            error_messages.append("Maze must be at least 1x1.\n")
        elif width < 1:
            self.width_entry.configure(style="Error.TEntry")
            error_messages.append("Maze must be at least 1x1.\n")
        elif height < 1:
            self.height_entry.configure(style="Error.TEntry")
            error_messages.append("Maze must be at least 1x1.\n")
        
        # Remove error styling if there are no errors
        if not error_messages:
            self.width_entry.configure(style="TEntry")
            self.height_entry.configure(style="TEntry")
            return width, height, None
        
        return None, None, error_messages
    
    def generate_maze(self):
        # Retrieve the selected algorithm from the combobox
        algo = self.generation_algorithm.get()
        
        # Validate both entries at once
        width, height, errors = self.validate_dimensions()
        
        if errors:
            error_message = "".join(errors)
            messagebox.showerror("Input Error", error_message)
            return

        # Matches maze generation function to the respective combobox selection
        if algo == "DFS":
            self.grid, self.width, self.height, self.steps = generate_maze_dfs(width, height)
        elif algo == "Prim's":
            self.grid, self.width, self.height, self.steps = generate_maze_prims(width, height)
        else:
            self.grid, self.width, self.height, self.steps = generate_maze_binary_tree(width, height)

        # Clears the previous solution; different mazes need different solutions
        self.path = None

        # Animates the generation if selected by user
        if self.animate_generation.get():
            self.start_generation_animation()
        else:
            self.anim_grid = None
            self.render_grid()
            
        # Save the final image
        if self.save_maze.get():
            filename = datetime.now().strftime("maze_%Y%m%d_%H%M%S.png")
            path = os.path.join(self.img_folder, filename)
            self.fig.savefig(path)
            messagebox.showinfo("Export Completion", f"Saved maze image: {path}")
    
    # Create a fresh grid with all walls intact before removal in animation
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
        # Checks if an aniamtion is running; stop is before beginning a new one
        if self.gen_after_id:
            self.root.after_cancel(self.gen_after_id)

        # Create a clean maze for step-by-step wall removal
        self.anim_grid = self.create_empty_grid()
        
        # Reset the animation step (new animation starts at the beginning)
        self.anim_index = 0

        # Draw the empty grid once
        self.render_grid()
        
        self.animate_generation_step()
        
    def animate_generation_step(self, save=False):
        # If the animation has finished, render the complete grid and exit
        if self.anim_index >= len(self.steps):
            self.anim_grid = None
            self.render_grid()

            # Save the gif
            if self.save_generation.get() and self.gen_frames:
                filename = datetime.now().strftime("gen_%Y%m%d_%H%M%S.gif")
                path = os.path.join(self.gen_folder, filename)

                imageio.mimsave(path, self.gen_frames, duration=0.03)
                messagebox.showinfo("Export Completion", f"Saved generation GIF: {path}")


                self.gen_frames.clear()

            return

        # Retrieve the current wall removal from steps list
        current, neighbor = self.steps[self.anim_index]

        # Look up the cells in the animation grid (steps contains coords not Cells)
        c = self.anim_grid[current.x][current.y]
        n = self.anim_grid[neighbor.x][neighbor.y]

        # Calculate direction to determine which walls to remove
        dx = current.x - neighbor.x
        dy = current.y - neighbor.y

        # Carve the respective walls
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

        # Move to the next step and draw the maze with the current state
        self.anim_index += 1
        
        draw_y = self.height - 1 - current.y
        
        # Retrieve the colour dictionary for the current theme
        theme = self.themes[self.current_theme]
        
        # Remove wall visually by deleting the line
        if dx == 1:
            self.wall_lines[(current.x, current.y)]["left"].remove()
            self.wall_lines[(neighbor.x, neighbor.y)]["right"].remove()

        elif dx == -1:
            self.wall_lines[(current.x, current.y)]["right"].remove()
            self.wall_lines[(neighbor.x, neighbor.y)]["left"].remove()

        elif dy == 1:
            self.wall_lines[(current.x, current.y)]["top"].remove()
            self.wall_lines[(neighbor.x, neighbor.y)]["bottom"].remove()

        elif dy == -1:
            self.wall_lines[(current.x, current.y)]["bottom"].remove()
            self.wall_lines[(neighbor.x, neighbor.y)]["top"].remove()
            
        self.canvas.draw()
        
        # Save each frame
        if self.save_generation.get():
            image = np.asarray(self.canvas.buffer_rgba())
            self.gen_frames.append(image.copy())

        # Recall itself after the dealy (speed in ms)
        # ID must be stored for cancellation
        self.gen_after_id = self.root.after(self.speed, self.animate_generation_step)

    def solve_maze(self):
        # Retrieve the corresponding algorithm from the combobox
        algo = self.solving_algorithm.get()
        
        # If the maze has not been generated, cancel the solution
        if not self.grid:
            return

        result = None
        if algo == "BFS":
            result = solve_bfs(self.grid, self.width, self.height)
        elif algo == "DFS":
            result = solve_dfs(self.grid, self.width, self.height)
        elif algo == "A*":
            result = solve_a_star(self.grid, self.width, self.height)
        
        # Extract path and steps from the result
        self.path = result["path"] if result else None
        self.solution_steps = result["steps"] if result else []

        if not self.animate_solution.get():
            # Instant draw
            self.render_grid()

            # Draw explored cells (exploration steps) in a lighter color
            for step_type, x, y in self.solution_steps:
                if step_type == "explore":
                    self.ax.add_patch(
                        plt.Rectangle(
                            (x, self.height - 1 - y),
                            1, 1,
                            color=self.themes[self.current_theme]["path"],
                            alpha=0.15
                        )
                    )

            # Highlights each cell within the solution path in a darker color
            if self.path:
                for x, y in self.path:
                    # Adds a coloured rectandle within the plot
                    self.ax.add_patch(
                        plt.Rectangle(
                            (x, self.height - 1 - y),
                            1, 1,
                            color=self.themes[self.current_theme]["path"],
                            alpha=0.3
                        )
                    )

            # Immenediately updates the canvas
            self.canvas.draw()
            return

        # Animate
        self.solve_index = 0

        if self.solve_after_id:
            self.root.after_cancel(self.solve_after_id)

        self.animate_solution_step()
        
        # Save the gif
        if self.save_solution.get():
            filename = datetime.now().strftime("solution_%Y%m%d_%H%M%S.png")
            path = os.path.join(self.img_folder, filename)
            self.fig.savefig(path)
            messagebox.showinfo("Export Completion", f"Saved solution image: {path}")

        
    def remove_error_styling(self, key, entry):
        # Reset entry style on input:
        entry.configure(style="TEntry")

    def animate_solution_step(self):
        # Initialize on first call
        if self.solve_index == 0:
            self.render_grid()
        
        # Check if we have valid steps and path
        if not self.path or not self.solution_steps:
            if self.solve_index == 0:
                self.render_grid()
                self.canvas.draw()
            return
        
        total_steps = len(self.solution_steps) + len(self.path)
        
        # When the animation index is past the total steps, exit
        if self.solve_index >= total_steps:
            
            # Save the gif
            if self.save_solving.get() and self.solve_frames:
                filename = datetime.now().strftime("solve_%Y%m%d_%H%M%S.gif")
                path = os.path.join(self.solve_folder, filename)

                imageio.mimsave(path, self.solve_frames, duration=0.03)
                messagebox.showinfo("Export Completion", f"Saved solving GIF: {path}")


                self.solve_frames.clear()
                
            return
        
        # Draw exploration steps first (lighter color)
        if self.solve_index < len(self.solution_steps):
            step_type, x, y = self.solution_steps[self.solve_index]
            if step_type == "explore":
                self.ax.add_patch(
                    plt.Rectangle((x, self.height - y - 1), 
                    1, 1,
                    color=self.themes[self.current_theme]["path"],
                    alpha=0.15))
            elif step_type == "backtrack":
                # TODO: highlight backtracking differently if desired
                self.ax.add_patch(
                    plt.Rectangle((x, self.height - y - 1), 
                    1, 1,
                    color=self.themes[self.current_theme]["path"],
                    alpha=0.05))
        # Draw final solution path (darker color)
        else:
            path_index = self.solve_index - len(self.solution_steps)
            if path_index < len(self.path):
                x, y = self.path[path_index]
                self.ax.add_patch(
                    plt.Rectangle((x, self.height - y - 1), 
                    1, 1,
                    color=self.themes[self.current_theme]["path"],
                    alpha=0.3))

        self.canvas.draw()
        
        # Save each frame
        if self.save_solving.get():
            image = np.asarray(self.canvas.buffer_rgba())
            self.solve_frames.append(image.copy())

        # Increment the animation index and schedule the next frame
        self.solve_index += 1
        self.solve_after_id = self.root.after(self.speed, self.animate_solution_step)

    def render_grid(self):
        # Remove the previous drawings on the axes
        self.ax.clear()

        # Use the animation grid if animating or the final grid if not
        grid_to_draw = self.anim_grid if self.anim_grid else self.grid

        # Only draw if the grid exists
        if grid_to_draw:
            # Retrieve the colour theme
            theme = self.themes[self.current_theme]

            self.wall_lines = draw_maze_base(
                self.ax,
                grid_to_draw,
                self.width,
                self.height,
                wall_color=theme["wall"],
                entrance_color="green",
                exit_color="red",
                wall_width=2
            )

            self.ax.set_aspect("equal")
            self.ax.axis("off")
            
            # Refresh the canvas display (before it was only drawn on the axes)
            self.canvas.draw()

# If the file is not imported and executed direction, run the application
if __name__ == "__main__":
    # Create the root tkinter window
    root = tk.Tk()
    
    # Instantiate the application and populate the window
    app = MazeApp(root)
    
    # Begin the main event loop (listening for user inputs, etc)
    root.mainloop()
    