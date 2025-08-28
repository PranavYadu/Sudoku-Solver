import tkinter as tk
from solver import solve_board, generate_random_puzzle

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        def close_on_esc(event=None):
            self.root.destroy()
        self.root.bind('<Escape>', close_on_esc)
        self.root = root
        self.root.title("Sudoku Solver")

        self.selected_cell = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.solved_cells = set()  # Add this line

        title = tk.Label(root, text="Sudoku Solver", font=("Helvetica", 20, "bold"))
        title.pack(pady=10)

        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)

        self.grid_frame = tk.Frame(main_frame, bg="black")
        self.grid_frame.grid(row=0, column=0, sticky="n")

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.grid_frame, width=2, font=("Helvetica", 22), justify='center', highlightthickness=0, relief="flat")
                entry.configure(insertontime=0)

                top = 2 if i % 3 == 0 else 1
                left = 2 if j % 3 == 0 else 1
                bottom = 2 if i == 8 else 0
                right = 2 if j == 8 else 0

                entry.grid(row=i, column=j, ipadx=10, ipady=10, padx=(left, right), pady=(top, bottom))

                entry.bind("<FocusIn>", lambda e, row=i, col=j: self.select_cell(row, col))
                entry.bind("<KeyPress>", lambda e: self.validate_input(e))
                entry.bind("<KeyRelease>", lambda e, row=i, col=j: self.limit_input(row, col))
                entry.bind("<Up>", lambda e, row=i, col=j: self.move_cursor(row-1, col))
                entry.bind("<Down>", lambda e, row=i, col=j: self.move_cursor(row+1, col))
                entry.bind("<Left>", lambda e, row=i, col=j: self.move_cursor(row, col-1))
                entry.bind("<Right>", lambda e, row=i, col=j: self.move_cursor(row, col+1))

                self.cells[i][j] = entry

        self.right_frame = tk.Frame(main_frame)
        self.right_frame.grid(row=0, column=1, padx=(30, 10), sticky="n")

        self.create_number_pad()
        self.root.bind("<Button-1>", self.handle_root_click)

    def create_number_pad(self):
        self.btn_font = ("Helvetica", 20, "bold")
        self.default_bg = "#eaeef1"
        self.hover_bg = "#dce1e6"
        self.text_color = "#5a7bc0"

        control_frame = tk.Frame(self.right_frame)
        control_frame.pack(pady=(98, 10))

        self.create_icon_button(control_frame, "⟲", self.reset_grid).grid(row=0, column=0, padx=5)
        self.create_icon_button(control_frame, "⌫", self.erase_cell).grid(row=0, column=1, padx=5)
        self.create_icon_button(control_frame, "🎲", self.fill_random).grid(row=0, column=2, padx=5)

        numbers_frame = tk.Frame(self.right_frame)
        numbers_frame.pack()

        for num in range(1, 10):
            row = (num - 1) // 3
            col = (num - 1) % 3
            btn = self.create_custom_button(
                numbers_frame, text=str(num),
                command=lambda n=num: self.insert_number(n)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

        solve_btn = self.create_custom_button(
            self.right_frame, text="Solve", width=14, height=2,
            bg="#5a7bc0", fg="white", hover_bg="#4b69ad",
            command=self.solve
        )
        solve_btn.pack(pady=(10, 0))

    def create_custom_button(self, parent, text, command=None, width=4, height=2,
                             bg=None, fg=None, hover_bg=None):
        bg = bg or self.default_bg
        fg = fg or self.text_color
        hover_bg = hover_bg or self.hover_bg

        btn = tk.Button(parent, text=text,
                        font=self.btn_font, width=width, height=height,
                        bg=bg, fg=fg, bd=0, relief="flat", activebackground=bg,
                        activeforeground=fg, highlightthickness=0,
                        command=command)

        def on_enter(e): btn.config(bg=hover_bg)
        def on_leave(e): btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def create_icon_button(self, parent, icon, command):
        return self.create_custom_button(parent, text=icon, command=command, width=3, height=1)

    def insert_number(self, num):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, str(num))
            # Remove from solved_cells if user edits
            self.solved_cells.discard((row, col))
            self.highlight_conflicts()

    def erase_cell(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].delete(0, tk.END)
            # Remove from solved_cells if user erases
            self.solved_cells.discard((row, col))
            self.highlight_conflicts()

    def reset_grid(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
        self.reset_focus()

    def fill_random(self):
        puzzle = generate_random_puzzle(given=30)
        self.solved_cells.clear()  # Clear solved cells so all numbers are black
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if puzzle[i][j] != 0:
                    self.cells[i][j].insert(0, str(puzzle[i][j]))
        self.reset_focus()

    def solve(self):
        original_values = [[self.cells[i][j].get() for j in range(9)] for i in range(9)]
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)

        self.solved_cells.clear()  # Clear previous solved cells

        if solve_board(board):
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(board[i][j]))
                    if original_values[i][j] == '':
                        self.solved_cells.add((i, j))  # Track solved cell
            self.reset_focus()
        else:
            print("No solution exists.")

    def select_cell(self, row, col):
        self.selected_cell = (row, col)
        self.highlight_conflicts()

    def move_cursor(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            self.select_cell(row, col)

    def validate_input(self, event):
        # Only allow single digit, and always replace cell with new digit
        if event.char in "123456789":
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].insert(0, event.char)
                self.solved_cells.discard((row, col))
                self.highlight_conflicts()
            return "break"
        elif event.keysym in ("BackSpace", "Delete", "Tab"):
            return None
        else:
            return "break"

    def limit_input(self, row, col):
        # No need to fix cell here, handled in validate_input
        value = self.cells[row][col].get()
        if len(value) > 1:
            self.cells[row][col].delete(1, tk.END)
        self.solved_cells.discard((row, col))
        self.highlight_conflicts()

    def highlight_conflicts(self):
        for i in range(9):
            for j in range(9):
                # Color solved cells blue, others black
                if (i, j) in getattr(self, 'solved_cells', set()):
                    self.cells[i][j].config(bg="white", fg="#5a7bc0")
                else:
                    self.cells[i][j].config(bg="white", fg="black")

        if self.selected_cell:
            row, col = self.selected_cell

            for i in range(9):
                self.cells[row][i].config(bg="#e0f0ff")
                self.cells[i][col].config(bg="#e0f0ff")

            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    self.cells[i][j].config(bg="#e0f0ff")

            self.cells[row][col].config(bg="#a5d8ff")
            self.cells[row][col].focus_set()

        for i in range(9):
            for j in range(9):
                val = self.cells[i][j].get()
                if val:
                    for k in range(9):
                        if k != j and self.cells[i][k].get() == val:
                            self.cells[i][j].config(bg="#fddede", fg="red")
                    for k in range(9):
                        if k != i and self.cells[k][j].get() == val:
                            self.cells[i][j].config(bg="#fddede", fg="red")
                    box_row = (i // 3) * 3
                    box_col = (j // 3) * 3
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if (r != i or c != j) and self.cells[r][c].get() == val:
                                self.cells[i][j].config(bg="#fddede", fg="red")

        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].config(bg="#a5d8ff")

    def reset_focus(self):
        self.selected_cell = None
        self.highlight_conflicts()
        self.root.focus_set()

    def handle_root_click(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            return
        if isinstance(widget, tk.Button):
            if widget['text'] in [str(i) for i in range(1, 10)] + ["⌫"]:
                return
        self.reset_focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
