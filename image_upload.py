import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageTk

# Set Tesseract path (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Core Sudoku Functions ---

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (600, 600))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    return img, thresh

def find_sudoku_contour(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = np.array([])
    max_area = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 1000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4 and area > max_area:
                biggest = approx
                max_area = area
    return biggest

def reorder(points):
    points = points.reshape((4, 2))
    new = np.zeros((4, 2), dtype=np.float32)
    add = points.sum(1)
    diff = np.diff(points, axis=1)
    new[0] = points[np.argmin(add)]
    new[2] = points[np.argmax(add)]
    new[1] = points[np.argmin(diff)]
    new[3] = points[np.argmax(diff)]
    return new

def warp_image(img, points):
    reordered = reorder(points)
    pts1 = reordered
    pts2 = np.float32([[0, 0], [450, 0], [450, 450], [0, 450]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (450, 450))
    return imgWarp

def split_cells(img):
    rows = np.vsplit(img, 9)
    cells = []
    for row in rows:
        cols = np.hsplit(row, 9)
        cells.append(cols)
    return cells

def extract_digits(cells):
    board = []
    for row in cells:
        line = []
        for cell in row:
            cell = cell[5:-5, 5:-5]
            _, bin_cell = cv2.threshold(cell, 100, 255, cv2.THRESH_BINARY_INV)
            config = r'--psm 10 -c tessedit_char_whitelist=123456789'
            text = pytesseract.image_to_string(bin_cell, config=config)
            digit = ''.join(filter(str.isdigit, text))
            line.append(int(digit) if digit else 0)
        board.append(line)
    return board

def find_empty(b):
    for i in range(9):
        for j in range(9):
            if b[i][j] == 0:
                return i, j
    return None

def is_valid(b, num, pos):
    row, col = pos
    for j in range(9):
        if b[row][j] == num and j != col:
            return False
    for i in range(9):
        if b[i][col] == num and i != row:
            return False
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if b[i][j] == num and (i, j) != pos:
                return False
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

def draw_solution(warp, board, original):
    cell_size = 50
    for i in range(9):
        for j in range(9):
            if original[i][j] == 0:
                text = str(board[i][j])
                pos = (j * cell_size + 15, i * cell_size + 35)
                # #5a7bc0 in BGR is (192, 123, 90)
                cv2.putText(warp, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (192, 123, 90), 2)
    return warp

# --- GUI ---

class SudokuApp:
    def __init__(self, root):
        self.root = root
        def close_on_esc(event=None):
            self.root.destroy()
        self.root.bind('<Escape>', close_on_esc)
        self.root = root
        self.root.title("Sudoku Solver")

        tk.Label(root, text="Sudoku Solver", font=("Helvetica", 20, "bold")).pack(pady=10)

        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.btn_font = ("Helvetica", 12, "bold")
        self.btn_bg = "#5a7bc0"
        self.btn_hover = "#4b69ad"

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image,
                                    font=self.btn_font, bg=self.btn_bg, fg="white", relief="flat",
                                    width=14, height=2, activebackground=self.btn_bg, activeforeground="white",
                                    borderwidth=0, highlightthickness=0)
        self.upload_btn.pack(pady=10)

        # Add hover effect to upload button
        def on_enter(e): self.upload_btn.config(bg=self.btn_hover)
        def on_leave(e): self.upload_btn.config(bg=self.btn_bg)
        self.upload_btn.bind("<Enter>", on_enter)
        self.upload_btn.bind("<Leave>", on_leave)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return

        img, thresh = preprocess_image(file_path)
        contour = find_sudoku_contour(thresh)

        if contour.size == 0:
            messagebox.showerror("Error", "Sudoku grid not found!")
            return

        warped = warp_image(img, contour)
        warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        cells = split_cells(warped_gray)
        puzzle = extract_digits(cells)
        original = [row[:] for row in puzzle]

        if solve(puzzle):
            solved_img = draw_solution(warped.copy(), puzzle, original)
            self.show_image(solved_img)
            # Remove solved label if present
            if hasattr(self, 'solved_label') and self.solved_label.winfo_exists():
                self.solved_label.destroy()
            # Remove upload button
            if hasattr(self, 'upload_btn') and self.upload_btn.winfo_exists():
                self.upload_btn.pack_forget()
            # Show Save Image button with hover effect
            self.save_img = solved_img  # Store for saving
            self.save_btn = tk.Button(self.root, text="Save Image", font=self.btn_font, bg="#5a7bc0", fg="white",
                                     width=14, height=2, relief="flat", borderwidth=0, highlightthickness=0,
                                     activebackground="#4b69ad", activeforeground="white",
                                     command=self.save_image)
            self.save_btn.pack(pady=10)
            def on_enter(e): self.save_btn.config(bg="#4b69ad")
            def on_leave(e): self.save_btn.config(bg="#5a7bc0")
            self.save_btn.bind("<Enter>", on_enter)
            self.save_btn.bind("<Leave>", on_leave)
        else:
            messagebox.showerror("Error", "Could not solve the puzzle.")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            cv2.imwrite(file_path, self.save_img)
            messagebox.showinfo("Saved", f"Image saved to {file_path}")
        if hasattr(self, 'save_btn') and self.save_btn.winfo_exists():
            self.save_btn.destroy()

    def show_image(self, img_cv2):
        img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.canvas.config(image=img_tk)
        self.canvas.image = img_tk


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
