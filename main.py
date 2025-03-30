import pygame
import sys

from constants import *
import player
import asteroid
import asteroidfield
import shot




def main(): 

    pygame.init()

    game_clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    color = pygame.Color(0,0,0)
   
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    player.Player.containers = (updatable,drawable)
    shot.Shot.containers = (shots,updatable,drawable)

    asteroid.Asteroid.containers = (asteroids,updatable,drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    

    player_model = player.Player(SCREEN_WIDTH/2 , SCREEN_HEIGHT / 2)
    asteroid_field = asteroidfield.AsteroidField()


    while True:

        #Event handler: Quit Game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #updates player model if key interrupt 
        updatable.update(dt)

        for asteriod in asteroids:
            if player_model.check_collisions(asteriod):
                print("Game over!")
                sys.exit()

            for _shot in shots:
                if _shot.check_collisions(asteriod):
                    _shot.kill()
                    asteriod.split()

        #Fills screen with black
        screen.fill(color)

        #draws player model on screen 
        for obj in drawable:
            obj.draw(screen)

        #renders current screen 
        pygame.display.flip()

        #sets frame timer 
        dt = game_clock.tick(60) / 1000

if __name__ == "__main__":
    main()



