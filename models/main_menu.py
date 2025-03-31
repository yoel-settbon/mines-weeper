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
        
        # Fonts
        self.title_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 14)
        
        # Couleurs
        self.bg_color = (192, 192, 192)
        self.border_light = (255, 255, 255)
        self.border_dark = (128, 128, 128)
        self.text_color = (0, 0, 0)
        
        # Éléments d'interface
        input_width = 200
        input_height = 30
        button_width = 150
        button_height = 40
        
        # Créer une boîte d'entrée pour le nom
        self.input_box = InputBox(
            x=(self.width - input_width) // 2,
            y=120,
            width=input_width,
            height=input_height,
            placeholder="Entrez votre nom"
        )
        
        # Créer un bouton pour démarrer le jeu
        self.play_button = MenuButton(
            x=(self.width - button_width) // 2,
            y=170,
            width=button_width,
            height=button_height,
            text="Jouer"
        )
        
        # Charger les scores
        self.score_manager = ScoreManager()
        
    def draw_scores(self):
        # Dessiner le titre des scores
        title_text = self.subtitle_font.render("Meilleurs scores", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 230))
        self.screen.blit(title_text, title_rect)
        
        # Récupérer les meilleurs scores
        scores = self.score_manager.get_top_scores()
        
        # Dessiner un cadre pour les scores
        scores_rect = pygame.Rect(50, 250, self.width - 100, 120)
        pygame.draw.rect(self.screen, (255, 255, 255), scores_rect)
        
        # Dessiner une bordure 3D
        pygame.draw.line(self.screen, (64, 64, 64), (scores_rect.x, scores_rect.y), (scores_rect.right-1, scores_rect.y), 1)
        pygame.draw.line(self.screen, (64, 64, 64), (scores_rect.x, scores_rect.y), (scores_rect.x, scores_rect.bottom-1), 1)
        pygame.draw.line(self.screen, (223, 223, 223), (scores_rect.x+1, scores_rect.bottom-1), (scores_rect.right-1, scores_rect.bottom-1), 1)
        pygame.draw.line(self.screen, (223, 223, 223), (scores_rect.right-1, scores_rect.y+1), (scores_rect.right-1, scores_rect.bottom-1), 1)
        
        # Dessiner l'en-tête
        pygame.draw.line(self.screen, (0, 0, 0), (scores_rect.x, scores_rect.y + 25), (scores_rect.right, scores_rect.y + 25), 1)
        name_text = self.text_font.render("Nom", True, self.text_color)
        time_text = self.text_font.render("Temps", True, self.text_color)
        self.screen.blit(name_text, (scores_rect.x + 10, scores_rect.y + 5))
        self.screen.blit(time_text, (scores_rect.right - 60, scores_rect.y + 5))
        
        # Afficher les scores
        for i, score in enumerate(scores):
            y_pos = scores_rect.y + 30 + i * 20
            
            # Nom
            name = score["name"] if score["name"] else "Anonyme"
            name_text = self.text_font.render(name, True, self.text_color)
            self.screen.blit(name_text, (scores_rect.x + 10, y_pos))
            
            # Temps
            seconds = score["time"]
            minutes = seconds // 60
            seconds %= 60
            time_text = self.text_font.render(f"{minutes:02d}:{seconds:02d}", True, self.text_color)
            self.screen.blit(time_text, (scores_rect.right - 60, y_pos))
        
        # Si pas de scores, afficher un message
        if not scores:
            no_scores_text = self.text_font.render("Aucun score pour le moment", True, self.text_color)
            no_scores_rect = no_scores_text.get_rect(center=(scores_rect.centerx, scores_rect.centery))
            self.screen.blit(no_scores_text, no_scores_rect)
    
    def draw(self):
        # Dessiner le fond
        self.screen.fill(self.bg_color)
        
        # Dessiner le titre
        title_text = self.title_font.render("Mines Weeper", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Dessiner les éléments d'interface
        self.input_box.draw(self.screen)
        self.play_button.draw(self.screen)
        
        # Dessiner les scores
        self.draw_scores()
    
    def run(self):
        player_name = ""
        should_start = False
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # Gérer les événements de la boîte d'entrée
                self.input_box.handle_event(event)
                
                # Gérer les clics sur le bouton de jeu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_click(event.pos):
                        player_name = self.input_box.get_text()
                        if not player_name:
                            player_name = "Anonyme"
                            
                        should_start = True
                        self.running = False
            
            # Mettre à jour les éléments d'interface
            self.input_box.update()
            self.play_button.update(mouse_pos)
            
            # Dessiner l'interface
            self.draw()
            
            # Mettre à jour l'écran
            pygame.display.flip()
            self.clock.tick(60)
        
        return player_name, should_start