# -*- coding: utf-8 -*-


import pygame
import random
import fitness
import parameters
import classes
import functions

from deap import base
from deap import creator
from deap import tools













        
    
    

    

# ----------------------------------------------------------------------------
# main loop 
# ----------------------------------------------------------------------------

def main():
    
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()

    toolbox.register("attr_rand", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_rand, parameters.DELKA_JEDINCE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # vlastni random mutace
    # <----- ZDE TODO vlastní mutace
    def mutRandom(individual, indpb):
        for i in range(len(individual)):
            if random.random() < indpb:
                if random.random() < 0.95:
                    if random.random() > 0.5:
                        individual[i] = individual[i] + random.random()
                    else:
                        individual[i] = individual[i] - random.random()
                else:
                    individual[i] = random.random()
        return individual,

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutRandom, indpb=0.05)
    toolbox.register("select", tools.selRoulette)
    toolbox.register("selectbest", tools.selBest)
    pop = toolbox.population(n=parameters.VELIKOST_POPULACE)

    # =====================================================================
    # testování hraním a z toho odvození fitness
    mines = []
    mes = functions.set_mes(parameters.VELIKOST_POPULACE)
    flag = classes.Flag()
    hof = classes.Hof()
    run = True
    level = 1   # <--- ZDE nastavení obtížnosti počtu min !!!!!
    generation = 0
    evolving = True
    timer = 0
    while run:
        # pokud evolvujeme pripravime na dalsi sadu testovani - zrestartujeme scenu
        if evolving:           
            timer = 0
            generation += 1
            functions.reset_mes(mes, pop) # přiřadí sekvence z populace jedincům a dá je na start !!!!
            mines = functions.set_mines(level)
            evolving = False
        timer += 1
        functions.check_mes_won(mes, flag)
        functions.handle_mes_movement(mes, mines, flag)
        functions.handle_mines_movement(mines)
        functions.mes_collision(mes, mines)
        if functions.all_dead(mes):
            evolving = True
        functions.update_mes_timers(mes, timer)
        functions.draw_window(mes, mines, flag, level, generation, timer)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # druhá část evoluce po simulaci, když všichni dohrají, simulace končí 1000 krocích
        if timer >= parameters.SIMSTEPS or functions.nobodys_playing(mes):
            # přepočítání fitness funkcí, dle dat uložených v jedinci
            fitness.handle_mes_fitnesses(mes, flag)
            functions.update_hof(hof, mes)
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
                if random.random() < parameters.CXPB:
                    toolbox.mate(child1, child2)
            for mutant in offspring:
                if random.random() < parameters.MUTPB:
                    toolbox.mutate(mutant)
            pop[:] = offspring
            evolving = True
    pygame.quit()    


if __name__ == "__main__":
    main()