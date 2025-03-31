import pygame

class MenuButton:
    def __init__(self, x, y, width, height, text, font_size=14):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', font_size)
        self.bg_color = (192, 192, 192)
        self.text_color = (0, 0, 0)
        self.hovered = False
        self.highlight = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        if self.highlight:
            pygame.draw.rect(screen, (160, 160, 220), self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        if self.hovered:
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 2)
        else:
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 2)
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 2)
            pygame.draw.line(screen, (128, 128, 128), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        if self.hovered:
            text_rect.x += 1
            text_rect.y += 1
            
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def check_click(self, pos):
        return self.rect.collidepoint(pos)