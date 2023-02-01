# Import module
import random
import sys
import pygame
from game import * 
from utilitaries import * 


game = Game()

print("Starting game")

while RUNNING:

    game.get_event()

    match global_status.status:

        case "In game":
                game.move_objects()
                game.check_impact() 

                game.render()

        case "In pause":
                game.render()                

        case "Game Over":
                game.render()

        case "Quitting":
                pygame.quit()
                RUNNING = False
                sys.exit()