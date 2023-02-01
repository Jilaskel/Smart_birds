import pygame
import random
from pygame.locals import *
from population import * 
from bird import * 
from pipe import * 
from neural_network import * 
from utilitaries import *

############################# 
## Main functions
#############################

class Game():
    def __init__(self):

        self.timestep = 0.0

        self.score = 0
        self.best_score = 0

        self.speed_factor = 1.0
        self.gravity_coeff = 2.0

        self.ratio_for_hitbox = 0.97

        self.population = Population(self)
        self.number_alive = self.population.number
        self.generation_number = 1

        self.my_bird = random.choice(self.population.birds)

        self.all_pipes = All_pipes()

        self.neural_network = Neural_network(self.my_bird.brain)
        # self.neural_network.brain = self.my_bird.brain


        self.font_size = int(100*RESIZE_COEFF_GAME)
        self.font = pygame.font.Font(FONT_PATH,self.font_size)
        self.font_color = (243,243,243)
        self.font_pos = vec(10*RESIZE_COEFF_GAME,WINDOW_HEIGHT_GAME*1.1)
        self.font_margin = WINDOW_HEIGHT_GAME*0.1

    def move_objects(self):
        for bird in self.population.birds:
            if bird.alive:
                bird.move(self)

        for pipe in self.all_pipes:
            pipe.move(self)
        self.all_pipes.spawning()   

    def check_impact(self):
        self.number_alive = 0
        self.birds_alive = []
        for bird in self.population.birds:
            if bird.alive:
                self.hit = pygame.sprite.spritecollide(bird, self.all_pipes, False,pygame.sprite.collide_rect_ratio(self.ratio_for_hitbox))
                if ((bird.posY<-bird.image_size[1]) or (bird.posY>WINDOW_HEIGHT_GAME)):
                    out = True
                else:
                    out = False

                if (self.hit or out):
                    bird.alive = False
                
                self.number_alive += 1
                self.birds_alive.append(bird)

        if self.number_alive==0:
            # global_status.status = "In pause" 
            self.restart()           

    def live(self):
        self.population.live(self)


    def restart(self):
        print("=== Generation n°"+str(self.generation_number)+" ===")
        self.population.next_gen()

        for bird in self.population.birds:
            bird.reset()
        self.all_pipes.reset()
        self.best_score = max(self.best_score,self.score)
        self.score = 0
        self.generation_number += 1

    def display_text(self):
        txt = "Score: " + str(int(self.score))
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,self.font_pos)

        txt = "Number of birds alive: " + str(int(self.number_alive))
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,(self.font_pos[0],self.font_pos[1]+self.font_margin))        

        txt = "Generation: " + str(int(self.generation_number))
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,(self.font_pos[0],self.font_pos[1]+self.font_margin*2))    

        txt = "Best Score: " + str(int(self.best_score))
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,(self.font_pos[0],self.font_pos[1]+self.font_margin*3))   

        txt = "Speed Factor: x" + str(self.speed_factor)
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,(self.font_pos[0],self.font_pos[1]+self.font_margin*5))   

        txt = "Gravity: x" + str(self.gravity_coeff)
        self.txt = self.font.render(txt,True,self.font_color)
        window.blit(self.txt,(self.font_pos[0],self.font_pos[1]+self.font_margin*6)) 

    def render(self):
        window.fill((0,0,0))
        window_game.fill((0,0,0))

        self.population.render()

        for pipe in self.all_pipes:
            pipe.render()

        self.display_text()

        window.blit(window_game,(0,0))

        if self.birds_alive:
            if not self.my_bird.alive:
                self.my_bird = random.choice(self.birds_alive)
            self.neural_network.brain = self.my_bird.brain
            self.neural_network.render()

        pygame.display.update()

    def get_event(self):
        CLOCK.tick(FPS**self.speed_factor)
        self.timestep = CLOCK.get_time()*self.speed_factor

        self.all_events = pygame.event.get()
        for event in self.all_events:
                if event.type == QUIT:
                    global_status.status = "Quitting"
                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE): 
                        global_status.status = "Quitting"
                    if (event.key == K_p):
                        if (global_status.status == "Learning"):
                            global_status.status = "In pause"
                        elif (global_status.status == "In pause"):
                            global_status.status = "Learning"
                    if (event.key == K_SPACE):
                        if (global_status.status == "In pause"):
                            global_status.status = "Learning"
                    
                    if (event.key == K_r):
                        self.restart()
                        global_status.status = "In pause"

                    if (event.key == K_RIGHT):
                        self.speed_factor *= 2.0

                    if (event.key == K_LEFT):
                        self.speed_factor /= 2.0

                    if (event.key == K_UP):
                        self.gravity_coeff *= 2.0

                    if (event.key == K_DOWN):
                        self.gravity_coeff /= 2.0