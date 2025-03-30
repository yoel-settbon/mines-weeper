import pygame
from models.game import Game
from models.main_menu import MainMenu

def main():
    pygame.init()
    
    # Initialiser le menu principal
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("Mines Weeper")
    
    # Boucle principale
    running = True
    
    # Créer le menu principal
    menu = MainMenu(screen)
    
    while running:
        # Afficher le menu principal 
        player_name, should_start = menu.run()
        
        # Si l'utilisateur a cliqué sur "Jouer", démarrer une partie
        if should_start:
            # Créer et démarrer le jeu avec le nom du joueur
            game = Game(player_name)
            
            # Exécuter le jeu
            return_to_menu = game.run()
            
            # Si le jeu est terminé, retourner au menu principal
            if not return_to_menu:
                running = False
        else:
            # Si l'utilisateur a fermé la fenêtre depuis le menu
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()