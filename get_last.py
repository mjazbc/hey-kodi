import json
import play_next
from datetime import datetime, timedelta

def getLast(file_path):
        try:
                with open(file_path, 'r') as fd:
                        json_data = json.load(fd)

                last_played = max(episode[u'lastplayed'] for episode in json_data)
                last_played_ts = datetime.strptime(last_played, '%Y-%m-%d %H:%M:%S')

                if datetime.now() > last_played_ts + timedelta(hours=2):
                        print(0)
                else:
                        title = json_data[0][u'name']
                        print(title)
                        play_next.playNextEpisode(title)
        except IOError:
                return

if __name__== "__main__":
       watchedfile = '.cache/watched.json'
       getLast(watchedfile)