import pygame
from models.grid import Grid
from models.information_widget import TopBar
from models.utilities import *

pygame.init()

class Game :
    def __init__(self, cell_num = 20, mines_count = 20, num_flags = 10):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.topbar_height = 0.20 * self.screen_height
        self.grid_height = self.screen_height - self.topbar_height
        self.grid_width = self.screen_width
        self.cell_num = cell_num
        self.cell_size = self.grid_width // self.cell_num
        self.mines_count = mines_count
        self.top_bar = TopBar(self.screen_width, self.topbar_height, num_flags)
        self.grid = Grid(self.grid_width, self.grid_height, self.cell_size, self.cell_num, self.mines_count, self.topbar_height)
        self.running = True
        self.paused = False
        self.game_over = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.running = False
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE : 
                    self.paused = not self.paused
                    self.top_bar.paused = self.paused

                    if self.paused :
                        self.paused_time = pygame.time.get_ticks()
                    else :
                        paused_duration = pygame.time.get_ticks() - self.paused_time
                        self.top_bar.timer_start_ticks += paused_duration
                elif event.key == pygame.K_ESCAPE and self.game_over :
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused and not self.game_over :
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y > self.topbar_height :
                    cell_x = mouse_x // self.cell_size
                    cell_y = (mouse_y - self.topbar_height) // self.cell_size
                    cell_y = int(cell_y)
                    if event.button == 1 :
                        if self.grid.revealed_cell(cell_x, cell_y):
                            self.handle_game_over()
                        else :
                            self.top_bar.score += 1
                        if self.grid.check_win_condition():
                            self.handle_game_over()
                            self.top_bar.score += 1000
                    elif event.button == 3 and self.top_bar.num_flags :
                        self.grid.cells[cell_x][cell_y].toggle_flag()
                        self.top_bar.num_flags -= 1
        
    def update(self):
        if not self.paused and not self.game_over :
            self.top_bar.update()
    
    def draw_pause(self):
        font = pygame.font.SysFont("Arial", 72)
        paused_text = font.render("Paused", True, GREEN)
        rect = paused_text.get_rect(center = (self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(paused_text, rect)
    
    def draw_game_over(self):
        font = pygame.font.SysFont("Arial", 72)
        game_over_text = font.render("Game Over", True, RED)
        rect = game_over_text.get_rect(center = (self.screen_width // 2))
        self.screen.blit(game_over_text, rect)

    def draw_win(self):
        font = pygame.font.SysFont("Arial", 72)
        game_over_text = font.render("You Win", True, GREEN)
        rect = game_over_text.get_rect(center = (self.screen_width // 2, 0))
        self.screen.blit(game_over_text, rect)

    def handle_game_over(self):
        self.game_over = True
        self.grid.reveal_all_mines()

    def draw(self):
        self.screen.fill(WHITE)
        self.top_bar.draw()
        self.screen.blit(self.top_bar, (0, 0))
        self.grid.draw(self.screen)
        if self.game_over :
            self.draw_game_over()
        elif self.paused :
            self.draw_pause()
        pygame.display.flip()

    def reset_game(self):
        self.top_bar.reset()
        self.grid = Grid(self.grid_width, self.grid_height, self.cell_size, self.cell_num, self.mines_count, self.topbar_height)
        self.game_over = False
        self.paused = False

    def run(self):
        while self.running :
            self.handle_input()
            self.update()
            self.draw()
            pygame.time.wait(100)