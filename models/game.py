import pygame
from models.grid import Board
from models.utilities import UI
from models.popup import Popup

class Game:
    def __init__(self):
        self.width = 300
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mines Weeper")
        
        self.board = Board(rows=9, cols=9, mines=10)
        self.ui = UI(self.screen, self.board)
        self.clock = pygame.time.Clock()
        
        self.game_over = False
        self.win = False
        self.popup = None 

    def run(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.popup:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = self.popup.handle_click(event.pos)
                        if result == "restart":
                            self.__init__()
                            continue
                        elif result == "quit":
                            running = False
                else: 
                    if not self.game_over and not self.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.handle_left_click(event.pos)
                            elif event.button == 3:
                                self.handle_right_click(event.pos)
            
            self.screen.fill((192, 192, 192))
            self.ui.draw()
            
            if (self.board.game_over or self.board.win) and not self.popup:
                message = "You WIN !" if self.board.win else "You LOSE !"
                self.popup = Popup(self.screen, message)
            
            if self.popup:
                self.popup.draw()
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def handle_left_click(self, pos):
        cell = self.ui.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if not self.board.revealed[row][col] and self.board.cell_states[row][col] != 1:
                self.board.reveal(row, col)
                if self.board.grid[row][col] == -1:
                    self.board.game_over = True
                    self.board.reveal_all_mines()
                elif self.board.check_win():
                    print(self.board.elapsed_time())
                    self.board.win = True
    
    def handle_right_click(self, pos):
        if not self.game_over and not self.win:
            cell = self.ui.get_cell_from_pos(pos)
            if cell:
                row, col = cell
                if not self.board.revealed[row][col]:
                    self.board.toggle_flag(row, col)