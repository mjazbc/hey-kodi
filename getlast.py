import json
import os
import subprocess
import sys

title = sys.argv[1]

watchedfile = '/storage/automation/watchedbackup.json'

with open(watchedfile, 'r') as fd:
        json_data = json.load(fd)

def findNextEpisode(json_data):
        #take first unplayed
        notplayed = [ep for ep in json_data if ep[u'playcount' < 1]]
        if len(notplayed) > 0:
                notplayed.sort(key=lambda x: x[u'episode_year'])
                nextepisode = notplayed[0][u'episode_year']
                season, episode = nextepisode.split('x')
                return int(season), int(episode)
        #if all episodes on list are played, calculate next
        else:
                json_data.sort(key=lambda x: x[u'episode_year'])
                lastplayedepisode = json_data[-1][u'episode_year']
                season, episode = lastplayedepisode.split('x')
                return int(season), int(episode) + 1

def formatEpisode(season, episode):
        return str.format('{0}x{1:02d}', season, episode)

s, e = findNextEpisode(json_data)

#load list of episodes for tv shows
tvshows = subprocess.check_output(['texturecache.py', 'jd', 'tvshows', title])
#print(tvshows)
tvshowsjson = json.loads(tvshows)

#flatten episodes into single list
episodes = []
for season in tvshowsjson[0][u'seasons']:
        episodes += season[u'episodes']

for episode in episodes:
    if episode[u'label'].startswith(formatEpisode(s,e)):
        file = episode[u'file']
        print(file)
        exit(0)

#if no next episode in current season, try first episode of next season
nextEpisode = formatEpisode(s + 1, 1)

for episode in episodes:
        if episode[u'label'].startswith(nextEpisode):
                file = episode[u'file']
                print(file)
                exit(0)


raise ValueError('Next episode not found')