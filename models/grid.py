import random
from models.cell import Cell

class Grid :
    def __init__(self, width, height, cell_size, cell_num, mines_count, shift):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cell_num = cell_num
        self.mines_count = mines_count
        self.shift = shift
        self.cells = [[Cell(x, y, self.cell_size, self.shift) for y in range(0, self.cell_num)] for x in range (0, self.cell_num)]
        self.mines_place = False

    def place_mines(self, safe_x, safe_y):
        mines_to_place = self.mines_count
        while mines_to_place > 0 :
            x = random.randint(0, self.cell_num -1)
            y = random.randint(0, self.cell_num - 1)
            if (x, y) != (safe_x, safe_y) and not self.cells[x][y].mine :
                self.cells[x][y].mine = True
                mines_to_place -= 1

        for x in range(self.cell_num):
            for y in range(self.cell_num):
                self.cells[x][y].mines_arround = self.count_mines_around(x, y)

    def count_mines_around(self, x, y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num :
                    if self.cells[nx][ny].mine :
                        count += 1
        return count
    
    def revealed_cell(self, x, y):
        if not self.mines_place :
            self.place_mines(x, y)
            self.mines_place = True
        if self.cells[x][y].mines_arround == 0 :
            self.reveal_adjacent(x, y)
        return False
    
    def reveal_adjacent(self, x, y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num :
                    if not self.cells[nx][ny].revealed and not self.cells[nx][ny].mine :
                        self.cells[nx][ny].revealed = True
                        if self.cells[nx][ny].mines_arround == 0 :
                            self.reveal_adjacent(nx, ny)


    def check_win_condition(self):
        for row in self.cells :
            for cell in row :
                if not cell.mine and not cell.revealed:
                    return False
    
    def reveal_all_mines(self):
        for row in self.cells :
            for cell in row :
                if cell.mine :
                    cell.reveal()
    
    def draw(self, screen):
        for row in self.cells :
            for cell in row :
                cell.draw(screen)