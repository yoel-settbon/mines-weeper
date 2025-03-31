import pygame

class InputBox:
    def __init__(self, x, y, width, height, text='', placeholder='Entrez votre nom'):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color(128, 128, 128)
        self.color_active = pygame.Color(0, 0, 128)
        self.color = self.color_inactive
        self.text = text
        self.placeholder = placeholder
        self.font = pygame.font.SysFont('Arial', 14)
        self.txt_surface = self.font.render(text, True, (0, 0, 0))
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 12  # Longueur maximale du texte

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si l'utilisateur clique sur la boîte, la rendre active
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive
            # Changer la couleur de la boîte d'entrée
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Désactiver la boîte lors de l'appui sur Entrée
                    self.active = False
                    self.color = self.color_inactive
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Ajouter un caractère si la touche est valide et que la longueur maximale n'est pas atteinte
                    if len(self.text) < self.max_length and event.unicode.isprintable():
                        self.text += event.unicode
                
                # Mettre à jour la surface du texte
                if self.text:
                    self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
                else:
                    # Afficher le placeholder si le texte est vide
                    self.txt_surface = self.font.render(self.placeholder, True, (180, 180, 180))
        
        return False

    def update(self):
        # Ajuster la largeur du rectangle si le texte est trop long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        
        # Mettre à jour le curseur clignotant
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Changer la visibilité du curseur toutes les 30 frames
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        # Dessiner le fond de la boîte d'entrée
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
        # Dessiner le bord 3D style Windows 95/98
        pygame.draw.line(screen, (64, 64, 64), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 1)
        pygame.draw.line(screen, (64, 64, 64), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 1)
        pygame.draw.line(screen, (223, 223, 223), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 1)
        pygame.draw.line(screen, (223, 223, 223), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 1)
        
        # Dessiner le texte ou le placeholder
        if self.text:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
            
            # Dessiner le curseur clignotant si la boîte est active
            if self.active and self.cursor_visible:
                cursor_pos = self.rect.x + 5 + self.txt_surface.get_width()
                pygame.draw.line(screen, (0, 0, 0), 
                                (cursor_pos, self.rect.y + 5),
                                (cursor_pos, self.rect.y + self.rect.h - 5), 1)
        else:
            # Afficher le placeholder en gris
            placeholder_surface = self.font.render(self.placeholder, True, (180, 180, 180))
            screen.blit(placeholder_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - placeholder_surface.get_height()) // 2))
            
            # Dessiner le curseur clignotant si la boîte est active
            if self.active and self.cursor_visible:
                pygame.draw.line(screen, (0, 0, 0), 
                                (self.rect.x + 5, self.rect.y + 5),
                                (self.rect.x + 5, self.rect.y + self.rect.h - 5), 1)

    def get_text(self):
        return self.text