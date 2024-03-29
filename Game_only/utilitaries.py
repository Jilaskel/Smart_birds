import pygame


pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

RUNNING = True

### RESOLUTION
WINDOW_WIDTH_GAME = 1920
WINDOW_HEIGHT_GAME = 1080

RESIZE_COEFF_GAME = WINDOW_WIDTH_GAME/1920

window = pygame.display.set_mode((WINDOW_WIDTH_GAME, WINDOW_HEIGHT_GAME))

### FPS
FPS = 120
CLOCK = pygame.time.Clock() 

### GAME
GAME_TITLE = "Flappy bird IA"

pygame.display.set_caption(GAME_TITLE)

BIRD_PATH = "images/bird.png"
PIPE_PATH = "images/pipe_extended.png"
GROUND_PATH = "images/ground.png"


## BIRD
BIRD_RESIZE_COEFF = 1.0
GRAVITY_ACCELERATION = 1200*RESIZE_COEFF_GAME
FLAP_SPEED = -600*RESIZE_COEFF_GAME
BIRD_STARTING_POSX = WINDOW_WIDTH_GAME/5.0
BIRD_STARTING_POSY = WINDOW_HEIGHT_GAME/2.0


## PIPE 
PIPE_RESIZE_COEFF = 1.0
PIPE_STARTING_POSX = WINDOW_WIDTH_GAME*0.75
PIPE_STARTING_POSY = WINDOW_HEIGHT_GAME/2.0
PIPE_VELOCITY = 800*RESIZE_COEFF_GAME
PIPE_SPACE_X = WINDOW_WIDTH_GAME*0.75
PIPE_SPACE_Y = WINDOW_HEIGHT_GAME*0.20
PIPE_SPAWN_BOUND_MIN = WINDOW_HEIGHT_GAME/4.0
PIPE_SPAWN_BOUND_MAX = WINDOW_HEIGHT_GAME*3.0/4.0

FONT_PATH = "images/font/SparkyStonesRegular-BW6ld.ttf"

class Global_status():
    def __init__(self):
        self.status = "In pause"

global_status = Global_status()

