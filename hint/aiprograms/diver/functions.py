# -----------------------------------------------------------------------------
# nastavení herního plánu
# -----------------------------------------------------------------------------
import classes
import parameters
import pygame
import senzors
import neural_network
import numpy as np


# rozestavi miny v danem poctu num
def set_mines(num):
    l = []
    for i in range(num):
        m = classes.Mine()
        l.append(m)

    return l


# inicializuje me v poctu num na start
def set_mes(num):
    l = []
    for i in range(num):
        m = classes.Me()
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


# ---------------------------------------------------------------------------
# funkce řešící pohyb agentů
# ----------------------------------------------------------------------------


# konstoluje kolizi 1 agenta s minama, pokud je kolize vraci True
def me_collision(me, mines):
    for mine in mines:
        if me.rect.colliderect(mine.rect):
            # pygame.event.post(pygame.event.Event(ME_HIT))
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

    if mine.dirx == 1 and mine.rect.x + mine.rect.width + mine.velocity > parameters.WIDTH:
        mine.dirx = -1

    if mine.diry == -1 and mine.rect.y - mine.velocity < 0:
        mine.diry = 1

    if mine.diry == 1 and mine.rect.y + mine.rect.height + mine.velocity > parameters.HEIGHT:
        mine.diry = -1

    mine.rect.x += mine.dirx * mine.velocity
    mine.rect.y += mine.diry * mine.velocity


# resi pohyb min
def handle_mines_movement(mines):
    for mine in mines:
        handle_mine_movement(mine)


# ----------------------------------------------------------------------------
# vykreslovací funkce
# ----------------------------------------------------------------------------


# vykresleni okna
def draw_window(mes, mines, flag, level, generation, timer):
    parameters.WIN.blit(parameters.SEA, (0, 0))

    t = parameters.LEVEL_FONT.render("level: " + str(level), 1, parameters.WHITE)
    parameters.WIN.blit(t, (10, parameters.HEIGHT - 30))

    t = parameters.LEVEL_FONT.render("generation: " + str(generation), 1, parameters.WHITE)
    parameters.WIN.blit(t, (150, parameters.HEIGHT - 30))

    t = parameters.LEVEL_FONT.render("alive: " + str(alive_mes_num(mes)), 1, parameters.WHITE)
    parameters.WIN.blit(t, (350, parameters.HEIGHT - 30))

    t = parameters.LEVEL_FONT.render("won: " + str(won_mes_num(mes)), 1, parameters.WHITE)
    parameters.WIN.blit(t, (500, parameters.HEIGHT - 30))

    t = parameters.LEVEL_FONT.render("timer: " + str(timer), 1, parameters.WHITE)
    parameters.WIN.blit(t, (650, parameters.HEIGHT - 30))

    parameters.WIN.blit(parameters.FLAG, (flag.rect.x, flag.rect.y))

    # vykresleni min
    for mine in mines:
        parameters.WIN.blit(parameters.ENEMY, (mine.rect.x, mine.rect.y))

    # vykresleni me
    for me in mes:
        if me.alive:
            parameters.WIN.blit(parameters.ME, (me.rect.x, me.rect.y))

    pygame.display.update()


def draw_text(text):
    t = parameters.BOOM_FONT.render(text, 1, parameters.WHITE)
    parameters.WIN.blit(t, (parameters.WIDTH // 2, parameters.HEIGHT // 2))

    pygame.display.update()
    pygame.time.delay(1000)


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

            inp.append(senzors.my_senzor(me, mines, flag))

            neural_network.nn_navigate_me(me, inp)


# updatuje timery jedinců
def update_mes_timers(mes, timer):
    for me in mes:
        if me.alive and not me.won:
            me.timealive = timer


# uloží do hof jedince s nejlepší fitness
def update_hof(hof, mes):
    l = [me.fitness for me in mes]
    ind = np.argmax(l)
    hof.sequence = mes[ind].sequence.copy()