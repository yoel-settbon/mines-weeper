import pygame
from models.grid import Board
from models.utilities import UI

class Game:
    def __init__(self):
        self.width = 300
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Démineur")
        
        self.board = Board(rows=9, cols=9, mines=10)
        self.ui = UI(self.screen, self.board)
        self.clock = pygame.time.Clock()
        
        self.game_over = False
        self.win = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if not self.game_over and not self.win:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Clic gauche
                            self.handle_left_click(event.pos)
                        elif event.button == 3:  # Clic droit
                            self.handle_right_click(event.pos)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
            
            self.screen.fill((192, 192, 192))
            self.ui.draw()
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
                    self.reveal_all_mines()
                elif self.board.check_win():
                    self.board.win = True
    
    def handle_right_click(self, pos):
        if not self.game_over and not self.win:
            cell = self.ui.get_cell_from_pos(pos)
            if cell:
                row, col = cell
                if not self.board.revealed[row][col]:
                    self.board.toggle_flag(row, col)