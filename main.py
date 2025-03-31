import pygame
from models.game import Game
from models.main_menu import MainMenu

def main():
    pygame.init()
    
    # Initialize the screen
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("Mines Weeper")
    
    # Main loop
    running = True
    
    while running:
        # Create the main menu (new instance each time)
        menu = MainMenu(screen)
        
        # Display the main menu
        player_name, should_start, difficulty = menu.run()
        
        # If the user clicked "Play", start a game
        if should_start:
            # Create and start the game with the player's name
            game = Game(player_name, difficulty)
            
            # Run the game
            return_to_menu = game.run()
            
            # Continue the loop if we need to return to the menu
            if not return_to_menu:
                running = False
        else:
            # If the user closed the window from the menu
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
