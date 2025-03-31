import pygame

class Popup:
    def __init__(self, screen, message, show_menu_button=False):
        self.screen = screen
        self.message = message
        self.width = 300
        self.height = 180 if show_menu_button else 150
        self.rect = pygame.Rect(
            (screen.get_width() - self.width) // 2,
            (screen.get_height() - self.height) // 2,
            self.width,
            self.height
        )
        self.font_large = pygame.font.SysFont('Arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 14)

        button_width = 80
        button_height = 24

        # Adjust button positions depending on menu button presence
        if show_menu_button:
            self.restart_button = pygame.Rect(
                self.rect.x + 20,
                self.rect.y + 100,
                button_width,
                button_height
            )
            self.menu_button = pygame.Rect(
                self.rect.x + (self.width - button_width) // 2,
                self.rect.y + 100,
                button_width,
                button_height
            )
            self.quit_button = pygame.Rect(
                self.rect.x + self.width - 20 - button_width,
                self.rect.y + 100,
                button_width,
                button_height
            )
        else:
            self.restart_button = pygame.Rect(
                self.rect.x + 30,
                self.rect.y + 100,
                button_width,
                button_height
            )
            self.quit_button = pygame.Rect(
                self.rect.x + 170,
                self.rect.y + 100,
                button_width,
                button_height
            )
            self.menu_button = None

        self.show_menu_button = show_menu_button

        self.icon = None
        if "WIN" in message.upper():
            self.icon = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(self.icon, (255, 255, 0), (16, 16), 15)
            pygame.draw.circle(self.icon, (0, 0, 0), (10, 12), 3)
            pygame.draw.circle(self.icon, (0, 0, 0), (22, 12), 3)
            pygame.draw.arc(self.icon, (0, 0, 0), (8, 10, 16, 16), 3.14, 6.28, 2)
        else:
            self.icon = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(self.icon, (255, 0, 0), (16, 16), 15)
            pygame.draw.line(self.icon, (255, 255, 255), (10, 10), (22, 22), 3)
            pygame.draw.line(self.icon, (255, 255, 255), (22, 10), (10, 22), 3)

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
            self.screen.blit(self.icon, (self.rect.x + 15, self.rect.y + 35))

        text_lines = [self.message[i:i+30] for i in range(0, len(self.message), 30)]
        for i, line in enumerate(text_lines):
            text = self.font_small.render(line, True, (0, 0, 0))
            self.screen.blit(text, (self.rect.x + 60, self.rect.y + 40 + i * 20))

        self.draw_button(self.restart_button, "Retry")
        self.draw_button(self.quit_button, "Quit")
        if self.show_menu_button and self.menu_button:
            self.draw_button(self.menu_button, "Menu")

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
        if self.restart_button.collidepoint(pos) or self.quit_button.collidepoint(pos) or (self.menu_button and self.menu_button.collidepoint(pos)):
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
        elif self.menu_button and self.menu_button.collidepoint(pos):
            pygame.time.delay(100)
            return "menu"
        return None
