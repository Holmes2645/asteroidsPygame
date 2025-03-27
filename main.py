import pygame
from constants import *




def main(): 
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    color = pygame.Color(0,0,0)

    while True:

        #Event handler: Quit Game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #Fills screen with black
        screen.fill(color)
        pygame.display.flip()


if __name__ == "__main__":
    main()



