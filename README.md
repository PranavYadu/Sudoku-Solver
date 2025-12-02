# 🧩 Sudoku Solver

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)

A modern, user-friendly Sudoku Solver with three modes:
- **Manual Input**: Enter Sudoku puzzles by hand in a beautiful GUI.
- **Image Upload**: Upload a photo of a Sudoku puzzle and let the app recognise and solve it using OCR and computer vision.
- **Play Game**: Solve Sudoku on your own for fun

## Features
- **Manual Input Mode**
  - Intuitive 9x9 grid for entering puzzles.
  - Number pad and control buttons for easy editing.
  - Highlights conflicts and solved cells.
  - Option to generate a random puzzle.
  - Solve button instantly fills in the solution.
  - **Show Backtracking**: Visualize the solving process step-by-step.

- **Image Upload Mode**
  - Upload a photo or scan of a Sudoku puzzle.
  - Automatic grid detection and digit recognition (using OpenCV and Tesseract OCR).
  - Solves the puzzle and overlays the solution on the image.
  - Option to save the solved image.
 
- **Game Mode**
  - **Difficulty Levels**: Easy, Medium, Hard, Extreme
  
  - **Game Controls**
    - **Number Pad**: Click numbers 1-9 to fill cells
    - **Hint Button**: Get a hint for the current puzzle
    - **Clear Button**: Clear all user entries
    - **Reset Button**: Reset the puzzle to the initial state
  
  - **Features**
    - Real-time conflict detection
    - Timer to track solving time
    - Score calculation based on difficulty and time
    - Highlights for row, column, and box
    - Tracks player statistics and best times

## Visualise Backtracking

In manual mode, after solving a Sudoku puzzle, you can click the **Show Backtracking** button to visualise the backtracking algorithm step-by-step. This feature animates how the solver explores possibilities and finds the solution, helping you understand the solving process.

- **How to use:**
  1. Enter your puzzle in manual mode.
  2. Click **Solve** to solve the puzzle.
  3. Click **Visualize** to watch the solving process animated in the GUI with 1x, 2x or 4x speed.

## Technologies Used
- Python 3
- Tkinter (GUI)
- OpenCV (image processing)
- pytesseract (OCR)
- PIL/Pillow (image handling)

## Getting Started

### Prerequisites
- Python 3.x
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (required for image mode)
- Install required Python packages:

```bash
pip install opencv-python pytesseract pillow numpy
```

### Tesseract Setup
- Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
- Update the `pytesseract.pytesseract.tesseract_cmd` path in `image_upload.py` if needed.

## 🚀 Clone Repository

To get started with the Sudoku Solver on your local machine, clone the repository using:

```bash
git clone https://github.com/PranavYadu/Sudoku-Solver.git
cd sudoku-solver
```

### Running the App

```bash
python main.py
```

- Choose **Manual Input** to enter a puzzle by hand.
- Choose **Image Upload** to solve a puzzle from an image.
- Choose **Play Game** to play sudoku for fun.

## Screenshots

### Sudoku Solver GUI
<img width="1033" height="794" alt="Screenshot 2025-08-28 114231" src="https://github.com/user-attachments/assets/4a113c6f-7be9-4e23-9126-a185e9f1846e" />

## Acknowledgments

- **OpenCV** – used for image preprocessing and grid detection.  
- **Tesseract OCR** – used for recognising digits from Sudoku images.  
- **Tkinter** – used for building the interactive graphical user interface.  
- **Python** – the core language that powers the solver and algorithm.  

## Feedback

If you have any feedback, ideas, or want to contribute to this project, feel free to:  
- Open an **issue** in the repository.  
- Submit a **pull request** with improvements.  

We truly appreciate community input and contributions! 🚀
