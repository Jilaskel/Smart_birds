import pygame
import random
from brain import * 
from utilitaries import *


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.alive = True

        self.timer = 0.0

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

        self.mask_transparency = 150
        self.mask_color = (random.random()*255, random.random()*255, random.random()*255)
        mask = pygame.mask.from_surface(self.image0)
        self.mask_image0 = mask.to_surface(setcolor=self.mask_color)
        self.mask_image0.set_colorkey((0, 0, 0))
        self.mask_image0.set_alpha(self.mask_transparency)        

        self.mask_image = self.mask_image0.convert_alpha()

        self.brain = Brain(self)
        self.new_brain = None

    def move(self,game):
        self.timer += game.timestep

        self.velocity += GRAVITY_ACCELERATION*game.gravity_factor*game.timestep/1000
        self.posY += self.velocity*game.timestep/1000
        self.rect.y = self.posY
        self.rotate()

    def flap(self):
        self.velocity = FLAP_SPEED

    def rotate(self):
        angle = self.velocity/FLAP_SPEED*self.angle_max
        if angle>0:
            angle = min(angle,self.angle_max)
        else:
            angle = max(angle,-self.angle_max)

        self.image = pygame.transform.rotate(self.image0, angle)
        self.mask_image = pygame.transform.rotate(self.mask_image0, angle)

    def reset(self):
        self.posX = BIRD_STARTING_POSX
        self.posY = BIRD_STARTING_POSY
        self.velocity = 0.0
        self.rotate()
        self.alive = True
        self.timer = 0.0

    def render(self):
        if self.alive:
            window_game.blit(self.image, (self.posX, self.posY))  
            window_game.blit(self.mask_image, (self.posX, self.posY))  