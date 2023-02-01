import pygame
from pygame.locals import *
from bird import * 
from pipe import * 
from utilitaries import *

############################# 
## Main functions
#############################

class Game():
    def __init__(self):

        self.timestep = 0.0

        self.score = 0

        self.ratio_for_hitbox = 0.97

        self.bird = Bird()

        self.all_pipes = All_pipes()

        self.font_size = int(100*RESIZE_COEFF_GAME)
        self.font = pygame.font.Font(FONT_PATH,self.font_size)
        self.font_color = (243,243,243)
        self.font_pos = vec(10*RESIZE_COEFF_GAME,10*RESIZE_COEFF_GAME)

    def move_objects(self):
        self.bird.move(self)
        for pipe in self.all_pipes:
            pipe.move(self)
        self.all_pipes.spawning()   

    def check_impact(self):
        self.hit = pygame.sprite.spritecollide(self.bird, self.all_pipes, False,pygame.sprite.collide_rect_ratio(self.ratio_for_hitbox))
        if ((self.bird.posY<-self.bird.image_size[1]) or (self.bird.posY>WINDOW_HEIGHT_GAME)):
            out = True
        else:
            out = False

        if (self.hit or out):
            global_status.status = "Game Over"


    def restart(self):
        self.bird.reset()
        self.all_pipes.reset()
        self.score = 0

    def display_score(self):
        txt = "Score: " + str(int(self.score))
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,self.font_pos)

    def render(self):
        window.fill((0,0,0))

        self.bird.render()

        for pipe in self.all_pipes:
            pipe.render()

        self.display_score()

        pygame.display.update()

    def get_event(self):
        CLOCK.tick(FPS)
        self.timestep = CLOCK.get_time()

        self.all_events = pygame.event.get()
        for event in self.all_events:
                if event.type == QUIT:
                    global_status.status = "Quitting"
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE): 
                        global_status.status = "Quitting"
                    if (event.key == K_p):
                        if (global_status.status == "In game"):
                            global_status.status = "In pause"
                        elif (global_status.status == "In pause"):
                            global_status.status = "In game"
                    if (event.key == K_SPACE):
                        if (global_status.status == "In pause"):
                            global_status.status = "In game"
                        self.bird.velocity = FLAP_SPEED
                    
                    if (event.key == K_r):
                        self.restart()
                        global_status.status = "In pause"