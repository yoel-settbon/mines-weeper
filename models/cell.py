import pygame
from views.utilities import *

class Cell:
    def __init__(self, x, y, size, shift):
        self.x = x
        self.y = y
        self.size = size
        self.shift = shift
        self.is_mine = False
        self.revealed = False
        self.is_flagges = False
        self.mines_around = 0
        self.font = pygame.font.SysFont(None, 36)
    
    def draw(self, screen):
        rect = pygame.Rect(self.x * self.size, self.y * self.size + self.shift, self.size, self.size)
        if self.is_revealed:
            if self.is_mine:
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.circle(screen, BLACK, rect.center, self.size // 4)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                if self.mines_around > 0:
                    text = self.font.render(str(self.mines_around), True, BLUE)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, DARK_GRAY if self.is_flagged else GRAY, rect)
        
        pygame.draw.rect(screen, BLACK, rect, 1)
    
    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
    
    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return self.is_mine
        return False