# -*- coding: utf-8 -*-


import pygame
import numpy as np
import random
import math


from deap import base
from deap import creator
from deap import tools


pygame.font.init()


#-----------------------------------------------------------------------------
# Parametry hry 
#-----------------------------------------------------------------------------

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)


TITLE = "Boom Master"
pygame.display.set_caption(TITLE)

FPS = 800
ME_VELOCITY = 5
MAX_MINE_VELOCITY = 3



BOOM_FONT = pygame.font.SysFont("comicsans", 100)   
LEVEL_FONT = pygame.font.SysFont("comicsans", 20)   



ENEMY_IMAGE  = pygame.image.load("mine.png")
ME_IMAGE = pygame.image.load("me.png")
SEA_IMAGE = pygame.image.load("sea.png")
FLAG_IMAGE = pygame.image.load("flag.png")


ENEMY_SIZE = 50
ME_SIZE = 50

ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_SIZE, ENEMY_SIZE))
ME = pygame.transform.scale(ME_IMAGE, (ME_SIZE, ME_SIZE))
SEA = pygame.transform.scale(SEA_IMAGE, (WIDTH, HEIGHT))
FLAG = pygame.transform.scale(FLAG_IMAGE, (ME_SIZE, ME_SIZE))






# ----------------------------------------------------------------------------
# třídy objektů 
# ----------------------------------------------------------------------------

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

        x = random.randint(200, WIDTH - ENEMY_SIZE) 
        y = random.randint(200, HEIGHT - ENEMY_SIZE) 
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        
        self.velocity = random.randint(1, MAX_MINE_VELOCITY)

        
  
    
  
# trida reprezentujici me, tedy meho agenta        
class Me:
    def __init__(self):
        self.rect = pygame.Rect(10, random.randint(1, 300), ME_SIZE, ME_SIZE)  
        self.alive = True
        self.won = False
        self.timealive = 0
        self.sequence = []
        self.fitness = 0
        self.dist = 0

    
    
# třída reprezentující cíl = praporek    
class Flag:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - ME_SIZE, HEIGHT - ME_SIZE - 10, ME_SIZE, ME_SIZE)
        

# třída reprezentující nejlepšího jedince - hall of fame   
class Hof:
    def __init__(self):
        self.sequence = []
        
    
    
# -----------------------------------------------------------------------------    
# nastavení herního plánu    
#-----------------------------------------------------------------------------
    

# rozestavi miny v danem poctu num
def set_mines(num):
    l = []
    for i in range(num):
        m = Mine()
        l.append(m)
        
    return l
    

# inicializuje me v poctu num na start 
def set_mes(num):
    l = []
    for i in range(num):
        m = Me()
        l.append(m)
        
    return l

# zresetuje vsechny mes zpatky na start
def reset_mes(mes, pop):
    for i in range(len(pop)):
        me = mes[i]
        me.rect.x = 10
        me.rect.y = 10
        me.alive = True
        me.dist = 0
        me.won = False
        me.timealive = 0
        me.sequence = pop[i]
        me.fitness = 0



    

# -----------------------------------------------------------------------------    
# senzorické funkce 
# -----------------------------------------------------------------------------    




# TODO

def my_senzor(me, mines):
    # vzdalenosti od zdi - done
    # vzdalenost od cile
    # v jakem kvadrantu jsou miny
    # WIDTH, HEIGHT = 900, 500
    senzors = []
    senzors.append((WIDTH - me.rect.x)/WIDTH)
    senzors.append((HEIGHT - me.rect.y)/HEIGHT)
    senzors.append(me.rect.x/WIDTH)
    senzors.append(me.rect.y/HEIGHT)
    senzors.append((HEIGHT + WIDTH - me.rect.x - me.rect.y) / (HEIGHT + WIDTH))
    mine_cor = [0, 0, 0, 0]
    for mine in mines:
        if mine.rect.x > me.rect.x:
            if mine.rect.y > me.rect.y:
                mine_cor[3] = 1
            else:
                mine_cor[0] = 1
        else:
            if mine.rect.y > me.rect.y:
                mine_cor[2] = 1
            else:
                mine_cor[1] = 1
    senzors.append(mine_cor[0])
    senzors.append(mine_cor[1])
    senzors.append(mine_cor[2])
    senzors.append(mine_cor[3])
    # print(mine_cor)

    return senzors


