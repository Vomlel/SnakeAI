# ----------------------------------------------------------------------------
# třídy objektů
# ----------------------------------------------------------------------------
import random
import parameters
import pygame

# trida reprezentujici minu
class Mine:
    def __init__(self):

        # random x direction
        if random.random() > 0.5:
            self.dirx = 1
        else:
            self.dirx = -1

        # random y direction
        if random.random() > 0.5:
            self.diry = 1
        else:
            self.diry = -1

        x = random.randint(200, parameters.WIDTH - parameters.ENEMY_SIZE)
        y = random.randint(200, parameters.HEIGHT - parameters.ENEMY_SIZE)
        self.rect = pygame.Rect(x, y, parameters.ENEMY_SIZE, parameters.ENEMY_SIZE)

        self.velocity = random.randint(1, parameters.MAX_MINE_VELOCITY)


# trida reprezentujici me, tedy meho agenta
class Me:
    def __init__(self):
        self.rect = pygame.Rect(10, random.randint(1, 300), parameters.ME_SIZE, parameters.ME_SIZE)
        self.alive = True
        self.won = False
        self.timealive = 0
        self.sequence = []
        self.fitness = 0
        self.dist = 0


# třída reprezentující cíl = praporek
class Flag:
    def __init__(self):
        self.rect = pygame.Rect(parameters.WIDTH - parameters.ME_SIZE, parameters.HEIGHT - parameters.ME_SIZE - 10, parameters.ME_SIZE, parameters.ME_SIZE)


# třída reprezentující nejlepšího jedince - hall of fame
class Hof:
    def __init__(self):
        self.sequence = []