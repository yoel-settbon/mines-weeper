import pygame
from models.grid import Board
from models.utilities import UI
from models.popup import Popup
from models.score_manager import ScoreManager

class Game:
    def __init__(self, player_name="Player"):
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
        self.player_name = player_name
        self.score_manager = ScoreManager()
        
        self.return_to_menu = False

    def run(self):
        running = True
        while running and not self.return_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.return_to_menu = False
                
                if self.popup:

                    if event.type == pygame.MOUSEMOTION:
                        self.popup.check_hover(event.pos)
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = self.popup.handle_click(event.pos)
                        if result == "restart":

                            self.__init__(self.player_name)
                        elif result == "quit":

                            running = False
                            self.return_to_menu = False
                        elif result == "menu":

                            running = False
                            self.return_to_menu = True
                else: 
                    if not self.game_over and not self.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Clic gauche
                                self.handle_left_click(event.pos)
                            elif event.button == 3:  # Clic droit
                                self.handle_right_click(event.pos)
            
            self.screen.fill((192, 192, 192))
            self.ui.draw()
            
            if (self.board.game_over or self.board.win) and not self.popup:
                if self.board.win:
                    final_time = self.board.get_elapsed_time()
                    is_high_score = self.score_manager.is_high_score(final_time)
                    
                    if is_high_score:
                        self.score_manager.add_score(self.player_name, final_time)
                        message = f"You WIN! Your time: {final_time} seconds. New high score!"
                    else:
                        message = f"You WIN! Your time: {final_time} seconds."
                else:
                    message = "You LOSE!"
                
                self.popup = Popup(self.screen, message, show_menu_button=True)
            
            if self.popup:
                self.popup.draw()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        return self.return_to_menu
    
    def handle_left_click(self, pos):
        cell = self.ui.get_cell_from_pos(pos)
        if cell:
            self.board.start_timer()
            
            row, col = cell
            if not self.board.revealed[row][col] and self.board.cell_states[row][col] != 1:
                self.board.reveal(row, col)
                if self.board.grid[row][col] == -1:
                    self.board.game_over = True
                    self.board.reveal_all_mines()
                elif self.board.check_win():
                    self.board.win = True
    
    def handle_right_click(self, pos):
        if not self.game_over and not self.win:
            cell = self.ui.get_cell_from_pos(pos)
            if cell:
                self.board.start_timer()
                
                row, col = cell
                if not self.board.revealed[row][col]:
                    self.board.toggle_flag(row, col)