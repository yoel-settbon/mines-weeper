import pygame

class MenuButton:
    def __init__(self, x, y, width, height, text, font_size=14):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.bg_color = (192, 192, 192)
        self.text_color = (0, 0, 0)
        self.hovered = False
        
    def draw(self, screen):
        # Dessiner le fond du bouton
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Dessiner les bordures 3D style Windows 95/98
        if self.hovered:
            # Bordures enfoncées quand survolé
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 2)
        else:
            # Bordures normales
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 2)
        
        # Dessiner le texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Ajuster le texte si le bouton est survolé (effet d'enfoncement)
        if self.hovered:
            text_rect.x += 1
            text_rect.y += 1
            
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        # Mettre à jour l'état du survol
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def check_click(self, pos):
        # Vérifier si le bouton a été cliqué
        return self.rect.collidepoint(pos)