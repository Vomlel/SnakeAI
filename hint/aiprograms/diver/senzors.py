# -----------------------------------------------------------------------------
# senzorické funkce
# -----------------------------------------------------------------------------

import parameters



# TODO
WIDTH = parameters.WIDTH
HEIGHT = parameters.HEIGHT


def my_senzor(me, mines, flag):
    # vzdalenosti od zdi - done
    # vzdalenost od cile
    # v jakem kvadrantu jsou miny
    # WIDTH, HEIGHT = 900, 500
    senzors = []
    senzors.append(me.rect.x / WIDTH)
    senzors.append(me.rect.y / HEIGHT)
    senzors.append(flag.rect.x / WIDTH)
    senzors.append(flag.rect.y / HEIGHT)
    mine_cor = [0] * 8
    myx = me.rect.x
    myy = me.rect.y
    for mine in mines:
        minex = mine.rect.x - myx
        miney = mine.rect.y - myy
    #     is in circle
        if abs(minex)**2 + abs(miney)**2 < 40000:
    #         which 1/4
            if minex >= 0 and miney >= 0:
    #             which 1/8
                if minex > miney:
                    mine_cor[7] = 1
                else:
                    mine_cor[6] = 1
            elif minex <= 0 and miney >= 0:
                if miney > abs(minex):
                    mine_cor[5] = 1
                else:
                    mine_cor[4] = 1
            elif minex <= 0 and miney <= 0:
                if abs(minex) > abs(miney):
                    mine_cor[3] = 1
                else:
                    mine_cor[2] = 1
            else:
                if abs(miney) > minex:
                    mine_cor[1] = 1
                else:
                    mine_cor[0] = 1
    for i in range(8):
        senzors.append(mine_cor[i])

    return senzors