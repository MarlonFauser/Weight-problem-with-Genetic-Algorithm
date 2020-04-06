from operator import itemgetter

GENERATION_PORCENTAGE = 50
GENERATION_TIMES = 3

CHOOSES_LEN = 5
MAX_WEIGHT = 30

ITEMS = [
    {"name": "Saco de dormir", "weight": 15, "points": 15},
    {"name": "Corda", "weight": 3, "points": 7},
    {"name": "Canivete", "weight": 2, "points": 10},
    {"name": "Tocha", "weight": 5, "points": 5},
    {"name": "Garrafa", "weight": 9, "points": 8},
    {"name": "Comida", "weight": 20, "points": 17}
]

generations = [
    {"chooses": [1, 0, 0, 1, 1, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 0, 1, 1, 1, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 1, 0, 1, 0, 0], "score": 0, "totalweight": 0},
    {"chooses": [0, 1, 1, 0, 0, 1], "score": 0, "totalweight": 0}
]


def setScoreAndTotalWeight(generations):
    filteredGenerations = []

    for generation in generations:
        alreadyCalculated = generation["score"] > 0 or generation["totalweight"] > 0
        if alreadyCalculated:
            filteredGenerations.append(generation)
            continue

        for i, choose in enumerate(generation["chooses"]):
            if choose:
                item = ITEMS[i]
                generation["score"] += item["points"]
                generation["totalweight"] += item["weight"]

        filteredGenerations.append(generation)

    return filteredGenerations


def getParents(generations):
    generations.sort(key=lambda generation: generation["score"], reverse=True)
    return generations[:(len(generations) * GENERATION_PORCENTAGE) // 100]


def getChildrens(parents):
    childrens = []

    for i in range(len(parents)):
        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 2, 4])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[1, 3, 5])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[1, 3, 5])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 2, 4])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 1, 2])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[3, 4, 5])
                                             (parents[i]["chooses"])))

        childrens.append({"chooses": [], "score": 0, "totalweight": 0})
        childrens[-1]["chooses"].extend(list(itemgetter(*[3, 4, 5])
                                             (parents[i-1]["chooses"])))
        childrens[-1]["chooses"].extend(list(itemgetter(*[0, 1, 2])
                                             (parents[i]["chooses"])))

    childrens = setScoreAndTotalWeight(childrens)
    return childrens


def getBestOne(generations):
    generations = list(
        filter(lambda generation: generation["totalweight"] <= MAX_WEIGHT, generations))

    if len(generations):
        generations.sort(
            key=lambda generation: generation["score"], reverse=True)
    else:
        return []

    return generations[0]


generations = setScoreAndTotalWeight(generations)
for time in range(GENERATION_TIMES):
    parents = getParents(generations)
    childrens = getChildrens(parents)
    print("Numero de gerações totais: " + str(len(generations)) + " >> Pais gerados: " +
          str(len(parents)) + " >> Filhos gerados: " + str(len(childrens)))
    generations.extend(childrens)

bestOne = getBestOne(generations)
print()
print("De " + str(len(generations)) + ", o melhor é: ")
print("Score: " + str(bestOne["score"]), end=', ')
print("Total weight: " + str(bestOne["totalweight"]))
print("Items: ", end='')

itemsName = [ITEMS[i]["name"]
             for i, choose in enumerate(bestOne["chooses"]) if choose]
print(itemsName)
