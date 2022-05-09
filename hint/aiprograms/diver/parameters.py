import pygame
pygame.font.init()

NEURAL_DEEP = 1
NEURAL_WIDTH = 24
NEURAL_INPUTS = 12

WIDTH, HEIGHT = 900, 500
ME_VELOCITY = 5
ENEMY_SIZE = 50
ME_SIZE = 50
FPS = 800
MAX_MINE_VELOCITY = 3

# =====================================================================
# <----- ZDE Parametry nastavení evoluce !!!!!

VELIKOST_POPULACE = 10
EVO_STEPS = 5  # pocet kroku evoluce
# DELKA_JEDINCE = 100  # <--------- záleží na počtu vah a prahů u neuronů !!!!!
DELKA_JEDINCE = NEURAL_INPUTS * NEURAL_WIDTH + NEURAL_WIDTH * 4 + NEURAL_WIDTH * NEURAL_DEEP + (NEURAL_DEEP - 1) * NEURAL_WIDTH * NEURAL_WIDTH
NGEN = 30  # počet generací
CXPB = 0.6  # pravděpodobnost crossoveru na páru
MUTPB = 0.2  # pravděpodobnost mutace

SIMSTEPS = 300

#-----------------------------------------------------------------------------
# Parametry hry
#-----------------------------------------------------------------------------

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)


TITLE = "Boom Master"
pygame.display.set_caption(TITLE)





BOOM_FONT = pygame.font.SysFont("comicsans", 100)
LEVEL_FONT = pygame.font.SysFont("comicsans", 20)



ENEMY_IMAGE  = pygame.image.load("pictures/mine.png")
ME_IMAGE = pygame.image.load("pictures/me.png")
SEA_IMAGE = pygame.image.load("pictures/sea.png")
FLAG_IMAGE = pygame.image.load("pictures/flag.png")




ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_SIZE, ENEMY_SIZE))
ME = pygame.transform.scale(ME_IMAGE, (ME_SIZE, ME_SIZE))
SEA = pygame.transform.scale(SEA_IMAGE, (WIDTH, HEIGHT))
FLAG = pygame.transform.scale(FLAG_IMAGE, (ME_SIZE, ME_SIZE))