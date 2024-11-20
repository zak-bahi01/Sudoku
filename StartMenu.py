import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from SudokuGame import SudokuGame


class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Start Menu")
        self.create_start_menu()

    def create_start_menu(self):
        # Set the geometry of the root window to 300x300 and center it on the screen
        self.root.geometry("300x300+{}+{}".format(self.root.winfo_screenwidth() // 2 - 150,
                                                  self.root.winfo_screenheight() // 2 - 150))

        # Increase the font size for the label
        ttk.Label(self.root, text="Sudoku Game", font=("Arial", 20)).pack(pady=20)

        # Create a custom style for buttons and configure the font within that style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14))

        # Use the custom style for the New Game button
        new_game_button = ttk.Button(self.root, text="New Game", command=self.start_new_game, style="TButton")
        new_game_button.pack(pady=15)

        # Use the custom style for the Load Game button
        load_game_button = ttk.Button(self.root, text="Load Game", command=self.load_game, style="TButton")
        load_game_button.pack(pady=15)

    def start_new_game(self):
        self.root.destroy()  # Close the start menu window
        difficulty_root = tk.Tk()
        difficulty_root.geometry("300x300+{}+{}".format(difficulty_root.winfo_screenwidth() // 2 - 150,
                                                        difficulty_root.winfo_screenheight() // 2 - 150))
        difficulty_root.title("Difficulty Selection")

        ttk.Label(difficulty_root, text="Select Difficulty", font=("Arial", 14)).pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TMenubutton", font=("Arial", 12))

        difficulty_var = tk.StringVar(value="Easy")
        difficulty_options = ttk.OptionMenu(difficulty_root, difficulty_var,
                                            "Easy", "Easy", "Medium", "Hard")
        difficulty_options.configure(width=10, style="TMenubutton")  # Apply the custom style
        difficulty_options.pack(pady=10)

        start_game_button = ttk.Button(difficulty_root, text="Start Game",
                                       command=lambda: self.start_game_with_difficulty(difficulty_root,
                                                                                       difficulty_var.get()),
                                       style="TButton")
        start_game_button.pack(pady=10)

        difficulty_root.mainloop()

    def start_game_with_difficulty(self, difficulty_root, selected_difficulty):
        difficulty_root.destroy()  # Close the difficulty selection window

        game_root = tk.Tk()
        sudoku_game = SudokuGame(game_root, difficulty_level=selected_difficulty)
        game_root.mainloop()

    def load_game(self):
        filename = "sudoku_savegame.pkl"
        try:
            with open(filename, 'rb') as file:
                saved_data = pickle.load(file)
                self.root.destroy()  # Close the start menu window
                game_root = tk.Tk()
                sudoku_game = SudokuGame(game_root, saved=list(saved_data['board']))
                for i in range(9):
                    for j in range(9):
                        if isinstance(sudoku_game.entries[i][j], tk.Entry):
                            sudoku_game.entries[i][j].delete(0, tk.END)
                            sudoku_game.entries[i][j].insert(0, saved_data['entries'][i][j])
                game_root.mainloop()
        except FileNotFoundError:
            messagebox.showinfo("Information", "No saved game found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading game: {e}")