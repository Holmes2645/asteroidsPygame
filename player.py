import pygame

from circleshape import CircleShape
from constants import *
import shot

class Player(CircleShape):

    #Contructor 
    def __init__(self, x, y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    #Draws white triangle onto pygame screen
    def draw(self, screen):
        pygame.draw.polygon(screen,"white",self.triangle(),2)

    #Updates position and orientation of triangle based on key press
    def update(self, dt):

        self.timer -= dt

        #Catches key interrupt 
        keys = pygame.key.get_pressed()

        #Move Foward(W)
        if keys[pygame.K_w]:
            self.move(dt)

        #Move Back(S)
        if keys[pygame.K_s]:
            self.move(-dt)

        #Rotate Left(A)
        if keys[pygame.K_a]:
            self.rotate(-dt)

        #Rotate Right(D)
        if keys[pygame.K_d]:
            self.rotate(dt)

        #Shoot(Space)
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()

    #Updates rotation angle of triangle 
    def rotate(self, dt):
        self.rotation += PLAYER_TURNING_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        self.timer = PLAYER_SHOOT_COOLDOWN
        new_shot = shot.Shot(self.position.x, self.position.y)
        new_shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED





    # Calculates points of a triangle for player model
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] 
