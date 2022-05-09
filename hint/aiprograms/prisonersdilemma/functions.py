import fighters


def rozdej_skore(tah1, tah2):
    # 1 = zradi, 0 = nezradi

    skores = (0, 0)

    if (tah1 == 1) and (tah2 == 1):
        skores = (2, 2)

    if (tah1 == 1) and (tah2 == 0):
        skores = (0, 3)

    if (tah1 == 0) and (tah2 == 1):
        skores = (3, 0)

    if (tah1 == 0) and (tah2 == 0):
        skores = (1, 1)

    return skores


def play(f1, f2, stepsnum):
    skore1 = 0
    skore2 = 0

    historie1 = []
    historie2 = []

    for i in range(stepsnum):
        tah1 = f1(historie1, historie2)
        tah2 = f2(historie2, historie1)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def playgenome(f1, f2, stepsnum):
    skore1 = 0
    skore2 = 0

    historie1 = []
    historie2 = []

    fighter1 = getattr(fighters, f1)
    fighter2 = getattr(fighters, f2)

    for i in range(stepsnum):
        tah1 = fighter1(historie1, historie2)
        tah2 = fighter2(historie2, historie1)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def playforgenome(f1, f2, stepsnum, genome):
    skore1 = 0
    skore2 = 0

    historie1 = []
    historie2 = []

    fighter1 = getattr(fighters, f1)
    fighter2 = getattr(fighters, f2)

    for i in range(stepsnum):
        tah1 = fighter1(historie1, historie2, genome)
        tah2 = fighter2(historie2, historie1)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def tournament(ucastnici, STEPSNUM):
    l = len(ucastnici)
    skores = [0 for i in range(l)]

    print("=========================================")
    print("Turnaj")
    print("hra délky:", STEPSNUM)
    print("-----------------------------------------")

    for i in range(l):
        for j in range(i + 1, l):
            f1 = ucastnici[i]
            f2 = ucastnici[j]
            skore1, skore2 = play(f1, f2, STEPSNUM)
            print(f1.__name__, "x", f2.__name__, " ", skore1, ":", skore2)
            skores[i] += skore1
            skores[j] += skore2

    print("=========================================")
    print("= Výsledné pořadí")
    print("-----------------------------------------")

    # setrideni indexu vysledku
    index = sorted(range(l), key=lambda k: skores[k])
    print(index)

    poradi = 1
    for i in index:
        f = ucastnici[i]
        print(poradi, ".", f.__name__, ":", skores[i])
        poradi += 1


def fight(ucastnici, STEPSNUM, genome):
    ourfighter = ucastnici[0]
    l = len(ucastnici)
    skores = [0 for i in range(l)]
    for i in range(l):
        for j in range(i + 1, l):
            f1 = ucastnici[i]
            f2 = ucastnici[j]
            if i == 0:
                skore1, skore2 = playforgenome(f1, f2, STEPSNUM, genome)
            else:
                skore1, skore2 = playgenome(f1, f2, STEPSNUM)
            skores[i] += skore1
            skores[j] += skore2

    index = sorted(range(l), key=lambda k: skores[k])

    for i in index:
        f = ucastnici[i]
        if f == ourfighter:
            return skores[i]


def fight2(ucastnici, STEPSNUM, genome):
    ourfighter = ucastnici[0]
    l = len(ucastnici)
    skores = [0 for i in range(l)]
    for i in range(l):
        for j in range(i + 1, l):
            f1 = ucastnici[i]
            f2 = ucastnici[j]
            if i == 0:
                skore1, skore2 = playforgenome(f1, f2, STEPSNUM, genome)
            else:
                skore1, skore2 = playgenome(f1, f2, STEPSNUM)
            skores[i] += skore1
            skores[j] += skore2

    index = sorted(range(l), key=lambda k: skores[k])

    if len(index) == 2:
        return index[0]
    else:
        if index[0] == len(index) - 1:
            return index[0]
        else:
            for i in range(len(index)):
                if index[i] == len(ucastnici) - 1:
                    print("i: " + i)
                    print("len ucastnici: " + len(ucastnici))
                    ucastnici.pop(i)
            return fight2(ucastnici, STEPSNUM, genome)
