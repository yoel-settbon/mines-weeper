import pygame
from models.utilities import *

class Cell :
    def __init__(self, x, y, size, shift):
        self.x = x
        self.y = y
        self.size = size
        self.shift = shift
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.mines_arround = 0
        self.font = pygame.font.SysFont("Arial", 36)

    def draw(self, screen):
        rect = pygame.Rect(self.x * self.size, self.y * self.size + self.shift, self.size, self.size)
        if self.revealed :
            if self.mine :
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.circle(screen, BLACK, rect.center, self.size // 4)
            else :
                pygame.draw.rect(screen, WHITE, rect)
                if self.mines_arround > 0 :
                    text = self.font.render(str(self.mines_arround), True, BLUE)
                    text_rect = text.get_rect(center = rect.center)
                    screen.blit(text, text_rect)
        else :
            pygame.draw.rect(screen, DARK_GRAY if self.flagged else GRAY, rect)
        
        pygame.draw.rect(screen, BLACK, rect, 1)

    def toggle_flag(self):
        if not self.revealed :
            self.flagged = not self.flagged

    def revealed(self):
        if not self.flagged :
            self.revealed = True
            return self.mine
        return False