# -----> ZDE je prostor pro vlastní senzorické funkce !!!!









# ---------------------------------------------------------------------------
# funkce řešící pohyb agentů
# ----------------------------------------------------------------------------


# konstoluje kolizi 1 agenta s minama, pokud je kolize vraci True
def me_collision(me, mines):    
    for mine in mines:
        if me.rect.colliderect(mine.rect):
            #pygame.event.post(pygame.event.Event(ME_HIT))
            return True
    return False
            
            
# kolidujici agenti jsou zabiti, a jiz se nebudou vykreslovat
def mes_collision(mes, mines):
    for me in mes: 
        if me.alive and not me.won:
            if me_collision(me, mines):
                me.alive = False
            
            
# vraci True, pokud jsou vsichni mrtvi Dave            
def all_dead(mes):    
    for me in mes: 
        if me.alive:
            return False
    
    return True


# vrací True, pokud již nikdo nehraje - mes jsou mrtví nebo v cíli
def nobodys_playing(mes):
    for me in mes: 
        if me.alive and not me.won:
            return False
    
    return True


# rika, zda agent dosel do cile
def me_won(me, flag):
    if me.rect.colliderect(flag.rect):
        return True
    
    return False


# vrací počet živých mes
def alive_mes_num(mes):
    c = 0
    for me in mes:
        if me.alive:
            c += 1
    return c



# vrací počet mes co vyhráli
def won_mes_num(mes):
    c = 0
    for me in mes: 
        if me.won:
            c += 1
    return c

         
    
# resi pohyb miny        
def handle_mine_movement(mine):
        
    if mine.dirx == -1 and mine.rect.x - mine.velocity < 0:
        mine.dirx = 1
       
    if mine.dirx == 1  and mine.rect.x + mine.rect.width + mine.velocity > WIDTH:
        mine.dirx = -1

    if mine.diry == -1 and mine.rect.y - mine.velocity < 0:
        mine.diry = 1
    
    if mine.diry == 1  and mine.rect.y + mine.rect.height + mine.velocity > HEIGHT:
        mine.diry = -1
         
    mine.rect.x += mine.dirx * mine.velocity
    mine.rect.y += mine.diry * mine.velocity


# resi pohyb min
def handle_mines_movement(mines):
    for mine in mines:
        handle_mine_movement(mine)


#----------------------------------------------------------------------------
# vykreslovací funkce 
#----------------------------------------------------------------------------


# vykresleni okna
def draw_window(mes, mines, flag, level, generation, timer):
    WIN.blit(SEA, (0, 0))   
    
    t = LEVEL_FONT.render("level: " + str(level), 1, WHITE)   
    WIN.blit(t, (10  , HEIGHT - 30))
    
    t = LEVEL_FONT.render("generation: " + str(generation), 1, WHITE)   
    WIN.blit(t, (150  , HEIGHT - 30))
    
    t = LEVEL_FONT.render("alive: " + str(alive_mes_num(mes)), 1, WHITE)   
    WIN.blit(t, (350  , HEIGHT - 30))
    
    t = LEVEL_FONT.render("won: " + str(won_mes_num(mes)), 1, WHITE)   
    WIN.blit(t, (500  , HEIGHT - 30))
    
    t = LEVEL_FONT.render("timer: " + str(timer), 1, WHITE)   
    WIN.blit(t, (650  , HEIGHT - 30))
    
    
    
    
    

    WIN.blit(FLAG, (flag.rect.x, flag.rect.y))    
         
    # vykresleni min
    for mine in mines:
        WIN.blit(ENEMY, (mine.rect.x, mine.rect.y))
        
    # vykresleni me
    for me in mes: 
        if me.alive:
            WIN.blit(ME, (me.rect.x, me.rect.y))
        
    pygame.display.update()



