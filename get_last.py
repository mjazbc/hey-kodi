import json
import play_next
from datetime import datetime, timedelta

def getLast(file_path):
        with open(watchedfile, 'r') as fd:
                json_data = json.load(fd)

        last_played = max(episode[u'lastplayed'] for episode in json_data)
        last_played_ts = datetime.strptime(last_played, '%Y-%m-%d %H:%M:%S')

        if datetime.now() > last_played_ts + timedelta(hours=2):
                print(0)
        else:
                title = json_data[0][u'name']
                print(title)
                play_next.playNextEpisode(title)

if __name__== "__main__":
       watchedfile = '/storage/automation/watchedbackup.json'
       getLast(watchedfile)