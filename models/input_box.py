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
        self.max_length = 12

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_length and event.unicode.isprintable():
                        self.text += event.unicode
                
                if self.text:
                    self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
                else:
                    self.txt_surface = self.font.render(self.placeholder, True, (180, 180, 180))
        
        return False

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
        pygame.draw.line(screen, (64, 64, 64), (self.rect.x, self.rect.y), (self.rect.right-1, self.rect.y), 1)
        pygame.draw.line(screen, (64, 64, 64), (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom-1), 1)
        pygame.draw.line(screen, (223, 223, 223), (self.rect.x+1, self.rect.bottom-1), (self.rect.right-1, self.rect.bottom-1), 1)
        pygame.draw.line(screen, (223, 223, 223), (self.rect.right-1, self.rect.y+1), (self.rect.right-1, self.rect.bottom-1), 1)
        
        if self.text:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
            
            if self.active and self.cursor_visible:
                cursor_pos = self.rect.x + 5 + self.txt_surface.get_width()
                pygame.draw.line(screen, (0, 0, 0), 
                                (cursor_pos, self.rect.y + 5),
                                (cursor_pos, self.rect.y + self.rect.h - 5), 1)
        else:
            placeholder_surface = self.font.render(self.placeholder, True, (180, 180, 180))
            screen.blit(placeholder_surface, (self.rect.x + 5, self.rect.y + (self.rect.h - placeholder_surface.get_height()) // 2))
            
            if self.active and self.cursor_visible:
                pygame.draw.line(screen, (0, 0, 0), 
                                (self.rect.x + 5, self.rect.y + 5),
                                (self.rect.x + 5, self.rect.y + self.rect.h - 5), 1)

    def get_text(self):
        return self.text