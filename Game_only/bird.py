import pygame
from utilitaries import *


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.posX = BIRD_STARTING_POSX
        self.posY = BIRD_STARTING_POSY

        self.image0 = pygame.image.load(BIRD_PATH).convert_alpha()
        self.image0 = pygame.transform.scale(self.image0,vec(self.image0.get_size())*BIRD_RESIZE_COEFF*RESIZE_COEFF_GAME) 

        self.image = self.image0.convert_alpha()

        self.image_size = self.image.get_size()

        self.velocity = 0.0
        self.angle_max = 45

        self.rect = self.image.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def move(self,game):
        self.velocity += GRAVITY_ACCELERATION*game.timestep/1000
        self.posY += self.velocity*game.timestep/1000
        self.rect.y = self.posY
        self.rotate()

    def rotate(self):
        angle = self.velocity/FLAP_SPEED*self.angle_max
        if angle>0:
            angle = min(angle,self.angle_max)
        else:
            angle = max(angle,-self.angle_max)

        self.image = pygame.transform.rotate(self.image0, angle)

    def reset(self):
        self.posX = BIRD_STARTING_POSX
        self.posY = BIRD_STARTING_POSY
        self.velocity = 0.0
        self.rotate()

    def render(self):
        window.blit(self.image, (self.posX, self.posY))  