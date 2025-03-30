import pygame
from models.game import Game

def main():
    pygame.init()import pygame
from models.game import Game
from models.main_menu import MainMenu

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("Mines Weeper")
    
    running = True
    
    menu = MainMenu(screen)
    
    while running:
        player_name, should_start = menu.run()
        
        if should_start:
            game = Game(player_name)
            
            return_to_menu = game.run()
        
            if not return_to_menu:
                running = False
        else:
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()