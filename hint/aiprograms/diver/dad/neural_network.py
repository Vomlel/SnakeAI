#-----------------------------------------------------------------------------
# funkce reprezentující neuronovou síť, pro inp vstup a zadané váhy wei, vydá
# čtveřici výstupů pro nahoru, dolu, doleva, doprava
#----------------------------------------------------------------------------


# <----- ZDE je místo vlastní funkci !!!!

# funkce reprezentující výpočet neuronové funkce
# funkce dostane na vstupu vstupy neuronové sítě inp, a váhy hran wei
# vrátí seznam hodnot výstupních neuronů
import numpy as np
import parameters


def nn_function(inp, wei):
    # go inside first level of neural network
    # print(parameters.DELKA_JEDINCE)
    prahy = [0] * parameters.NEURAL_WIDTH
    inp_prahy = [0] * parameters.NEURAL_WIDTH
    for i in range(parameters.NEURAL_INPUTS):
        for j in range(parameters.NEURAL_WIDTH):
            prahy[j] = prahy[j] + inp[0][i] * wei[i * parameters.NEURAL_WIDTH + j]
    for i in range(parameters.NEURAL_WIDTH):
        if prahy[i] > wei[i + parameters.NEURAL_INPUTS * parameters.NEURAL_WIDTH]:
            inp_prahy[i] = 1
    for d in range(parameters.NEURAL_DEEP - 1):
        prahy = [0] * parameters.NEURAL_WIDTH
        index = parameters.NEURAL_WIDTH + parameters.NEURAL_INPUTS * parameters.NEURAL_WIDTH + d * (parameters.NEURAL_WIDTH + parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH)
        for i in range(parameters.NEURAL_WIDTH):
            for j in range(parameters.NEURAL_WIDTH):
                prahy[j] = prahy[j] + inp_prahy[i] * wei[index + i * parameters.NEURAL_WIDTH + j]
        inp_prahy = [0] * parameters.NEURAL_WIDTH
        for i in range(parameters.NEURAL_WIDTH):
            # print(i + index + parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH)
            if prahy[i] > wei[i + index + parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH]:
                inp_prahy[i] = 1
    # print(parameters.NEURAL_WIDTH + parameters.NEURAL_WIDTH + parameters.NEURAL_INPUTS * parameters.NEURAL_WIDTH  + parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH)
    cil = [0] * 4
    index = 0
    for i in range(parameters.NEURAL_WIDTH):
        for j in range(4):
            # print(parameters.NEURAL_INPUTS * parameters.NEURAL_WIDTH + parameters.NEURAL_WIDTH * parameters.NEURAL_DEEP + (parameters.NEURAL_DEEP - 1) * parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH + index)
            cil[j] = cil[j] + inp_prahy[i] * wei[parameters.NEURAL_INPUTS * parameters.NEURAL_WIDTH + parameters.NEURAL_WIDTH * parameters.NEURAL_DEEP + (parameters.NEURAL_DEEP - 1) * parameters.NEURAL_WIDTH * parameters.NEURAL_WIDTH + index]
            index = index + 1
    max_value = max(cil)
    for i in range(4):
        if cil[i] == max_value:
            return [i]


# naviguje jedince pomocí neuronové sítě a jeho vlastní sekvence v něm schované
def nn_navigate_me(me, inp):


    # TODO  <------ ZDE vlastní kód vyhodnocení výstupů z neuronové sítě !!!!!!

    out = np.array(nn_function(inp, me.sequence))
    #print(out)
    ind = out[0]
    #print(me.sequence)

    # nahoru, pokud není zeď
    if ind == 0 and me.rect.y - parameters.ME_VELOCITY > 0:
        me.rect.y -= parameters.ME_VELOCITY
        me.dist += parameters.ME_VELOCITY

    # dolu, pokud není zeď
    if ind == 1 and me.rect.y + me.rect.height + parameters.ME_VELOCITY < parameters.HEIGHT:
        me.rect.y += parameters.ME_VELOCITY
        me.dist += parameters.ME_VELOCITY

    # doleva, pokud není zeď
    if ind == 2 and me.rect.x - parameters.ME_VELOCITY > 0:
        me.rect.x -= parameters.ME_VELOCITY
        me.dist += parameters.ME_VELOCITY

    # doprava, pokud není zeď
    if ind == 3 and me.rect.x + me.rect.width + parameters.ME_VELOCITY < parameters.WIDTH:
        me.rect.x += parameters.ME_VELOCITY
        me.dist += parameters.ME_VELOCITY