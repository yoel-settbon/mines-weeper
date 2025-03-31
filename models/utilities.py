import pygame

class UI:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        screen_width, screen_height = screen.get_size()
        max_grid_width = screen_width - 20
        max_grid_height = screen_height - 100

        # Calculate the optimal cell size
        self.cell_size = min(
            max_grid_width // self.board.cols,
            max_grid_height // self.board.rows
        )

        # Calculate offsets to center the grid
        total_grid_width = self.board.cols * self.cell_size
        total_grid_height = self.board.rows * self.cell_size

        self.left_offset = (screen_width - total_grid_width) // 2
        self.top_offset = 80

        self.colors = {
            "hidden": (192, 192, 192),
            "revealed": (200, 200, 200),
            "text": (0, 0, 0),
            "mine": (0, 0, 0),
            "flag": (255, 0, 0),
            "background": (192, 192, 192),
            "border_light": (255, 255, 255),
            "border_dark": (128, 128, 128),
            "numbers": [
                (0, 0, 255),    
                (0, 128, 0),    
                (255, 0, 0),    
                (0, 0, 128),    
                (128, 0, 0),    
                (0, 128, 128),  
                (0, 0, 0),      
                (128, 128, 128) 
            ]
        }

        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self):
        self.draw_top_panel()
        self.draw_grid()

    def draw_top_panel(self):
        pygame.draw.rect(
            self.screen, 
            (192, 192, 192),
            (0, 0, self.screen.get_width(), self.top_offset - 20)
        )

        elapsed_time = self.board.get_elapsed_time()

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        time_text = self.font.render(f"Time: {str(minutes).zfill(2)}:{str(seconds).zfill(2)}", 
                                     True, (0, 0, 0))
        self.screen.blit(time_text, (self.screen.get_width() // 2 + 10, 20))

        remaining = self.board.get_remaining_mines()
        self.draw_counter(remaining, self.left_offset + 10, 20)

    def draw_counter(self, value, x, y):
        counter_rect = pygame.Rect(x, y, 50, 30)
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            counter_rect
        )
        pygame.draw.rect(
            self.screen,
            (128, 128, 128),
            counter_rect.inflate(-4, -4)
        )

        counter_text = self.font.render(f"{value:03d}", True, (255, 0, 0))
        self.screen.blit(
            counter_text,
            (counter_rect.centerx - counter_text.get_width() // 2,
             counter_rect.centery - counter_text.get_height() // 2)
        )

    def draw_grid(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                x = self.left_offset + col * self.cell_size
                y = self.top_offset + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if self.board.revealed[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        self.colors["revealed"],
                        rect
                    )

                    if self.board.grid[row][col] == -1:
                        color = (255, 0, 0) if self.board.game_over else self.colors["mine"]
                        pygame.draw.circle(
                            self.screen,
                            color,
                            rect.center,
                            self.cell_size // 3
                        )
                    elif self.board.grid[row][col] > 0:
                        text = self.font.render(
                            str(self.board.grid[row][col]),
                            True,
                            self.colors["numbers"][self.board.grid[row][col] - 1]
                        )
                        self.screen.blit(
                            text,
                            (rect.centerx - text.get_width() // 2,
                             rect.centery - text.get_height() // 2)
                        )

                    pygame.draw.rect(
                        self.screen,
                        self.colors["border_dark"],
                        rect,
                        1
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        self.colors["hidden"],
                        rect
                    )

                    pygame.draw.line(
                        self.screen,
                        self.colors["border_light"],
                        (x, y),
                        (x + self.cell_size - 1, y),
                        2
                    )
                    pygame.draw.line(
                        self.screen,
                        self.colors["border_light"],
                        (x, y),
                        (x, y + self.cell_size - 1),
                        2
                    )
                    pygame.draw.line(
                        self.screen,
                        self.colors["border_dark"],
                        (x + self.cell_size - 1, y),
                        (x + self.cell_size - 1, y + self.cell_size - 1),
                        2
                    )
                    pygame.draw.line(
                        self.screen,
                        self.colors["border_dark"],
                        (x, y + self.cell_size - 1),
                        (x + self.cell_size - 1, y + self.cell_size - 1),
                        2
                    )

                    state = self.board.cell_states[row][col]
                    if state == 1:
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),
                            (x + 5, y + 5, 20, 15)
                        )
                        pygame.draw.polygon(
                            self.screen,
                            (255, 0, 0),
                            [(x + 5, y + 5), (x + 15, y + 12), (x + 5, y + 20)]
                        )
                        pygame.draw.line(
                            self.screen,
                            (0, 0, 0),
                            (x + 5, y + 5),
                            (x + 5, y + self.cell_size - 5),
                            2
                        )
                    elif state == 2:
                        text = self.font.render("?", True, (0, 0, 255))
                        self.screen.blit(
                            text,
                            (rect.centerx - text.get_width() // 2,
                             rect.centery - text.get_height() // 2))

    def get_cell_from_pos(self, pos):
        x, y = pos
        if (self.left_offset <= x < self.left_offset + self.board.cols * self.cell_size and
            self.top_offset <= y < self.top_offset + self.board.rows * self.cell_size):
            col = (x - self.left_offset) // self.cell_size
            row = (y - self.top_offset) // self.cell_size
            return row, col
        return None
