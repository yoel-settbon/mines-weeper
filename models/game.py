import pygame
from models.grid import Board
from models.utilities import UI
from models.popup import Popup
from models.score_manager import ScoreManager

class Game:
    def __init__(self, player_name="Player"):
        # Dimensions de l'écran
        self.width = 300
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mines Weeper")
        
        # Initialisation du plateau
        self.board = Board(rows=9, cols=9, mines=10)
        
        # Interface utilisateur
        self.ui = UI(self.screen, self.board)
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.game_over = False
        self.win = False
        self.popup = None
        
        # Nom du joueur
        self.player_name = player_name
        
        # Gestionnaire de scores
        self.score_manager = ScoreManager()
        
        # État pour retourner au menu
        self.return_to_menu = False

    def run(self):
        running = True
        while running and not self.return_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.popup:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = self.popup.handle_click(event.pos)
                        if result == "restart":
                            self.__init__(self.player_name)
                            continue
                        elif result == "quit":
                            # Au lieu de quitter, on retourne au menu
                            self.return_to_menu = True
                            break
                        elif result == "menu":
                            self.return_to_menu = True
                            break
                else: 
                    if not self.game_over and not self.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.handle_left_click(event.pos)
                            elif event.button == 3:
                                self.handle_right_click(event.pos)
            
            self.screen.fill((192, 192, 192))
            self.ui.draw()
            
            # Vérification de fin de partie
            if (self.board.game_over or self.board.win) and not self.popup:
                # En cas de victoire, on enregistre le score
                if self.board.win:
                    final_time = self.board.get_elapsed_time()
                    
                    # Vérifier si c'est un high score avant d'afficher le popup
                    is_high_score = self.score_manager.is_high_score(final_time)
                    
                    if is_high_score:
                        # Ajouter le score
                        self.score_manager.add_score(self.player_name, final_time)
                        message = f"You WIN! Your time: {final_time} seconds. New high score!"
                    else:
                        message = f"You WIN! Your time: {final_time} seconds."
                else:
                    message = "You LOSE!"
                
                # Créer le popup avec un bouton pour retourner au menu
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