import pygame
from models.input_box import InputBox
from models.menu_button import MenuButton
from models.score_manager import ScoreManager

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.width, self.height = screen.get_size()
        
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 14)
        
        self.bg_color = (192, 192, 192)
        self.border_light = (255, 255, 255)
        self.border_dark = (128, 128, 128)
        self.text_color = (0, 0, 0)
        
        input_width = 200
        input_height = 30
        button_width = 150
        button_height = 40
        
        # Input box pour le nom du joueur
        self.input_box = InputBox(
            x=(self.width - input_width) // 2,
            y=120,
            width=input_width,
            height=input_height,
            placeholder="Entrez votre nom"
        )
        
        # Bouton Jouer
        self.play_button = MenuButton(
            x=(self.width - button_width) // 2,
            y=170,
            width=button_width,
            height=button_height,
            text="Jouer"
        )
        
        # Boutons de difficulté (en horizontal)
        small_button_width = 80
        small_button_height = 30
        button_spacing = 10
        
        total_width = (small_button_width * 3) + (button_spacing * 2)
        start_x = (self.width - total_width) // 2
        
        self.difficulty_buttons = [
            MenuButton(
                x=start_x,
                y=220,
                width=small_button_width,
                height=small_button_height,
                text="Facile"
            ),
            MenuButton(
                x=start_x + small_button_width + button_spacing,
                y=220,
                width=small_button_width,
                height=small_button_height,
                text="Moyen"
            ),
            MenuButton(
                x=start_x + (small_button_width + button_spacing) * 2,
                y=220,
                width=small_button_width,
                height=small_button_height,
                text="Difficile"
            )
        ]
        
        # Niveau de difficulté par défaut
        self.selected_difficulty = "Facile"
        
        self.score_manager = ScoreManager()
        
    def draw_scores(self):
        title_text = self.subtitle_font.render(f"Meilleurs scores ({self.selected_difficulty})", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 270))
        self.screen.blit(title_text, title_rect)
        
        scores = self.score_manager.get_top_scores(self.selected_difficulty)
        
        scores_rect = pygame.Rect(50, 290, self.width - 100, 100)
        pygame.draw.rect(self.screen, (255, 255, 255), scores_rect)
        
        pygame.draw.line(self.screen, (64, 64, 64), (scores_rect.x, scores_rect.y), (scores_rect.right-1, scores_rect.y), 1)
        pygame.draw.line(self.screen, (64, 64, 64), (scores_rect.x, scores_rect.y), (scores_rect.x, scores_rect.bottom-1), 1)
        pygame.draw.line(self.screen, (223, 223, 223), (scores_rect.x+1, scores_rect.bottom-1), (scores_rect.right-1, scores_rect.bottom-1), 1)
        pygame.draw.line(self.screen, (223, 223, 223), (scores_rect.right-1, scores_rect.y+1), (scores_rect.right-1, scores_rect.bottom-1), 1)
        
        pygame.draw.line(self.screen, (0, 0, 0), (scores_rect.x, scores_rect.y + 25), (scores_rect.right, scores_rect.y + 25), 1)
        name_text = self.text_font.render("Nom", True, self.text_color)
        time_text = self.text_font.render("Temps", True, self.text_color)
        self.screen.blit(name_text, (scores_rect.x + 10, scores_rect.y + 5))
        self.screen.blit(time_text, (scores_rect.right - 60, scores_rect.y + 5))
        
        for i, score in enumerate(scores):
            y_pos = scores_rect.y + 30 + i * 20
            
            name = score["name"] if score["name"] else "Anonyme"
            name_text = self.text_font.render(name, True, self.text_color)
            self.screen.blit(name_text, (scores_rect.x + 10, y_pos))
            
            seconds = score["time"]
            minutes = seconds // 60
            seconds %= 60
            time_text = self.text_font.render(f"{minutes:02d}:{seconds:02d}", True, self.text_color)
            self.screen.blit(time_text, (scores_rect.right - 60, y_pos))
        
        if not scores:
            no_scores_text = self.text_font.render("Aucun score pour le moment", True, self.text_color)
            no_scores_rect = no_scores_text.get_rect(center=(scores_rect.centerx, scores_rect.centery))
            self.screen.blit(no_scores_text, no_scores_rect)
    
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Titre du jeu
        title_text = self.title_font.render("Mines Weeper", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Dessiner l'input box et le bouton jouer
        self.input_box.draw(self.screen)
        self.play_button.draw(self.screen)
        

        
        # Dessiner les boutons de difficulté
        for i, button in enumerate(self.difficulty_buttons):
            # Mettre en surbrillance le bouton sélectionné
            if ["Facile", "Moyen", "Difficile"][i] == self.selected_difficulty:
                # Si tu as ajouté l'attribut highlight à MenuButton
                if hasattr(button, 'highlight'):
                    button.highlight = True
                # Sinon, tu peux simplement changer la couleur du texte
                else:
                    button.text_color = (0, 0, 255)  # Bleu pour le bouton sélectionné
            else:
                if hasattr(button, 'highlight'):
                    button.highlight = False
                else:
                    button.text_color = (0, 0, 0)  # Noir pour les autres boutons
                    
            button.draw(self.screen)
        
        # Afficher les scores
        self.draw_scores()
    
    def run(self):
        player_name = ""
        should_start = False
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                self.input_box.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_click(event.pos):
                        player_name = self.input_box.get_text()
                        if not player_name:
                            player_name = "Anonyme"
                            
                        should_start = True
                        self.running = False
                    
                    # Vérifier les clics sur les boutons de difficulté
                    for i, button in enumerate(self.difficulty_buttons):
                        if button.check_click(event.pos):
                            self.selected_difficulty = ["Facile", "Moyen", "Difficile"][i]
            
            self.input_box.update()
            self.play_button.update(mouse_pos)
            
            # Mettre à jour les boutons de difficulté
            for button in self.difficulty_buttons:
                button.update(mouse_pos)
            
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return player_name, should_start, self.selected_difficulty