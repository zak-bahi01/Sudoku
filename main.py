import tkinter as tk
from StartMenu import StartMenu


if __name__ == "__main__":
    start_menu_root = tk.Tk()
    start_menu = StartMenu(start_menu_root)
    start_menu_root.mainloop()
