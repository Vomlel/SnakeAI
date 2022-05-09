# ---------------------------------------------------------------------------
# fitness funkce výpočty jednotlivců
# ----------------------------------------------------------------------------


# funkce pro výpočet fitness všech jedinců
def handle_mes_fitnesses(mes, flag):
    for me in mes:
        me.fitness = - (flag.rect.x - me.rect.x + flag.rect.y - me.rect.y) * 100
        #me.fitness = me.fitness + me.dist
        if me.won:
            me.fitness = me.fitness + 5000