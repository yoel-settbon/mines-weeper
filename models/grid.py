import random
import time

class Board:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.cell_states = [[0 for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.win = False
        self.start_time = None
        self.elapsed_time = 0
        self.first_click = True
        self.paused_time = 0
        self.game_started = False
        self.generated = False

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        if self.game_over or self.win:
            return self.elapsed_time
        self.elapsed_time = int(time.time() - self.start_time - self.paused_time)
        return self.elapsed_time
        
    def start_timer(self):
        if self.first_click:
            self.start_time = time.time()
            self.game_started = True

    def generate_board(self, first_row, first_col):
        while True:
            # Reinitializes the grid
            self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            positions = [
                (r, c)
                for r in range(self.rows)
                for c in range(self.cols)
                if not (r == first_row and c == first_col)
            ]
            random.shuffle(positions)

            mines_placed = 0
            for r, c in positions:
                if mines_placed < self.mines:
                    self.grid[r][c] = -1
                    mines_placed += 1

            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] != -1:
                        self.grid[row][col] = self.count_adjacent_mines(row, col)
            # The clicked case has to be > 0 to avoid the cascade
            if self.grid[first_row][first_col] > 0:
                break

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(self.rows, row+2)):
            for c in range(max(0, col-1), min(self.cols, col+2)):
                if self.grid[r][c] == -1:
                    count += 1
        return count

    def reveal(self, row, col):
        if self.first_click:
            self.generate_board(row, col)
            self.start_timer()
            self.first_click = False

        if self.cell_states[row][col] == 1:
            return
        
        if self.revealed[row][col]:
            return

        self.revealed[row][col] = True

        if self.grid[row][col] == 0:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if not self.revealed[r][c] and self.cell_states[r][c] != 1:
                        self.reveal(r, c)
        
        if self.grid[row][col] == -1:
            self.game_over = True
            self.reveal_all_mines()

        # Check victory after revelation
        if not self.game_over:
            if self.check_win():
                self.win = True

    def reveal_all_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == -1:
                    self.revealed[row][col] = True
       
    def toggle_flag(self, row, col):
        if not self.revealed[row][col]:
            self.cell_states[row][col] = (self.cell_states[row][col] + 1) % 3
    
    def get_remaining_mines(self):
        flagged = sum(1 for row in self.cell_states for state in row if state == 1)
        return self.mines - flagged
    
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.grid[row][col] == -1 and self.cell_states[row][col] != 1) or \
                   (self.grid[row][col] != -1 and not self.revealed[row][col]):
                    return False
        self.win = True
        return True
