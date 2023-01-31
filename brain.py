import pygame
import random
import math
import numpy as np
from utilitaries import *


class Brain():
    def __init__(self,bird,weights=[],bias=None):
        self.bird = bird 

        self.number_of_inputs = NUMBER_OF_INPUTS
        self.number_of_weights = NUMBER_OF_WEIGHTS
        self.weight = np.zeros(self.number_of_weights)
        if len(weights)==0:
            for i in range (self.number_of_weights):
                self.weight[i] = random.random()*random.choice([-1,1])
        else:
            self.weight = weights

        if bias:
            self.bias = bias
        else:
            self.bias = random.random()*random.choice([-1,1])

        self.input = np.zeros(self.number_of_inputs)

        self.output = 0
        self.treshold_output = 0.5

        self.coeff_for_output = 1/100

        # self.neural_network_type = "One_layer"
        self.neural_network_type = "Two_layers"

    def compute_inputs(self,game):
        x_closest_pipe = WINDOW_WIDTH_GAME*1.5
        bird_posX = self.bird.posX - game.all_pipes.image_size[0]
        # bird_posX = self.bird.posX 
        for pipe in game.all_pipes:
            if (pipe.posX>bird_posX):
                x_closest_pipe = min(x_closest_pipe,pipe.posX)
                if (x_closest_pipe==pipe.posX):
                    if (pipe.type=="top"):
                        pipe_posY_top = pipe.posY+game.all_pipes.image_size[1]
                    elif (pipe.type=="bot"):
                        pipe_posY_bot = pipe.posY

        
        self.input[0] = x_closest_pipe - self.bird.posX   ## distance with closest pipe

        self.input[1] = pipe_posY_top - self.bird.posY

        self.input[2] = pipe_posY_bot - self.bird.posY

        self.input[3] = self.bird.posY

        self.input[4] = self.bird.velocity

        # print("Distance x: "+str(self.input[0]))
        # print("Distance top: "+str(self.input[1]))
        # print("Distance bot: "+str(self.input[2]))

    def compute_outputs(self):
        output = 0.0
        match self.neural_network_type:
            case "One_layer":
                for i in range (self.number_of_inputs):
                    output += self.weight[i]*self.input[i]
                output += self.bias 

            case "Two_layers":
                output_int1 = 0.0
                output_int2 = 0.0
                for i in range (self.number_of_inputs):
                    output_int1 += self.weight[i]*self.input[i]
                output_int1 += self.bias
                for i in range (self.number_of_inputs,self.number_of_inputs*2):
                    output_int2 -= self.weight[i]*self.input[i-self.number_of_inputs]
                output_int2 += self.bias

                output += self.weight[self.number_of_inputs*2]*output_int1
                output += self.weight[self.number_of_inputs*2+1]*output_int2
                output += self.bias                 

        ouput_norm = math.tanh(output*self.coeff_for_output)
        # print(ouput_norm)

        if (ouput_norm>self.treshold_output):
            self.bird.flap()

    def compute_fitness(self):
        self.fitness = self.bird.timer
        return self.fitness






        