def draw_text(text):
    t = BOOM_FONT.render(text, 1, WHITE)   
    WIN.blit(t, (WIDTH // 2  , HEIGHT // 2))     
    
    pygame.display.update()
    pygame.time.delay(1000)







#-----------------------------------------------------------------------------
# funkce reprezentující neuronovou síť, pro inp vstup a zadané váhy wei, vydá
# čtveřici výstupů pro nahoru, dolu, doleva, doprava    
#----------------------------------------------------------------------------


# <----- ZDE je místo vlastní funkci !!!!



# funkce reprezentující výpočet neuronové funkce
# funkce dostane na vstupu vstupy neuronové sítě inp, a váhy hran wei
# vrátí seznam hodnot výstupních neuronů
def nn_function(inp, wei):
    # print(inp)
    prahy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    prahy_for_omega = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cil = [0, 0, 0, 0]
    index = 0
    for i in range(9):
        for j in range(10):
            # print(index)
            prahy_for_omega[j] = prahy_for_omega[j] + inp[0][i] * wei[index]
            index = index + 1
    for i in range(10):
        if prahy_for_omega[i] >= wei[i + 90]:
            prahy[i] = 1
    for i in range(10):
        for j in range(4):
            if i == 0:
                cil[j] = cil[j] + prahy[i] * wei[j + 50]
            if i == 1:
                cil[j] = cil[j] + prahy[i] * wei[j + 54]
            if i == 2:
                cil[j] = cil[j] + prahy[i] * wei[j + 58]
            if i == 3:
                cil[j] = cil[j] + prahy[i] * wei[j + 62]
            if i == 4:
                cil[j] = cil[j] + prahy[i] * wei[j + 66]
    max_value = max(cil)
    for i in range(4):
        if cil[i] == max_value:
            # print("cil " + str(cil))
            # print("max_value " + str(max_value))
            return [i]


# naviguje jedince pomocí neuronové sítě a jeho vlastní sekvence v něm schované
def nn_navigate_me(me, inp):
       
    
    # TODO  <------ ZDE vlastní kód vyhodnocení výstupů z neuronové sítě !!!!!!
    
    out = np.array(nn_function(inp, me.sequence))
    # print(out)
    ind = out[0]
    # print(me.sequence)
    
    # nahoru, pokud není zeď
    if ind == 0 and me.rect.y - ME_VELOCITY > 0:
        me.rect.y -= ME_VELOCITY
        me.dist += ME_VELOCITY
    
    # dolu, pokud není zeď
    if ind == 1 and me.rect.y + me.rect.height + ME_VELOCITY < HEIGHT:
        me.rect.y += ME_VELOCITY  
        me.dist += ME_VELOCITY
    
    # doleva, pokud není zeď
    if ind == 2 and me.rect.x - ME_VELOCITY > 0:
        me.rect.x -= ME_VELOCITY
        me.dist += ME_VELOCITY
        
    # doprava, pokud není zeď    
    if ind == 3 and me.rect.x + me.rect.width + ME_VELOCITY < WIDTH:
        me.rect.x += ME_VELOCITY
        me.dist += ME_VELOCITY
    
    
        

# updatuje, zda me vyhrali 
def check_mes_won(mes, flag):
    for me in mes: 
        if me.alive and not me.won:
            if me_won(me, flag):
                me.won = True
    


# resi pohyb mes
def handle_mes_movement(mes, mines, flag):
    
    for me in mes:

        if me.alive and not me.won:
            
            # <----- ZDE  sbírání vstupů ze senzorů !!!
            # naplnit vstup in vstupy ze senzorů
            inp = []
            
            inp.append(my_senzor(me, mines))
            
            
            nn_navigate_me(me, inp)



# updatuje timery jedinců
def update_mes_timers(mes, timer):
    for me in mes:
        if me.alive and not me.won:
            me.timealive = timer



# ---------------------------------------------------------------------------
# fitness funkce výpočty jednotlivců
#----------------------------------------------------------------------------



# funkce pro výpočet fitness všech jedinců
def handle_mes_fitnesses(mes):    
    
    # <--------- TODO  ZDE se počítá fitness jedinců !!!!
    # na základě informací v nich uložených, či jiných vstupů
    for me in mes:
        # me.fitness = (me.rect.x + me.rect.y)*100
        # if me.alive:
        #     me.fitness = me.fitness + 1000
        # if me.won:
        #     me.fitness = 1000000
        if me.won  == True:
            me.fitness = 100000
        me.fitness = me.fitness + (me.rect.x + me.rect.y)*100
        if me.alive == False:
            me.fitness = me.fitness - 200
        if me.rect.x >= WIDTH - 10:
            if me.rect.y <= 10:
                me.fitness = me.fitness - 1000
        if me.rect.x <= 10:
            if me.rect.y >= HEIGHT - 10:
                me.fitness = me.fitness - 1000
        if me.rect.x <= 10:
            if me.rect.y <= 10:
                me.fitness = me.fitness - 1000
        # elif me.alive == True:
        #     me.fitness = 5000 + me.timealive + me.dist
        # else:
        #     me.fitness = me.timealive + me.dist
    
    

# uloží do hof jedince s nejlepší fitness
def update_hof(hof, mes):
    l = [me.fitness for me in mes]
    ind = np.argmax(l)
    hof.sequence = mes[ind].sequence.copy()
    

# ----------------------------------------------------------------------------
# main loop 
# ----------------------------------------------------------------------------

def main():
    
    
    # =====================================================================
    # <----- ZDE Parametry nastavení evoluce !!!!!
    
    VELIKOST_POPULACE = 10
    EVO_STEPS = 5  # pocet kroku evoluce
    DELKA_JEDINCE = 100   # <--------- záleží na počtu vah a prahů u neuronů !!!!!
    NGEN = 30        # počet generací
    CXPB = 0.6          # pravděpodobnost crossoveru na páru
    MUTPB = 0.2        # pravděpodobnost mutace
    
    SIMSTEPS = 400
    
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()

    toolbox.register("attr_rand", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_rand, DELKA_JEDINCE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # vlastni random mutace
    # <----- ZDE TODO vlastní mutace
    def mutRandom(individual, indpb):
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = random.random()
        return individual,

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutRandom, indpb=0.05)
    toolbox.register("select", tools.selRoulette)
    toolbox.register("selectbest", tools.selBest)
    
    pop = toolbox.population(n=VELIKOST_POPULACE)
        
    # =====================================================================
    
    clock = pygame.time.Clock()

    
    
    # =====================================================================
    # testování hraním a z toho odvození fitness 
   
    
    mines = []
    mes = set_mes(VELIKOST_POPULACE)    
    flag = Flag()
    
    hof = Hof()
    
    
    run = True

    level = 5   # <--- ZDE nastavení obtížnosti počtu min !!!!!
    generation = 0
    
    evolving = True
    evolving2 = False
    timer = 0
    
    while run:  
        
        # clock.tick(FPS)
        
               
        # pokud evolvujeme pripravime na dalsi sadu testovani - zrestartujeme scenu
        if evolving:           
            timer = 0
            generation += 1
            reset_mes(mes, pop) # přiřadí sekvence z populace jedincům a dá je na start !!!!
            mines = set_mines(level) 
            evolving = False
            
        timer += 1    
            
        check_mes_won(mes, flag)
        handle_mes_movement(mes, mines, flag)
        
        
        handle_mines_movement(mines)
        
        mes_collision(mes, mines)
        
        if all_dead(mes):
            evolving = True
            #draw_text("Boom !!!")"""

            
        update_mes_timers(mes, timer)        
        draw_window(mes, mines, flag, level, generation, timer)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    

        
        
        
        
        # ---------------------------------------------------------------------
        # <---- ZDE druhá část evoluce po simulaci  !!!!!
        
        # druhá část evoluce po simulaci, když všichni dohrají, simulace končí 1000 krocích

        if timer >= SIMSTEPS or nobodys_playing(mes): 
            
            # přepočítání fitness funkcí, dle dat uložených v jedinci
            handle_mes_fitnesses(mes)   # <--------- ZDE funkce výpočtu fitness !!!!
            
            update_hof(hof, mes)
            
            
            #plot fitnes funkcí
            #ff = [me.fitness for me in mes]
            
            #print(ff)
            
            # přiřazení fitnessů z jedinců do populace
            # každý me si drží svou fitness, a každý me odpovídá jednomu jedinci v populaci
            for i in range(len(pop)):
                ind = pop[i]
                me = mes[i]
                ind.fitness.values = (me.fitness, )
            
            
            # selekce a genetické operace
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))
            

            
            
            

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)  
            
            pop[:] = offspring
            
            
            evolving = True
                   
        
    # po vyskočení z cyklu aplikace vytiskne DNA sekvecni jedince s nejlepší fitness
    # a ukončí se
    
    pygame.quit()    


if __name__ == "__main__":
    main()