import pygame
from models.game import Game

def main(Width = 560, Height = 700, Title = "Minesweeper"):
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption(Title)
    Minesweeper = Game()
    Minesweeper.run()

if __name__ == "__main__" :
    main()