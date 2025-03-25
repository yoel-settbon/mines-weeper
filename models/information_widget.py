import pygame
from models.utilities import *

class TopBar(pygame.Surface):
    def __init__(self, width, height, num_flags):
        super().__init__((width, height))
        self.score = 0
        self.paused = False
        self.elapsed_time = 0
        self.timer_start_ticks = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Arial", 36)
        self.num_flags = num_flags
    
    def update(self):
        if not self.paused :
            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.timer_start_ticks) // 1000
        
        self.draw()
    
    def draw(self):
        self.fill(GRAY)
        score_text = self.font.render(f"Score : {self.score}", True, BLACK)
        time_text = self.font.render(f"Time : {self.elapsed_time}", True, BLACK)
        num_flags_text = self.font.render(f"Flags : {self.num_flags}", True, BLACK)
        self.blit(score_text, (0.1 * self.width, 0.1 * self.height))
        self.blit(time_text, (0.1 * self.width, 0.3 * self.height))
        self.blit(num_flags_text, (0.1 * self.width, 0.5 * self.height))
    
    def reset(self):
        self.score = 0
        self.time = 0
        self.timer_start_ticks = pygame.time.get_ticks()