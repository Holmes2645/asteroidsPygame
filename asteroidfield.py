import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * BOARD_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                BOARD_WIDTH + ASTEROID_MAX_RADIUS, y * BOARD_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * BOARD_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * BOARD_WIDTH, BOARD_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.num_asteroids = 0
        self.max_asteroids = 20
        self.wave = 1 

    def calc_speed(self):
        min_speed = int(10 + self.wave * 0.15)
        max_speed = int(50 + self.wave * 0.5)
        return random.randint(min_speed, max_speed)
    
    def wave_complete(self):
        self.wave += 1
        self.max_asteroids += 10

    def spawn(self, radius, position, velocity):
        #Checks for number of asteroids on field 
        if self.num_asteroids < self.max_asteroids:
            asteroid = Asteroid(position.x, position.y, radius)
            asteroid.velocity = velocity
            self.num_asteroids += 1

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = self.calc_speed()
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)


    
