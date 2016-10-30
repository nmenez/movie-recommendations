from pydelicious import get_popular, get_userposts, get_urlposts
import run_me
import time
from critics import critics


def initializeUserDict(tag, count=5):
    user_dict = {}
    # get the top count' popular posts
    for p1 in get_popular(tag=tag)[0:count]:

        for p2 in get_urlposts(p1['url']):
            user = p2['user']
            #print(p1['url'] + ' ' + user)
            user_dict[user] = {}
    return user_dict


def fillItems(user_dict):
    all_items = {}
    for user in user_dict:

        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print("Failed user " + user + ", retrying")

                time.sleep(4)

        try:

            for post in posts:

                url = post['url']
                user_dict[user][url] = 1.0
                all_items[url] = 1

        except:

            print('user: ' + user + ' has no posts')

    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item] = 0.0


delusers = initializeUserDict('programming', 10)
fillItems(delusers)

print(run_me.getRecommendations(delusers, 'wavyx'))
#print(run_me.topMatches(delusers,user) )
