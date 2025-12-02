import tkinter as tk
import tkinter.messagebox as messagebox
import copy
from solver import solve_board, is_valid


class SudokuGame:
    def __init__(self, root):
        self.root = root
        def close_on_esc(event=None):
            self.root.destroy()
        self.root.bind('<Escape>', close_on_esc)
        self.root.title("Sudoku Game")

        self.btn_font = ("Helvetica", 20, "bold")
        self.small_font = ("Helvetica", 12, "bold")
        self.default_bg = "#eaeef1"
        self.hover_bg = "#dce1e6"
        self.text_color = "#5a7bc0"
        self.muted_fg = "#7a8794"

        self.selected_cell = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.givens = [[False for _ in range(9)] for _ in range(9)]
        self.solution_board = [[0 for _ in range(9)] for _ in range(9)]
        self.current_board = [[0 for _ in range(9)] for _ in range(9)]
        self.mistakes = 0
        self.is_paused = False
        self.elapsed_seconds = 0
        self.timer_job = None
        self.pause_overlay_btn = None
        self.pause_overlay_win = None

        title = tk.Label(root, text="Sudoku Game", font=("Helvetica", 20, "bold"))
        title.pack(pady=10)

        main_frame = tk.Frame(root, bg=self.default_bg)
        main_frame.pack(padx=10, pady=10)

        self.grid_container = tk.Frame(main_frame)
        self.grid_container.grid(row=0, column=0, sticky="n")

        self.grid_frame = tk.Frame(self.grid_container, bg="black")
        self.grid_frame.pack()

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.grid_frame, width=2, font=("Helvetica", 22), justify='center',
                                 highlightthickness=0, relief="flat")
                entry.configure(insertontime=0)

                top = 2 if i % 3 == 0 else 1
                left = 2 if j % 3 == 0 else 1
                bottom = 2 if i == 8 else 0
                right = 2 if j == 8 else 0

                entry.grid(row=i, column=j, ipadx=10, ipady=10, padx=(left, right), pady=(top, bottom))

                entry.bind("<FocusIn>", lambda e, row=i, col=j: self.select_cell(row, col))
                entry.bind("<KeyPress>", self.on_keypress)
                entry.bind("<Up>", lambda e, row=i, col=j: self.move_cursor(row-1, col))
                entry.bind("<Down>", lambda e, row=i, col=j: self.move_cursor(row+1, col))
                entry.bind("<Left>", lambda e, row=i, col=j: self.move_cursor(row, col-1))
                entry.bind("<Right>", lambda e, row=i, col=j: self.move_cursor(row, col+1))

                self.cells[i][j] = entry

        self.right_frame = tk.Frame(main_frame, bg=self.default_bg)
        self.right_frame.grid(row=0, column=1, padx=(30, 10), sticky="n")

        self.top_bar = tk.Frame(self.right_frame, bg=self.default_bg)
        self.top_bar.pack(fill="x", pady=(0, 10))

        left_col = tk.Frame(self.top_bar, bg=self.default_bg)
        left_col.pack(side="left", anchor="w", padx=(0, 20))
        tk.Label(left_col, text="Mistakes", font=self.small_font, fg=self.muted_fg, bg=self.default_bg).pack(anchor="w")
        self.mistake_label = tk.Label(left_col, text="0", font=self.small_font, fg=self.muted_fg, bg=self.default_bg)
        self.mistake_label.pack(anchor="w")

        right_group = tk.Frame(self.top_bar, bg=self.default_bg)
        right_group.pack(side="right", anchor="e")

        time_col = tk.Frame(right_group, bg=self.default_bg)
        time_col.pack(side="left", anchor="e", padx=(0, 8))
        tk.Label(time_col, text="Time", font=self.small_font, fg=self.muted_fg, bg=self.default_bg).pack()
        self.timer_label = tk.Label(time_col, text="00:00", font=self.small_font, fg=self.muted_fg, bg=self.default_bg)
        self.timer_label.pack()

        self.pause_btn = self.create_custom_button(right_group, text="⏸", width=3, height=1,
                                                   command=self.toggle_pause)
        self.pause_btn.pack(side="left", anchor="e")

        util_frame = tk.Frame(self.right_frame, bg=self.default_bg)
        util_frame.pack(pady=(0, 10))
        self.create_icon_button(util_frame, "⟲", self.clear_user_inputs, width=3).grid(row=0, column=0, padx=5)
        self.create_icon_button(util_frame, "⌫", self.erase_cell, width=3).grid(row=0, column=1, padx=5)
        self.create_icon_button(util_frame, "💡", self.hint_cell, width=3).grid(row=0, column=2, padx=5)

        numbers_frame = tk.Frame(self.right_frame, bg=self.default_bg)
        numbers_frame.pack()
        for num in range(1, 10):
            row = (num - 1) // 3
            col = (num - 1) % 3
            btn = self.create_custom_button(numbers_frame, text=str(num), command=lambda n=num: self.place_number(n))
            btn.grid(row=row, column=col, padx=5, pady=5)

        spacer = tk.Frame(self.right_frame, bg=self.default_bg)
        spacer.pack(expand=True, fill="both")

        self.new_game_btn = self.create_custom_button(
            self.right_frame, text="New Game", width=14, height=2,
            bg="#5a7bc0", fg="white", hover_bg="#4b69ad",
            command=self.open_new_game_dialog
        )
        self.new_game_btn.pack(pady=(10, 0))

        self.root.bind("<Button-1>", self.handle_root_click)

        try:
           self.start_new_game(40, None)
        except Exception:
            pass

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

    def create_icon_button(self, parent, icon, command, width=3, height=1):
        return self.create_custom_button(parent, text=icon, command=command, width=width, height=height)

    def open_new_game_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Game Mode")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.default_bg)

        tk.Label(dialog, text="Select Game Mode", font=("Helvetica", 16, "bold"), bg=self.default_bg).pack(pady=(15, 5))
        tk.Label(dialog, text="Current game progress will be lost", font=("Helvetica", 10), bg=self.default_bg).pack(pady=(0, 15))

        btn_frame = tk.Frame(dialog, bg=self.default_bg)
        btn_frame.pack(padx=10, pady=(0, 15))

        options = [
            ("Easy", 40),
            ("Medium", 32),
            ("Hard", 26),
            ("Extreme", 17),
        ]

        for idx, (name, given) in enumerate(options):
            b = self.create_custom_button(btn_frame, text=name, width=8, height=1,
                                          bg="#5a7bc0", fg="white", hover_bg="#4b69ad",
                                          command=lambda g=given, d=dialog: self.start_new_game(g, d))
            b.grid(row=0, column=idx, padx=5)

        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

    def start_new_game(self, givens_count, dialog):
        try:
            dialog.destroy()
        except Exception:
            pass
        self.generate_puzzle(givens_count)
        self.render_board()
        self.reset_status()
        self.start_timer()

    def generate_puzzle(self, givens_count):
        solved = [[0 for _ in range(9)] for _ in range(9)]
        solve_board(solved)
        self.solution_board = copy.deepcopy(solved)

        import random
        all_cells = [(i, j) for i in range(9) for j in range(9)]
        cells_to_keep = set(random.sample(all_cells, max(17, min(81, givens_count))))
        self.current_board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if (i, j) in cells_to_keep:
                    self.current_board[i][j] = self.solution_board[i][j]
                    self.givens[i][j] = True
                else:
                    self.current_board[i][j] = 0
                    self.givens[i][j] = False

    def render_board(self):
        for i in range(9):
            for j in range(9):
                entry = self.cells[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                val = self.current_board[i][j]
                if val != 0:
                    entry.insert(0, str(val))
                if self.givens[i][j]:
                    entry.config(state="disabled", disabledforeground="#000000", disabledbackground="white")
                else:
                    entry.config(state="normal", fg="#000000", bg="white")
        self.selected_cell = None
        self.highlight_selection()

    def reset_status(self):
        self.mistakes = 0
        self.mistake_label.config(text=f"{self.mistakes}")
        self.elapsed_seconds = 0
        self.timer_label.config(text="00:00")
        self.is_paused = False
        if self.pause_overlay_btn:
            try:
                self.pause_overlay_btn.destroy()
            except Exception:
                pass
            self.pause_overlay_btn = None
        if self.pause_overlay_win:
            try:
                self.pause_overlay_win.destroy()
            except Exception:
                pass
            self.pause_overlay_win = None
        if self.pause_btn:
            self.pause_btn.config(text="⏸")

    def start_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None
        self.update_timer()

    def update_timer(self):
        if not self.is_paused:
            self.elapsed_seconds += 1
            m = self.elapsed_seconds // 60
            s = self.elapsed_seconds % 60
            self.timer_label.config(text=f"{m:02d}:{s:02d}")
        self.timer_job = self.root.after(1000, self.update_timer)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.hide_numbers()
            self.show_pause_overlay()
            if self.pause_btn:
                self.pause_btn.config(text="⏵")
        else:
            self.show_numbers()
            self.hide_pause_overlay()
            if self.pause_btn:
                self.pause_btn.config(text="⏸")

    def show_pause_overlay(self):
        if self.pause_overlay_win is not None:
            return
        color_key = "#ff00fe"
        size = 90

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        try:
            win.wm_attributes("-topmost", True)
            win.wm_attributes("-transparentcolor", color_key)
        except Exception:
            pass
        win.configure(bg=color_key)

        canvas = tk.Canvas(win, width=size, height=size, bg=color_key, highlightthickness=0, bd=0, relief="flat", cursor="hand2")
        canvas.pack()

        canvas.create_oval(1, 1, size-1, size-1, fill="#5a7bc0", outline="#5a7bc0")
        canvas.create_oval(3, 3, size-3, size-3, outline="#5a7bc0")

        cx, cy = size/2, size/2
        tri_w, tri_h = 26, 30
        cx_adj = cx - 3
        points = [cx_adj - tri_w/4, cy - tri_h/2,  cx_adj + tri_w*3/4, cy,  cx_adj - tri_w/4, cy + tri_h/2]
        canvas.create_polygon(points, fill="white", outline="white")
        canvas.bind("<Button-1>", lambda e: self.toggle_pause())

        self.root.update_idletasks()
        gx = self.grid_container.winfo_rootx()
        gy = self.grid_container.winfo_rooty()
        gw = self.grid_container.winfo_width()
        gh = self.grid_container.winfo_height()
        x = gx + (gw - size) // 2
        y = gy + (gh - size) // 2
        win.geometry(f"{size}x{size}+{x}+{y}")

        self.pause_overlay_win = win
        self.pause_overlay_btn = canvas

    def hide_pause_overlay(self):
        if self.pause_overlay_btn:
            try:
                self.pause_overlay_btn.destroy()
            except Exception:
                pass
            self.pause_overlay_btn = None
        if self.pause_overlay_win:
            try:
                self.pause_overlay_win.destroy()
            except Exception:
                pass
            self.pause_overlay_win = None

    def hide_numbers(self):
        for i in range(9):
            for j in range(9):
                e = self.cells[i][j]
                e.config(state="normal")
                e.delete(0, tk.END)
                if self.givens[i][j]:
                    e.config(state="disabled", disabledbackground="white")

    def show_numbers(self):
        for i in range(9):
            for j in range(9):
                e = self.cells[i][j]
                e.config(state="normal")
                e.delete(0, tk.END)
                val = self.current_board[i][j]
                if val != 0:
                    e.insert(0, str(val))
                if self.givens[i][j]:
                    e.config(state="disabled", disabledforeground="#000000", disabledbackground="white")

    def select_cell(self, row, col):
        self.selected_cell = (row, col)
        self.highlight_selection()

    def move_cursor(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            self.select_cell(row, col)

    def on_keypress(self, event):
        if self.is_paused:
            return "break"
        if event.char in "123456789":
            self.place_number(int(event.char))
            return "break"
        if event.keysym in ("BackSpace", "Delete"):
            self.erase_cell()
            return "break"
        return None

    def place_number(self, num):
        if self.is_paused:
            return
        if not self.selected_cell:
            return
        r, c = self.selected_cell
        if self.givens[r][c]:
            return
        correct = self.solution_board[r][c]
        entry = self.cells[r][c]
        entry.config(state="normal")
        if num == correct:
            self.current_board[r][c] = num
            entry.delete(0, tk.END)
            entry.insert(0, str(num))
            entry.config(bg="white", fg="#000000")
        else:
            self.mistakes += 1
            self.mistake_label.config(text=f"{self.mistakes}")
            self.current_board[r][c] = num
            entry.delete(0, tk.END)
            entry.insert(0, str(num))
        self.highlight_selection()
        self.check_game_finished()

    def erase_cell(self):
        if self.is_paused or not self.selected_cell:
            return
        r, c = self.selected_cell
        if self.givens[r][c]:
            return
        self.current_board[r][c] = 0
        e = self.cells[r][c]
        e.config(state="normal")
        e.delete(0, tk.END)
        self.highlight_selection()

    def clear_user_inputs(self):
        if self.is_paused:
            return
        for i in range(9):
            for j in range(9):
                if not self.givens[i][j]:
                    self.current_board[i][j] = 0
                    e = self.cells[i][j]
                    e.config(state="normal")
                    e.delete(0, tk.END)
                    e.config(bg="white", fg="#000000")
        self.highlight_selection()

    def hint_cell(self):
        if self.is_paused or not self.selected_cell:
            return
        r, c = self.selected_cell
        if self.givens[r][c]:
            return
        if self.current_board[r][c] == 0:
            num = self.solution_board[r][c]
            self.current_board[r][c] = num
            e = self.cells[r][c]
            e.config(state="normal")
            e.delete(0, tk.END)
            e.insert(0, str(num))
            e.config(bg="white", fg="#000000")
        self.highlight_selection()
        self.check_game_finished()

    def is_board_complete(self):
        """Return True if there are no empty cells in the current board."""
        for i in range(9):
            for j in range(9):
                if self.current_board[i][j] == 0:
                    return False
        return True

    def check_game_finished(self):
        """If the puzzle is correctly solved, stop the timer and show a dialog."""
        if self.is_paused or not self.is_board_complete():
            return

        if self.current_board != self.solution_board:
            return

        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        self.is_paused = True

        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        try:
            messagebox.showinfo(
                "Congratulations!",
                f"You solved the puzzle!\n\nTime: {time_str}\nMistakes: {self.mistakes}",
                parent=self.root,
            )
        except Exception:
            pass

        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                try:
                    cell.config(state="normal")
                    cell.config(fg="#000000", bg="white")
                    cell.config(state="disabled", disabledforeground="#000000", disabledbackground="white")
                except Exception:
                    pass

    def handle_root_click(self, event):
        widget = event.widget
        if isinstance(widget, tk.Entry):
            return
        if isinstance(widget, tk.Button):
            if widget['text'] in [str(i) for i in range(1, 10)] + ["⌫", "⟲", "💡", "New Game", "⏸", "⏵"]:
                return
        self.selected_cell = None
        self.highlight_selection()

    def highlight_selection(self):
        for i in range(9):
            for j in range(9):
                e = self.cells[i][j]
                if self.givens[i][j]:
                    e.config(state="disabled", disabledforeground="#000000", disabledbackground="white")
                else:
                    e.config(bg="white", fg="#000000")

        if self.selected_cell:
            row, col = self.selected_cell
            for i in range(9):
                if self.givens[row][i]:
                    self.cells[row][i].config(state="disabled", disabledbackground="#e0f0ff")
                else:
                    self.cells[row][i].config(bg="#e0f0ff")
                if self.givens[i][col]:
                    self.cells[i][col].config(state="disabled", disabledbackground="#e0f0ff")
                else:
                    self.cells[i][col].config(bg="#e0f0ff")
            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if self.givens[i][j]:
                        self.cells[i][j].config(state="disabled", disabledbackground="#e0f0ff")
                    else:
                        self.cells[i][j].config(bg="#e0f0ff")

            selected_val = self.cells[row][col].get()
            if selected_val:
                for i in range(9):
                    for j in range(9):
                        if (i, j) == (row, col):
                            continue
                        if self.cells[i][j].get() == selected_val:
                            same_num_bg = "#cfe4ff"
                            if self.givens[i][j]:
                                self.cells[i][j].config(
                                    state="disabled",
                                    disabledbackground=same_num_bg,
                                )
                            else:
                                self.cells[i][j].config(bg=same_num_bg)

        for i in range(9):
            for j in range(9):
                val = self.cells[i][j].get()
                if not val:
                    continue

                def mark_conflict_cell(rr, cc):
                    cell = self.cells[rr][cc]
                    is_selected = self.selected_cell and (rr, cc) == self.selected_cell
                    if self.givens[rr][cc]:
                        cell.config(
                            state="disabled",
                            disabledbackground="#fddede",
                            disabledforeground="red",
                        )
                    else:
                        if is_selected:
                            cell.config(fg="red")
                        else:
                            cell.config(bg="#fddede", fg="red")

                for k in range(9):
                    if k != j and self.cells[i][k].get() == val:
                        mark_conflict_cell(i, j)
                        mark_conflict_cell(i, k)
                for k in range(9):
                    if k != i and self.cells[k][j].get() == val:
                        mark_conflict_cell(i, j)
                        mark_conflict_cell(k, j)
                box_row = (i // 3) * 3
                box_col = (j // 3) * 3
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r != i or c != j) and self.cells[r][c].get() == val:
                            mark_conflict_cell(i, j)
                            mark_conflict_cell(r, c)

        if self.selected_cell:
            row, col = self.selected_cell
            e = self.cells[row][col]
            is_conflict = False
            try:
                is_conflict = (e.cget("fg") == "red")
            except Exception:
                pass
            if self.givens[row][col]:
                e.config(
                    state="disabled",
                    disabledbackground="#a5d8ff",
                    disabledforeground="red" if is_conflict else "#000000",
                )
            else:
                e.config(
                    bg="#a5d8ff",
                    fg="red" if is_conflict else "#000000",
                )
            try:
                e.focus_set()
            except Exception:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGame(root)
    root.mainloop()


