import random

def is_valid(board, row, col, num):
    # Row check
    for x in range(9):
        if board[row][x] == num:
            return False

    # Column check
    for x in range(9):
        if board[x][col] == num:
            return False

    # 3x3 box check
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_board(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)  # Add randomness

    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_board(board):
                return True
            board[row][col] = 0

    return False


def solve_gui_board(gui_cells):
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Read values from GUI
    for i in range(9):
        for j in range(9):
            val = gui_cells[i][j].get()
            if val.isdigit():
                board[i][j] = int(val)

    # Solve it
    if solve_board(board):
        for i in range(9):
            for j in range(9):
                gui_cells[i][j].delete(0, 'end')
                gui_cells[i][j].insert(0, str(board[i][j]))
        return True
    else:
        return False

def generate_random_puzzle(given=None):
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_board(board)

    # Number of filled cells to keep
    if given is None:
        given = random.randint(17, 30)

    cells_to_keep = random.sample([(i, j) for i in range(9) for j in range(9)], given)
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    for i, j in cells_to_keep:
        puzzle[i][j] = board[i][j]

    return puzzle
