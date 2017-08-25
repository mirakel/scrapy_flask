from db.models import *
from scrapy.gameofthrones import *
import json
from sqlalchemy import and_

def run_scrapy():
    # save info seasons
    seasons = json.loads(info_seasons())
    for s in seasons:
        season = Season(s['title'])
        db.session.add(season)
        db.session.commit()

    # Save info episodes
    episodes = json.loads(info_episodes())
    for e in episodes:
        episode = Episode(e['title'], e['title_original'], e['synopsis'], e['seasonId'], e['n_episode'])
        db.session.add(episode)
        db.session.commit()

    # save videos, update table episodes
    info_video = info_videos()
    videos = info_video['result']['files']
    for video in videos:
        img = get_splash(video['linkextid'])
        s, e = video['name'].split('.')[0].split('x') # season1,1
        conds = [Episode.season_id == s.split('season')[1], Episode.n_episode == e]
        episode = Episode.query.filter(and_(*conds)).first()
        if episode is not None:
            episode.url_video = video['link']
            episode.name_video = video['name']
            episode.type_video = video['content_type']
            episode.url_img = img['result']
            db.session.commit()

    print('ok!')
