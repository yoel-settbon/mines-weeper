import random
import pygame


from Game.cell import Cell


class Grid:
    def __init__(self, width, height, cell_size, cell_num, mines_count, shift):
        self.width = width
        self.height = height
        
        self.cell_size = cell_size
        self.cell_num = cell_num
        self.mines_count = mines_count
        self.shift = shift
        self.cells = [[Cell(x, y, self.cell_size, self.shift) for y in range(0, self.cell_num)] for x in range(0, self.cell_num)]
        self.mines_placed = False


    def place_mines(self, safe_x, safe_y):
        mines_to_place = self.mines_count
        while mines_to_place > 0:
            x = random.randint(0, self.cell_num - 1)
            y = random.randint(0, self.cell_num - 1)
            if (x, y) != (safe_x, safe_y) and not self.cells[x][y].is_mine:
                self.cells[x][y].is_mine = True
                mines_to_place -= 1


        # Update the mines around count
        for x in range(self.cell_num):
            for y in range(self.cell_num):
                self.cells[x][y].mines_around = self.count_mines_around(x, y)


    def count_mines_around(self, x, y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    if self.cells[nx][ny].is_mine:
                        count += 1
        return count


    def reveal_cell(self, x, y):
        if not self.mines_placed:
            self.place_mines(x, y)
            self.mines_placed = True
        if self.cells[x][y].reveal():
            return True  # Hit a mine
        if self.cells[x][y].mines_around == 0:
            self.reveal_adjacent(x, y)
        return False


    def reveal_adjacent(self, x, y):
        stack = [(x, y)] 
        while stack:
            cx, cy = stack.pop()
            
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                        cell = self.cells[nx][ny]
                        if not cell.is_revealed and not cell.is_mine:
                            cell.reveal()


                            if cell.mines_around == 0:
                                stack.append((nx, ny)) 




    def check_win_condition(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True


    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()


    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
