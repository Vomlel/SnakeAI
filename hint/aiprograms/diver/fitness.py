# ---------------------------------------------------------------------------
# fitness funkce výpočty jednotlivců
# ----------------------------------------------------------------------------


# funkce pro výpočet fitness všech jedinců
def handle_mes_fitnesses(mes, flag):
    for me in mes:
        me.fitness = 10000
        me.fitness = me.fitness - (flag.rect.x - me.rect.x + flag.rect.y - me.rect.y) * 100
        if me.won:
            me.fitness = me.fitness + 1000000
        # me.fitness = me.fitness + me.dist
        # if me.alive:
        #     me.fitness = me.fitness + 50