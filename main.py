import tkinter as tk
import mannual_input
import image_upload
import game

def launch_gui():
    mannual_input.SudokuGUI(tk.Tk())

def launch_image():
    image_upload.SudokuApp(tk.Tk())

def launch_game():
    game.SudokuGame(tk.Tk())

def main():
    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry("400x380")
    root.configure(bg="#eaeef1")
    def close_on_esc(event=None):
        root.destroy()
    root.bind('<Escape>', close_on_esc)

    title = tk.Label(root, text="Sudoku Solver", font=("Helvetica", 30, "bold"), bg="#eaeef1", fg="#000000")
    title.pack(pady=30)

    btn_font = ("Helvetica", 18, "bold")
    btn_bg = "#5a7bc0"
    btn_fg = "white"
    btn_hover = "#4b69ad"

    def make_button(text, command):
        btn = tk.Button(root, text=text, font=btn_font, bg=btn_bg, fg=btn_fg, relief="flat",
                       width=14, height=2, activebackground=btn_bg, activeforeground=btn_fg, borderwidth=0, highlightthickness=0,
                       command=command)
        def on_enter(e): btn.config(bg=btn_hover)
        def on_leave(e): btn.config(bg=btn_bg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    manual_btn = make_button("Manual Input", lambda: [root.destroy(), launch_gui()])
    manual_btn.pack(pady=5)

    image_btn = make_button("Image Upload", lambda: [root.destroy(), launch_image()])
    image_btn.pack(pady=5)

    game_btn = make_button("Play Game", lambda: [root.destroy(), launch_game()])
    game_btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
