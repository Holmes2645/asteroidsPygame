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

        if DEBUG:
            pygame.draw.circle(screen,"red",self.position,self.radius,width=2)

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


    def triangle(self, scale: float = 2.0) -> list[pygame.Vector2]:
        """
        Return the three vertices of an isosceles triangle that fully encloses
        the circular hit-box (self.radius).  `scale` > 1 enlarges the triangle;
        lower the value if you want it tighter.
        """
        # “Forward” points along the ship's nose; “right” is a wing-tip direction.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right   = pygame.Vector2(0, 1).rotate(self.rotation + 90)

        # Triangle dimensions
        height = self.radius * scale * 2        # nose to base
        half_base = self.radius * scale / 1.5   # base half-width

        # For isosceles, a good approximation: incenter is ~1/3 from base to tip
        incenter_offset = forward * (height / 3)

        #Tip
        a = self.position + forward * (2 * height / 3)

        # Base Corners 
        base_center = self.position - incenter_offset
        b = base_center - right * half_base  # left wing
        c = base_center + right * half_base  # right wing
        return [a, b, c]

