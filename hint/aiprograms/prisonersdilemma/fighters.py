import random
import numpy as np


def always_cooperate(my_history, enemy_history):
    return 0


def random_answer(my_history, enemy_history):
    if random.random() < 0.5:
        return 1
    return 0


def thief_vomlel(my_history, other_history):
    count = len(other_history)
    if count == 0:
        return 0
    how_bad = sum(other_history) / (count + 1)
    rand = random.random()
    if (rand < how_bad):
        return 1
    else:
        return 0


def my_tactic1(myhistory, otherhistory):
    my1 = np.sum(myhistory)
    l = len(otherhistory)
    if l < 4:
        return 0
    if l >= 5 and l < 10:
        if np.sum(otherhistory) > 3:
            return 1

    # if my1*2 < l:
    #     return 1
    if l > 0 and otherhistory[l-1] == 1:
        return 1
    for0 = 0
    for1 = 0
    for i in range(l):
        if otherhistory[i] == 0:
            for0 = for0 + 1
        else:
            for1 = for1 + 1
    if for0 > for1:
        return 0
    else:
        return 1


def killer(my_history, enemy_history, genome):
    # genome = [1, 0, 1, 0, 1, 0, 1]
    # genome = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    # genome = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    games = len(enemy_history)
    if games == 0:
        return genome[0]
    elif games == 1:
        if enemy_history[0] == 0:
            return genome[1]
        else:
            return genome[2]
    else:
        enemy_moves = [enemy_history[games - 2], enemy_history[games - 1]]
        if enemy_moves[0] == 0:
            if enemy_moves[1] == 0:
                return genome[3]
            else:
                return genome[4]
        else:
            if enemy_moves[1] == 0:
                return genome[5]
            else:
                return genome[6]


# every time answer same way
def zeroclass(my_history, enemy_history, code):
    return code[0]


# code[1] is answer for 1, code[2] is answer for 0
def firstclass(my_history, enemy_history, code):
    l = len(enemy_history)
    if l == 0:
        return code[0]
    if enemy_history[l - 1] == 1:
        return code[1]
    else:
        return code[2]


# code[3] is answer for 11, code[4] is answer for 10, code[5] is answer for 01, code[6] is answer for 00
def secondclass(my_history, enemy_history, code):
    l = len(enemy_history)
    if l == 0:
        return code[0]
    if l == 1:
        return firstclass(my_history, enemy_history, [code[0], code[1], code[2]])
    else:
        if enemy_history[l - 2] == 1:
            if enemy_history[l - 1] == 1:
                return code[3]
            return code[4]
        if enemy_history[l - 1] == 1:
            return code[5]
        return code[6]


def fighter0(my_history, enemy_history):
    return zeroclass(my_history, enemy_history, [0])


def fighter1(my_history, enemy_history):
    return zeroclass(my_history, enemy_history, [1])


def fighter111(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [1, 1, 1])


def fighter011(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [0, 1, 1])


def fighter101(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [1, 0, 1])


def fighter110(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [1, 1, 0])


def fighter001(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [0, 0, 1])


def fighter010(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [0, 1, 0])


def fighter100(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [1, 0, 0])


def fighter000(my_history, enemy_history):
    return firstclass(my_history, enemy_history, [0, 0, 0])
