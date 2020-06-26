import json
import os
import subprocess
import sys

watchedfile = '/storage/automation/watchedbackup.json'

def findNextEpisode(json_data):

        #take first unplayed
        notplayed = [ep for ep in json_data if int(ep[u'playcount']) < 1]
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

def findEpisodePath(nextEpisode, episodes):
        for episode in episodes:
                if episode[u'label'].startswith(nextEpisode):
                        return episode[u'file']

def playNextEpisode(title):
        
        subprocess.call(['texturecache.py', 'watched', 'tvshows', 'backup', './automation/watchedbackup.json', title])

        path = getNextEpisodePath(title)
        
        subprocess.call(['texturecache.py', 'play', path])


def getNextEpisodePath(title):

        with open(watchedfile, 'r') as fd:
                json_data = json.load(fd)

        s, e = findNextEpisode(json_data)

        #load list of episodes for tv shows
        tvshows = subprocess.check_output(['texturecache.py', 'jd', 'tvshows', title])
        #print(tvshows)
        tvshowsjson = json.loads(tvshows)

        #flatten episodes into single list
        episodes = []
        for season in tvshowsjson[0][u'seasons']:
                episodes += season[u'episodes']

        nextEpisode = formatEpisode(s,e)

        file = findEpisodePath(nextEpisode, episodes)
        if file:
                return file
                exit(0)

        #if no next episode in current season, try first episode of next season
        nextEpisode = formatEpisode(s + 1, 1)

        file = findEpisodePath(nextEpisode, episodes)
        if file:
                return file
                exit(0)


        raise ValueError('Next episode not found')      

if __name__== "__main__":
        title = sys.argv[1]
        playNextEpisode(title)
       