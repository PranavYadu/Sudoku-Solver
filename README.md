🧩 Sudoku Solver

A Python-based Sudoku Solver with a modern Tkinter GUI, offering two solving modes:

Manual Input Mode – enter puzzles by hand.

Image Upload Mode – automatically detect and solve Sudoku from an image using OpenCV and Tesseract OCR.

✨ Features

🔢 Manual Input – fill numbers into a 9x9 interactive grid.

📷 Image Upload – upload a Sudoku image, automatically detect the grid, extract digits, and solve it.

🎨 Modern UI – clean Tkinter interface with styled buttons and hover effects.

🎲 Random Puzzle Generator – generate random Sudoku puzzles with a chosen number of clues.

✅ Backtracking Solver – efficient algorithm to solve any valid Sudoku puzzle.

📌 Conflict Highlighting – shows duplicate numbers in row, column, or 3×3 box.

💾 Save Solved Puzzle (Image mode) – save the solved Sudoku as an image.

⌨️ Keyboard & Mouse Controls – easy navigation with arrow keys and input validation.

📂 Project Structure
Sudoku-Solver/
│── main.py              # Main launcher with mode selection
│── mannual_input.py     # Manual Sudoku input GUI
│── image_upload.py      # Image upload + OCR + solver GUI
│── solver.py            # Backtracking solver & puzzle generator

🚀 Getting Started
1. Clone Repository
git clone https://github.com/your-username/sudoku-solver.git
cd sudoku-solver

2. Install Dependencies

Make sure you have Python 3.8+ installed, then install the required libraries:

pip install opencv-python pillow pytesseract numpy

3. Install Tesseract OCR

Download from: Tesseract OCR

Update the path in image_upload.py if necessary:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

4. Run the App
python main.py

🖼️ Usage
Manual Input Mode

Enter digits directly in the 9×9 grid.

Use arrow keys to move between cells.

Click Solve to complete the puzzle.

Use buttons:

⟲ Reset Grid

⌫ Erase Cell

🎲 Fill Random Puzzle

Image Upload Mode

Upload a Sudoku image (JPG/PNG).

The app detects the grid, extracts digits, and solves it.

Solved numbers appear in blue (#5a7bc0).

Option to save the solved image.

🧮 Solver Algorithm

The project uses a backtracking algorithm:

Find an empty cell.

Try digits 1–9.

Validate against Sudoku rules.

Recursively continue until solved or backtrack if stuck.

🎯 Future Improvements

Step-by-step solving visualization.

Difficulty classifier for puzzles.

Mobile/desktop standalone application (PyInstaller).

Enhanced OCR with deep learning digit recognition.
