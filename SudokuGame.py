import pickle
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random
import copy


class SudokuGame:
    def __init__(self, root, saved=None, difficulty_level=None):
        self.root = root
        self.root.title("Sudoku Game")
        self.level_var = tk.StringVar(value=difficulty_level)
        self.entries = []
        self.hints = 0
        self.generate_sudoku(saved)
        self.create_grid()

    def create_grid(self):
        # Add a ttk Style for customizing widgets
        style = ttk.Style()
        style.configure("TFrame", background="#ececec")  # Set background color for frames
        style.configure("TLabel", font=("Arial", 12), background="#ececec")  # Set font and background color for labels
        style.configure("TButton", font=("Arial", 12, "bold"), background="#ececec")  # Set font, background, and text color for buttons

        level_frame = ttk.Frame(self.root, style="TFrame")
        level_frame.grid(row=9, columnspan=9)

        solve_button = ttk.Button(self.root, text="Solve", command=self.solve_sudoku, style="TButton")
        solve_button.grid(row=10, columnspan=9)

        save_button = ttk.Button(self.root, text="Save Game", command=self.save_game)
        save_button.grid(row=11, columnspan=9)

        hint_button = ttk.Button(self.root, text="Hint", command=self.hint)
        hint_button.grid(row=12, columnspan=9)

        self.draw_grid_lines()    # Draw horizontal and vertical lines
        self.display_board()      # Display the board

    def draw_grid_lines(self):
        canvas = tk.Canvas(self.root, width=450, height=450, highlightthickness=0, background="#ececec")
        canvas.grid(row=0, column=0, rowspan=9, columnspan=9)

        for i in range(1, 9):
            # Draw horizontal lines
            canvas.create_line(0, i * 50, 450, i * 50, fill="black")

            # Draw vertical lines
            canvas.create_line(i * 50, 0, i * 50, 450, fill="black")

        # Draw bold lines to separate 3x3 blocks
        for i in range(0, 9, 3):
            canvas.create_line(0, i * 50, 450, i * 50, width=2, fill="black")
            canvas.create_line(i * 50, 0, i * 50, 450, width=2, fill="black")

    def generate_sudoku(self, saved=None):
        if saved:
            self.board = saved
            self.solved_board = self.generate_solved_board()
        else:
            self.board = np.full((9, 9), 0)
            self.solve_sudoku_recursive(self.board)
            self.solved_board = copy.deepcopy(self.board)
            self.remove_numbers()

    def generate_solved_board(self):
        solved_board = copy.deepcopy(self.board)
        self.solve_sudoku_recursive(solved_board)
        return solved_board

    def save_game(self, filename="sudoku_savegame.pkl"):
        try:
            saved_data = {'board': self.board, 'entries': []}

            for i in range(9):
                row_entries = []
                for j in range(9):
                    if isinstance(self.entries[i][j], tk.Entry):
                        row_entries.append(self.entries[i][j].get())
                    else:
                        row_entries.append(str(self.board[i][j]))
                saved_data['entries'].append(row_entries)

            with open(filename, 'wb') as file:
                pickle.dump(saved_data, file)
            messagebox.showinfo("Save", "Game saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving game: {e}")

    def remove_numbers(self):
        level = self.level_var.get()
        difficulty_levels = {
            "Easy": 30,
            "Medium": 45,
            "Hard": 60
        }

        for _ in range(difficulty_levels.get(level)):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.board[row][col] = 0

    def validate_cell(self, grid, number, row, col):
        for i in range(len(grid)):
            if grid[row][i] == number or grid[i][col] == number:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for block_i in range(start_row, start_row + 3):
            for block_j in range(start_col, start_col + 3):
                if grid[block_i][block_j] == number:
                    return False

        return True

    def solve_sudoku_recursive(self, board):
        empty_cell = self.find_empty_cell(board)

        if not empty_cell:
            # If no empty cell is found, the Sudoku is solved
            return True

        row, col = empty_cell

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.validate_cell(board, num, row, col):
                board[row][col] = num

                if self.solve_sudoku_recursive(board):
                    return True

                # If the current assignment leads to an invalid solution, backtrack
                board[row][col] = 0

        # If no number can be placed in the current cell, backtrack
        return False

    def find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def display_board(self):
        for i in range(9):
            row = []
            for j in range(9):
                if self.board[i][j] != 0:
                    entry = tk.Label(self.root, text=str(self.board[i][j]), width=2, font=('Arial', 20))
                else:
                    entry = tk.Entry(self.root, width=2, font=('Arial', 20))
                entry.grid(row=i, column=j)
                row.append(entry)
            self.entries.append(row)

    def empty_cells(self):
        empty = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and not self.entries[i][j].get():
                    empty.append((i, j))
        return empty

    def hint(self):
        try:
            if self.hints < 3:
                if not self.empty_cells():
                    messagebox.showinfo("No Empty Cells", "There are no empty cells to provide a hint.")
                    return

                hint = random.choice(self.empty_cells())
                value = self.solved_board[hint[0]][hint[1]]
                self.hints += 1
                messagebox.showinfo("Sudoku Hint",
                                    f"Consider placing {value} in row {hint[0] + 1} and column {hint[1] + 1}.")
            else:
                messagebox.showinfo("No More Hints",
                                    "You have already used all three available hints. Try solving the puzzle on your own!")
        except IndexError:
            messagebox.showerror("Hint Error", "Error in selecting a hint. Please try again.")

    def solve_sudoku(self):
        # Check if all entries are full
        if self.are_all_entries_full():
            # Get the values from the entries
            for i in range(9):
                for j in range(9):
                    if isinstance(self.entries[i][j], tk.Entry):
                        value = self.entries[i][j].get()
                        if value.isdigit() and 1 <= int(value) <= 9:
                            self.board[i][j] = int(value)
                        else:
                            messagebox.showerror("Error", "Invalid input")
                            return
            if self.is_valid_solution(self.board):
                # Display the solved sudoku
                for i in range(9):
                    for j in range(9):
                        if isinstance(self.entries[i][j], tk.Entry):
                            self.entries[i][j].delete(0, tk.END)
                            self.entries[i][j].insert(0, str(self.board[i][j]))
                messagebox.showinfo("Congratulations", "Congratulations, you have solved the Sudoku!")

            else:
                messagebox.showerror("Error", "Invalid solution")
        else:
            messagebox.showinfo("Incomplete Sudoku", "Please fill in all entries before solving.")

    def are_all_entries_full(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.entries[i][j], tk.Entry) and not self.entries[i][j].get():
                    return False
        return True

    def is_valid_solution(self, board):
        for i in range(9):                # Check rows and columns
            row_set = set()
            col_set = set()
            for j in range(9):
                if board[i][j] in row_set or board[j][i] in col_set:
                    return False
                row_set.add(board[i][j])
                col_set.add(board[j][i])
        for i in range(0, 9, 3):           # Check 3x3 subgrids
            for j in range(0, 9, 3):
                subgrid_set = set()
                for k in range(3):
                    for l in range(3):
                        if board[i+k][j+l] in subgrid_set:
                            return False
                        subgrid_set.add(board[i+k][j+l])
        return True
