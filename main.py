import pygame
import sys

from constants import *
import player
import asteroid
import asteroidfield
import shot




def main(): 

    score = 0
    score_timer = 0.0

    lives = 3

    pygame.init()

    color = pygame.Color(10,10,10)
    game_clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.SysFont('Arial',int(20 * SCALE))

    game_surface = pygame.Surface((BOARD_HEIGHT,BOARD_WIDTH))
    game_surface.fill(color)

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    
   
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    player.Player.containers = (updatable,drawable)
    shot.Shot.containers = (shots,updatable,drawable)

    asteroid.Asteroid.containers = (asteroids,updatable,drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    

    player_model = player.Player(BOARD_WIDTH/2 , BOARD_HEIGHT / 2)
    asteroid_field = asteroidfield.AsteroidField()


    while True:

        #Event handler: Quit Game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #updates player model if key interrupt 
        updatable.update(dt)

        #Increases score every second 
        if(score_timer >= 1.0):
            seconds_passed = int(score_timer)
            score += seconds_passed
            score_timer -= seconds_passed

        #Player Collision Check 
        for asteriod in asteroids:
            if player_model.check_collisions(asteriod):
                lives = lives - 1 
                if lives > 0:
                    #Reset Function WIP
                    for a in asteroids:
                        a.kill()
                    for _shot in shots:
                        _shot.kill()
                    player_model.position = pygame.Vector2(BOARD_WIDTH/2 , BOARD_HEIGHT / 2)
                else:    
                    print("Game over!")
                    print(f"Score: {score}")
                    sys.exit()

            for _shot in shots:
                if _shot.check_collisions(asteriod):
                    _shot.kill()
                    asteriod.split()
                    score = score + 10

        #Fills screen with black
        game_surface.fill(color)

        #draws player model on screen 
        for obj in drawable:
            obj.draw(game_surface)

        if (BOARD_HEIGHT != SCREEN_HEIGHT) or (BOARD_WIDTH != SCREEN_HEIGHT):
            scaled_surface = pygame.transform.scale(game_surface,screen.get_size())
            #renders current screen 
            screen.blit(scaled_surface,(0,0))

        else:
            screen.blit(game_surface,(0,0))

        #Score Layer 
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (0,0))

        #Lives Layer
        text_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH-(text_surface.get_width() + 10 ),0))

        #Update screen
        pygame.display.flip()

        #Update score timer 
        score_timer += dt

        #sets frame timer 
        dt = game_clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()



