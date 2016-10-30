from critics import critics
import recommendations as r

''' test sim ''' 
res = r.sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
print(res)

'''  test pearson '''
res = r.sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
print(res)


######## user based filtering
''' get recommendations '''
recs = r.getRecommendations(critics, 'Toby')
for score, movie in recs:
    print('%s: %0.2f' % (movie, score))


''' reverse prefs dict '''
print('\n')
movies = r.transformPrefs(critics)

matches = r.topMatches(movies, 'Superman Returns')
for score, movie in matches:
    print('%s: %0.2f' % (movie, score))

#####item based filtering

''' getting similar items '''
print('\nsimilar items')
print(r.transformPrefs(critics))

itemsim = r.calculateSimilarItems(critics, n=5)
print(itemsim['Lady in the Water'])


print(r.getRecommendedItems(critics, itemsim, 'Toby'))
