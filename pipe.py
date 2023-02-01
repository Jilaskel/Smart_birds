import pygame
import random
from utilitaries import *


class All_pipes(pygame.sprite.Group):
        def __init__(self,game):
            pygame.sprite.Group.__init__(self)  
            self.game = game

            posX = PIPE_STARTING_POSX
            posY = PIPE_STARTING_POSY

            self.image_top = pygame.image.load(PIPE_PATH).convert_alpha()
            self.image_top = pygame.transform.scale(self.image_top,vec(self.image_top.get_size())*PIPE_RESIZE_COEFF*RESIZE_COEFF_GAME) 

            self.image_bot = self.image_top.convert_alpha()
            self.image_bot = pygame.transform.flip(self.image_bot, False, True)

            self.image_size = self.image_top.get_size()

            self.add_two_pipes(posX,posY)

        def add_two_pipes(self,posX,posY):
            posY_top = posY - self.game.pipe_space_factor*PIPE_SPACE_Y*0.5 - self.image_size[1]
            posY_bot = posY + self.game.pipe_space_factor*PIPE_SPACE_Y*0.5

            self.add(Pipe(self,posX,posY_top,True))
            self.add(Pipe(self,posX,posY_bot,False))

        def spawning(self):
            x_max = 0.0
            for pipe in self:
                if ((pipe.posX+self.image_size[0])<0.0):
                    pygame.sprite.Sprite.kill(pipe)   
                if (pipe.posX>x_max):
                    x_max = pipe.posX  
 
            if ((WINDOW_WIDTH_GAME-x_max)>PIPE_SPACE_X):
                rand_posY = PIPE_SPAWN_BOUND_MIN + random.randint(0,100)/100*(PIPE_SPAWN_BOUND_MAX-PIPE_SPAWN_BOUND_MIN) 
                self.add_two_pipes(WINDOW_WIDTH_GAME,rand_posY)

        def reset(self):
            self.empty()

            posX = PIPE_STARTING_POSX
            posY = PIPE_STARTING_POSY

            self.add_two_pipes(posX,posY)       

class Pipe(pygame.sprite.Sprite):
    def __init__(self,all,posX,posY,top):
        super().__init__()

        self.posX = posX
        self.posY = posY

        self.velocity = -PIPE_VELOCITY

        if (top):
            self.image = all.image_top
            self.type = "top"
        else:
            self.image = all.image_bot
            self.type = "bot"

        self.rect = self.image.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def move(self,game):
        dx = self.velocity*game.timestep/1000
        if ((self.posX>BIRD_STARTING_POSX) and ((self.posX+dx)<BIRD_STARTING_POSX)):
            game.score += 0.5
        self.posX += dx
        self.rect.x = self.posX

    def render(self):
        window_game.blit(self.image, (self.posX, self.posY))  

