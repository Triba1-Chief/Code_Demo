
import random

EASY = 0.1
MEDIUM = 0.3
HARD = 0.5

#Question 1
def init_board(nb_rows,nb_cols,value):
    board = []

    for i in range(nb_rows):
        board.append([])
        for j in range(nb_cols):
            board[i].append(value)
    return board

def count_total(board, value):
    count = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == value:
                count += 1

    return count

def is_valid_position(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def get_neighbour_positions(board, row, col):
    neighbours = []

    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if is_valid_position(board, i, j) and not (i == row and j == col):
                neighbours.append([i, j])

    return neighbours

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
get_neighbour_positions(board,1,1)

def count_neighbours(board, row, col, value):
    neighbours = get_neighbour_positions(board, row, col)
    count = 0

    for neighbour in neighbours:
        if board[neighbour[0]][neighbour[1]] == value:
            count += 1

    return count

#Question 2
def new_mine_position(board):
    row = random.randint(0, len(board) - 1)
    column = random.randint(0, len(board[0]) - 1)

    while board[row][column] == -1:
        row = random.randint(0, len(board) - 1)
        column = random.randint(0, len(board[0]) - 1)

    return row, column

def new_mine(board):
    row,column = new_mine_position(board)
    board[row][column] = -1

    neighbours = get_neighbour_positions(board, row, column)
    for neighbour in neighbours:
        if board[neighbour[0]][neighbour[1]] != -1:
            board[neighbour[0]][neighbour[1]] += 1

def generate_helper_board(nb_rows, nb_cols, nb_mines):
    board = init_board(nb_rows,nb_cols,-1)

    count = nb_mines

    while count > 0:
        new_mine(board)
        count -= 1

    return board

#Question 3
def flag(board, row, col):
    if board[row][col] == "?":
        board[row][col] = "\u2691"
    elif board[row][col] == "\u2691":
        board[row][col] = "?"

def reveal(helper_board, game_board, row, col):
    if helper_board[row][col] == -1:
        raise AssertionError("BOOM! You lost.")
    else:
        game_board[row][col] = str(helper_board[row][col])

def print_board(board):
    for row in board:
       print(' '.join(row))

#Question 4
def play():
    rows = int(input("Enter number of rows for the board: "))
    cols = int(input("Enter number of columns for the board: "))
    difficulty = input("Choose a difficulty from [EASY, MEDIUM, HARD]: ")


    if difficulty == "EASY":
        difficulty = EASY
    elif difficulty == "MEDIUM":
        difficulty = MEDIUM
    else:
        difficulty = HARD


    nb_mines = round(rows * cols * difficulty, 0)
    helper_board = generate_helper_board(rows, cols, nb_mines)
    game_board = init_board(rows, cols, "?")

    while count_total(game_board,"?") + count_total(game_board,"\u2691") > nb_mines:
        print("Current Board: (" + str(nb_mines - count_total(game_board,"\u2691")) + " mines remaining)")
        print_board(game_board)

        decision = int(input("Choose 0 to reveal or 1 to flag: "))
        user_row = int(input("Which row?"))
        user_col = int(input("Which column?"))

        if decision == 0:
            reveal(helper_board, game_board, user_row, user_col)
        elif decision == 1:
            flag(game_board, user_row, user_col)


    for row in range(rows):
        for col in range(cols):
            if game_board[row][col] == "?":
                game_board[row][col] = "\u2691"

    print("Congratulations! You won!")
    print("Final Board:")
    print_board(game_board)

#Question 5
# def left_click(row, col): #Do they need to define this?
#     reveal(helper_board, game_board, row, col)
#
# def right_click(row, col):
#     flag(game_board, row, col)

def solve_cell(board, row, col, left_click, right_click):
    if board[row][col] == "?" or board[row][col] == "\u2691":
        return

    neighbours = get_neighbour_positions(board, row, col)
    nb_mines = int(board[row][col])

    if count_neighbours(board, row, col, "\u2691") == nb_mines:
        for neighbour in neighbours:
            if board[neighbour[0]][neighbour[1]] == "?":
                left_click(neighbour[0], neighbour[1])
    elif count_neighbours(board, row, col, "\u2691") + count_neighbours(board, row, col, "?") == nb_mines:
        for neighbour in neighbours:
            if board[neighbour[0]][neighbour[1]] == "?":
                right_click(neighbour[0], neighbour[1])

def solve(board, left_click, right_click):
    while count_total(board, "?") > 0:
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == "?":
                    solve_cell(board, row, col, left_click, right_click)











