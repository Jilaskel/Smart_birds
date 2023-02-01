import pygame
import random
from bird import *
from brain import *
from utilitaries import *


class Population():
    def __init__(self,game):
        self.game = game

        self.number = game.population_number

        self.birds = []
        for i in range(self.number):
            self.birds.append(Bird())

        self.number_of_inputs = NUMBER_OF_INPUTS
        self.number_of_weights = NUMBER_OF_WEIGHTS

        self.best_rate = game.best_rate

        self.timer = 0.0
        # self.live_period = 0.25
        self.live_period = 0.0

        # self.reproducing_mode = "One_parent"
        # self.reproducing_mode = "Two_parents_random_choice"
        self.reproducing_mode = "Two_parents_random_average"

    def live(self,game):
        self.timer += game.timestep/1000
        if self.timer>self.live_period:
            for bird in self.birds:
                if bird.alive:
                    bird.brain.compute_inputs(self.game)
                    bird.brain.compute_outputs()
            self.timer = 0.0

    def render(self):
        for bird in self.birds:
            bird.render()        
        
    def compute_fitness_sum(self):
        self.fitness_sum = 0.0
        self.max_fitness = 0.0
        for bird in self.birds:
            self.fitness_sum += bird.brain.compute_fitness()
            self.max_fitness = max(self.max_fitness,bird.brain.fitness)
            if self.max_fitness==bird.brain.fitness:
                self.best_bird = bird
        print("Last best time : "+ str(round(self.best_bird.brain.fitness/1000,2))+ " s")
        print("Average time : "+ str(round(self.fitness_sum/self.number/1000,2))+" s")

    def reproduce(self):
        match self.reproducing_mode:
            case "One_parent":
                for bird in self.birds:
                    parent1 = self.select_parent()

                    weights = np.zeros(self.number_of_weights)
                    for i in range(self.number_of_weights):
                        weights[i] = parent1.brain.weight[i] 
                    bias = parent1.brain.bias

                    bird.new_brain = Brain(bird,weights,bias)     
            case "Two_parents_random_choice":
                for bird in self.birds:
                    parent1 = self.select_parent()
                    parent2 = self.select_parent()

                    weights = np.zeros(self.number_of_weights)
                    for i in range(self.number_of_weights):
                        weights[i] = random.choice([parent1.brain.weight[i],parent2.brain.weight[i]])
                    bias = random.choice([parent1.brain.bias,parent2.brain.bias])

                    bird.new_brain = Brain(bird,weights,bias)
            case "Two_parents_random_average": 
                for bird in self.birds:
                    parent1 = self.select_parent()
                    parent2 = self.select_parent()

                    weights = np.zeros(self.number_of_weights)
                    rand = random.random()
                    for i in range(self.number_of_weights):
                        weights[i] = rand*parent1.brain.weight[i] + (1-rand)*parent2.brain.weight[i]
                    bias = rand*parent1.brain.bias+(1-rand)*parent2.brain.bias

                    bird.new_brain = Brain(bird,weights,bias)
      

    def mutate(self):
        for bird in self.birds:
            rand = random.random()
            if rand<self.game.mutation_rate:
                rand_int = random.randint(0,self.number_of_weights)
                if rand_int<self.number_of_weights:
                    bird.new_brain.weight[rand_int] = random.random()*random.choice([-1,1])
                else:
                    bird.new_brain.bias = random.random()*random.choice([-1,1])


    def next_gen(self):
        self.compute_fitness_sum()
        self.reproduce()
        self.mutate()
        for bird in self.birds:
            bird.brain = bird.new_brain


    def select_parent(self):
        rand = random.random()
        if rand<self.best_rate:
            return self.best_bird
        else:
            rand = random.random()*self.fitness_sum
            running_sum = 0.0
            for bird in self.birds:
                running_sum += bird.brain.fitness
                if (running_sum>rand):
                    return bird

        print("Issue with parent selection")


