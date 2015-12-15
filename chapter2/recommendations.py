# coding: utf-8

from math import sqrt


critics = {
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                  'Just My Luck': 3.0, 'Superman Returns': 3.5,
                  'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                     'Just My Luck': 1.5, 'Superman Returns': 5.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                     'The Night Listener': 4.5, 'Superman Returns': 4.0,
                     'You, Me and Dupree': 2.5},
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                     'Just My Luck': 2.0, 'Superman Returns': 3.0,
                     'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                      'The Night Listener': 3.0, 'Superman Returns': 5.0,
                      'You, Me and Dupree': 3.5},
    'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0,
             'Superman Returns': 4.0}
}


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum(pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in si)
    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    sum1 = sum(prefs[person1][item] for item in si)
    sum2 = sum(prefs[person2][item] for item in si)

    sum1_sq = sum(pow(prefs[person1][item], 2) for item in si)
    sum2_sq = sum(pow(prefs[person2][item], 2) for item in si)

    p_sum = sum(prefs[person1][item] * prefs[person2][item] for item in si)

    num = p_sum - sum1 * sum2 / n
    den = sqrt((sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    return list(reversed(sorted(scores)))[:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}
    for other in prefs:
        if other == person:
            continue

        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    rankings = [(total / sim_sums[item], item)
                for item, total in totals.items()]
    return list(reversed(sorted(rankings)))
