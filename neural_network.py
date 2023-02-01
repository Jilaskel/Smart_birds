import pygame
import numpy as np
from utilitaries import *

class Neural_network():
    def __init__(self,brain):
        self.brain = brain

        self.node_color = (0,255,0)
        self.radius = 20*RESIZE_COEFF_GAME
        self.width_circle = int(2*RESIZE_COEFF_GAME)

        self.pos_conn_color = (0,153,0)
        self.neg_conn_color = (153,0,0)
        self.width_nom = 10*RESIZE_COEFF_GAME


        self.font_size = int(50*RESIZE_COEFF_GAME)
        self.font = pygame.font.Font(FONT_NUMERIC_PATH,self.font_size)
        self.font_color = (0,245,0)
        self.font_pos = np.zeros((NUMBER_OF_INPUTS,2))
        self.font_margin = WINDOW_HEIGHT_GAME*0.05

        self.center_input = vec(WINDOW_WIDTH *0.65, WINDOW_HEIGHT *0.05)
        self.center_layer_one = vec(WINDOW_WIDTH *0.80, WINDOW_HEIGHT *0.05)
        self.center_output = vec(WINDOW_WIDTH *0.95, WINDOW_HEIGHT *0.05)

        self.margin = WINDOW_HEIGHT*0.1

        self.nodes = []
        for i in range (NUMBER_OF_INPUTS):
            self.nodes.append(Node(self,self.center_input+vec(0,self.margin*i)))
            self.font_pos[i,:] = self.center_input+vec(-6.5*self.font_margin,self.margin*i-0.1*self.margin)

        self.layer_node_1 = Node(self,self.center_layer_one+vec(0,self.margin*1.5))
        self.nodes.append(self.layer_node_1)
        self.layer_node_2 = Node(self,self.center_layer_one+vec(0,self.margin*2.5))
        self.nodes.append(self.layer_node_2)

        self.output_node = Node(self,self.center_output+vec(0,self.margin*2),True)
        self.nodes.append(self.output_node)

        self.connections = []
        for i in range (NUMBER_OF_INPUTS):
            self.connections.append(Connection(self,self.nodes[i],self.layer_node_1,i,i,0))
            self.connections.append(Connection(self,self.nodes[i],self.layer_node_2,i+NUMBER_OF_INPUTS,i,1))

        self.connections.append(Connection(self,self.layer_node_1,self.output_node,NUMBER_OF_INPUTS*2,0,2))
        self.connections.append(Connection(self,self.layer_node_2,self.output_node,NUMBER_OF_INPUTS*2+1,0,2))



    # def connect_with_brain(self,brain):
    #     self.brain = brain 

    #     self.connections = []
    #     for i in range (NUMBER_OF_INPUTS):
    #         self.connections.append(Connection(self,self.nodes[i],self.layer_node_1,i,self.brain.input[i],self.brain.output_int1))


    def render(self):
        for conn in self.connections:
            conn.render()
        for node in self.nodes:
            node.render()
        for i in range (NUMBER_OF_INPUTS):
            mess = self.brain.input_txt[i] + str(round(self.brain.input[i],1))
            txt = self.font.render(mess,True,self.font_color)
            window.blit(txt,self.font_pos[i,:])



class Node():
    def __init__(self,neural_network,center,last=False):

        self.neural_network = neural_network

        self.center = center
        
        self.last = last

    def render(self):
        if not self.last:
            pygame.draw.circle(window, self.neural_network.node_color, self.center, radius=self.neural_network.radius, width = 0)
        else:
            if (self.neural_network.brain.output_norm>self.neural_network.brain.treshold_output):
                pygame.draw.circle(window, self.neural_network.node_color, self.center, radius=self.neural_network.radius, width = 0)
            else:
                pygame.draw.circle(window, self.neural_network.node_color, self.center, radius=self.neural_network.radius, width = self.neural_network.width_circle)


class Connection():
    def __init__(self,neural_netowrk,node_1,node_2,weight_number,input_number,output_number):
        self.neural_network = neural_netowrk

        self.start_pos = node_1.center
        self.end_pos = node_2.center

        self.weight_number = weight_number
        self.input_number = input_number
        self.output_number = output_number

    def render(self):
        if self.output_number==0:
            sum_abs = sum(abs(self.neural_network.brain.weight[0:NUMBER_OF_INPUTS]*self.neural_network.brain.input[0:NUMBER_OF_INPUTS]))
            coeff = self.neural_network.brain.weight[self.weight_number]*self.neural_network.brain.input[self.input_number]/sum_abs

        elif self.output_number==1:
            sum_abs = sum(abs(self.neural_network.brain.weight[NUMBER_OF_INPUTS:NUMBER_OF_INPUTS*2]*self.neural_network.brain.input[0:NUMBER_OF_INPUTS]))
            coeff = self.neural_network.brain.weight[self.weight_number]*self.neural_network.brain.input[self.input_number]/sum_abs

        else:
            sum_abs = abs(self.neural_network.brain.weight[NUMBER_OF_INPUTS*2]*self.neural_network.brain.output[0]) + abs(self.neural_network.brain.weight[NUMBER_OF_INPUTS*2+1]*self.neural_network.brain.output[1])
            if (self.weight_number==NUMBER_OF_INPUTS*2):
                coeff = self.neural_network.brain.weight[NUMBER_OF_INPUTS*2]*self.neural_network.brain.output[0]/sum_abs
            else:
                coeff = self.neural_network.brain.weight[NUMBER_OF_INPUTS*2+1]*self.neural_network.brain.output[1]/sum_abs

        if coeff>0:
            color = self.neural_network.pos_conn_color
        else:
            color = self.neural_network.neg_conn_color

        if abs(coeff)>1:
            print(coeff)

        width_line = int(abs(coeff)*self.neural_network.width_nom)+1
        pygame.draw.line(window, color, self.start_pos, self.end_pos, width = width_line)