import os
import csv
from itertools import groupby
from math import sqrt
import pickle


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in si])

    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0

    r = num / den

    return r


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
    '''
    prefs: dict where keys are recommendors.  each value is itself a dict where keys are
    recommendations and values are scores. 
    e.g.
    critics = {'Lisa Rose': {'Lady in the Water': 2.5,
                         'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0,
                         'Superman Returns': 3.5,
                         'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0,
                            'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5,
                            'Superman Returns': 5.0,
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
                            }
    person: a recommedor in prefs
    similarity: a similarity metric
    '''
    totals = {}
    simSums = {}

    for other in prefs:

        if other == person:
            continue

        sim = similarity(prefs, person, other)
        if sim < 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim

    rankings = [(total / simSums[item], item)
                for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            result[item][person] = prefs[person][item]

    return result


def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print('%d / %d' % (c, len(itemPrefs)))
            # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    for item, rating in userRatings.items():
        for similarity, item2 in itemMatch[item]:
            if item2 in userRatings:
                continue

            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score / totalSim[item], item)
                for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens():
    data_dir = 'data//ml-20m'
    movieid_file = 'movies.csv'
    movieids = {}
    ratings = {}
    with open(data_dir + '//' + movieid_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movieid = int(row['movieId'])
            movie = row['title']
            genres = row['genres'].split('|')
            movieids[movieid] = {'id': movie, 'genres': genres}

    with open(data_dir + '//ratings.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for userid, userdata in groupby(reader, key=lambda row: row['userId']):
            ratings[userid] = {movieids[int(row['movieId'])]['id']: row['rating']
                               for row in userdata}

    return movieids, ratings


if __name__ == "__main__":
    movieids, ratings = loadMovieLens()
    pickle.dump(movieids, open('data//movieids.pkl', 'rb'))
    pickle.dump(ratings, open('data//ratings.pkl', 'rb'))

