import pygame
import sys

from constants import *
import player
import asteroid
import asteroidfield
import shot

def main(): 

    #Logic Setup 
    score = 0
    score_timer = 0.0
    wave = 1 
    asteroids_destroyed_till_next_wave = 10

    lives = 3

    pygame.init()

    #Game Clock Setup
    game_clock = pygame.time.Clock()
    dt = 0

    #Graphics Setup
    color = pygame.Color(10,10,10)
    font = pygame.font.SysFont('Arial',int(20 * SCALE))

    game_surface = pygame.Surface((BOARD_HEIGHT,BOARD_WIDTH))
    game_surface.fill(color)

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    
    #Sprite Group Declarations 
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #Pygame container setup
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
                    asteroid_field.num_asteroids = 0
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
                    if asteriod.radius <= ASTEROID_MIN_RADIUS:
                        asteroid_field.num_asteroids -= 1
                        asteroids_destroyed_till_next_wave -= 1
                        if asteroids_destroyed_till_next_wave <= 0:
                            wave += 1
                            asteroid_field.wave_complete() 
                            asteroids_destroyed_till_next_wave = 10 + wave * 5
                    asteriod.split()
                    score = score + 100

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

        #Waves Layer
        wave_surface =font.render(f"Wave: {wave}", True, (255, 255, 255))
        screen.blit(wave_surface, (0,score_surface.get_height()))

        #Update screen
        pygame.display.flip()

        #Update score timer 
        score_timer += dt

        #sets frame timer 
        dt = game_clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()



