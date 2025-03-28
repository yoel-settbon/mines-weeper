import pygame

class Popup:
    def __init__(self, screen, message):
        self.screen = screen
        self.message = message
        self.width = 300
        self.height = 150
        self.rect = pygame.Rect(
            (screen.get_width() - self.width) // 2,
            (screen.get_height() - self.height) // 2,
            self.width,
            self.height
        )
        self.font_large = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 14)
        
        button_width = 100
        self.restart_button = pygame.Rect(
            self.rect.x + 30,
            self.rect.y + 100,
            button_width,
            24
        )
        self.quit_button = pygame.Rect(
            self.rect.x + 170,
            self.rect.y + 100,
            button_width,
            24
        )

        self.icon = pygame.Surface((40, 40), pygame.SRCALPHA)
        if "Win" in message :
            pygame.draw.circle(self.icon, (0, 200, 0), (20, 20), 18)
            pygame.draw.line(self.icon, (255, 255, 255), (12, 20), (18, 26), 4)
            pygame.draw.line(self.icon, (255, 255, 255), (18, 26), (28, 14), 4)
        else:
            pygame.draw.circle(self.icon, (200, 0, 0), (20, 20), 18)
            pygame.draw.line(self.icon, (255, 255, 255), (12, 12), (28, 28), 4)
            pygame.draw.line(self.icon, (255, 255, 255), (28, 12), (12, 28), 4)
    
    def draw(self):
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.screen.blit(s, (0, 0))
        
        pygame.draw.rect(self.screen, (192, 192, 192), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        
        title_bar = pygame.Rect(self.rect.x, self.rect.y, self.width, 20)
        pygame.draw.rect(self.screen, (0, 0, 128), title_bar)
        
        pygame.draw.line(self.screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.right, self.rect.y), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom), 2)
        pygame.draw.line(self.screen, (128, 128, 128), (self.rect.x, self.rect.bottom), (self.rect.right, self.rect.bottom), 2)
        pygame.draw.line(self.screen, (128, 128, 128), (self.rect.right, self.rect.y), (self.rect.right, self.rect.bottom), 2) 
        
        title_text = self.font_small.render("Mines Weeper", True, (255, 255, 255))
        self.screen.blit(title_text, (self.rect.x + 5, self.rect.y + 3))
        
        if self.icon:
            self.screen.blit(self.icon, (self.rect.x + 20, self.rect.y + 35))
        
        text_lines = [self.message[i:i+30] for i in range(0, len(self.message), 30)]
        for i, line in enumerate(text_lines):
            text = self.font_small.render(line, True, (0, 0, 0))
            self.screen.blit(text, (self.rect.x + 70, self.rect.y + 40 + i * 20))
        
        self.draw_button(self.restart_button, "Retry")
        self.draw_button(self.quit_button, "Quit")
    
    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
        pygame.draw.line(self.screen, (223, 223, 223), (rect.x, rect.y), (rect.right-1, rect.y), 1)
        pygame.draw.line(self.screen, (223, 223, 223), (rect.x, rect.y), (rect.x, rect.bottom-1), 1)
        pygame.draw.line(self.screen, (64, 64, 64), (rect.x, rect.bottom-1), (rect.right-1, rect.bottom-1), 1)
        pygame.draw.line(self.screen, (64, 64, 64), (rect.right-1, rect.y), (rect.right-1, rect.bottom-1), 1)
        
        pygame.draw.rect(self.screen, (192, 192, 192), rect.inflate(-2, -2))
        
        text_surface = self.font_small.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        if self.restart_button.collidepoint(pos) or self.quit_button.collidepoint(pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return False
    
    def handle_click(self, pos):
        if self.restart_button.collidepoint(pos):
            pygame.time.delay(100)
            return "restart"
        elif self.quit_button.collidepoint(pos):
            pygame.time.delay(100)
            return "quit"
        return None