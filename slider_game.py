import tkinter as tk
import random
import numpy as np

# "Sliding Puzzle is a classic puzzle game where the goal is to arrange the numbered tiles in ascending order by sliding them into the empty space. 
# It challenges your logic and problem-solving skills, and the fewer moves you make, the better your score. Can you solve the puzzle and win the game?"

class SlidingPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle")
        self.root.geometry("500x500")

        # Create a canvas for the game board
        self.canvas = tk.Canvas(self.root, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        # Create a "New Game" button
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=1, column=0, padx=20, pady=10)

        # Create a "Quit" button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=1, column=1, padx=20, pady=10)

        # Create an "Info" button
        self.info_button = tk.Button(self.root, text="Info", command=self.show_info)
        self.info_button.grid(row=1, column=2, padx=20, pady=10)

        # Initialize the game board as a 3x3 grid
        self.board = np.zeros((3, 3), dtype=int)
        self.empty_tile = None
        self.move_count = 0  # Move counter
        self.create_board()

    def create_board(self):
        # Define the initial tile values
        # values = [1, 2, 3, 4, 5, 6, 7, 0, 8]
        values = list(range(9))
        random.shuffle(values)

        # Initialize the index to track the current value
        idx = 0

        # Populate the game board with initial tile values
        for i in range(3):
            for j in range(3):
                self.board[i][j] = values[idx]
                if values[idx] == 0:
                    self.empty_tile = (i, j)
                idx += 1

        # Create visual representation of the game board
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                tile = tk.Canvas(self.canvas, width=133, height=133, bg="white")
                tile.create_text(67, 67, text=str(value), font=("Arial", 24))
                tile.grid(row=i, column=j)
                tile.bind("<Button-1>", lambda event, i=i, j=j: self.tile_click(i, j))
                if value == 0:
                    self.empty_tile_canvas = tile

    def new_game(self):
        # Reset the game board for a new game
        for i in range(3):
            for j in range(3):
                self.board[i][j] = 0
        self.empty_tile = None
        for tile in self.canvas.winfo_children():
            tile.destroy()
        self.move_count = 0
        self.create_board()

    def tile_click(self, i, j):
        # Check if the clicked tile is adjacent to the empty tile
        if self.is_adjacent(self.empty_tile, (i, j)):
            # Swap the clicked tile with the empty tile
            self.swap_tiles(self.empty_tile, (i, j))
            self.empty_tile = (i, j)
            self.move_count += 1

            # Check if the game is over
            if self.is_game_over():
                self.show_congratulations()

    def is_adjacent(self, pos1, pos2):
        # Check if two positions are adjacent
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def swap_tiles(self, pos1, pos2):
        # Swap the values of two tiles
        self.board[pos1] = self.board[pos2]
        self.board[pos2] = 0
        self.update_tile(pos1)
        self.update_tile(pos2)

    def update_tile(self, pos):
        # Update the visual representation of a tile
        i, j = pos
        value = self.board[i][j]
        tile = self.canvas.grid_slaves(row=i, column=j)[0]
        tile.delete("all")
        tile.create_text(67, 67, text=str(value), font=("Arial", 24))

    def is_game_over(self):
        # Check if the game is over by comparing the current board with the target board
        target_board = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        return np.array_equal(self.board, target_board)

    def show_info(self):
        # Display game rules and instructions
        info = """
        Sliding Puzzle Game Rules:
        1. Your goal is to arrange tiles in ascending order from 1 to 8, leaving an empty space (0).
        2. You can slide tiles into the empty space to make a move.
        3. Click on a tile to slide it into the empty space.
        4. Click "New Game" to start a new game.
        5. Click "Quit" to exit the game.
        """
        info_window = tk.Toplevel(self.root)
        info_window.title("Game Rules")
        info_text = tk.Text(info_window, wrap=tk.WORD)
        info_text.insert(tk.END, info)
        info_text.pack()

    def show_congratulations(self):
        # Display a congratulatory message when the game is completed
        congratulations = f"Congratulations!\nYou completed the game in {self.move_count} moves."
        self.move_count = 0
        congrats_window = tk.Toplevel(self.root)
        congrats_window.title("Congratulations!")
        congrats_window.geometry("400x200")
        congrats_label = tk.Label(congrats_window, text=congratulations, font=("Arial", 16))
        congrats_label.pack()

    def print_board(self):
        for i in range(3):
            print(self.board[i])

if __name__ == "__main__":
    root = tk.Tk()
    app = SlidingPuzzleApp(root)
    root.mainloop()
