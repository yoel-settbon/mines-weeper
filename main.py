import pygame
from Game.game import Game


def main(Width=560, Height=600, Title="Minesweeper"):
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption(Title)
    Minesweeper = Game()
    Minesweeper.run()


if __name__ == "__main__":
    main()
