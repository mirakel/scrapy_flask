from flask import Flask
from db.models import *
from flask import abort
from flask import request
from flask import jsonify

app = Flask(__name__)

POSTGRES = {
    'user':'postgres',
    'pw':'123456',
    'db': 'learning_flask',
    'host':'localhost',
    'port':'5433'
}

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'M#lOkNdmdAxaGS=GgEPl)&9_$JFNCE&djVLB30zwRwvMDQxFq&tTnv-)'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

@app.route('/')
def main():
    return 'Hello Api!'

@app.route('/api/seasons', methods = ['GET'])
def seasons():
    seasons = Season.query.order_by(Season.created.asc()).all()

    return jsonify([s.to_dict() for s in seasons])


@app.route('/api/episodes', methods = ['GET'])
def episodes():
    episodes = Episode.query.order_by(Episode.created.asc()).all()

    return jsonify([e.to_dict() for e in episodes])


@app.route('/api/seasons/<int:season_id>', methods =['GET'])
def get_season(season_id):
    season = Season.query.filter_by(id = season_id).first()
    if season is None:
        abort(404)

    return jsonify(season.to_dict())


@app.route('/api/episodes/<int:episode_id>', methods=['GET'])
def get_episodio(episode_id):
    episode = Episode.query.filter_by(id = episode_id).first()
    if episode is None:
        abort(404)

    return jsonify(episode.to_dict())

@app.route('/api/seasons/add', methods=['POST'])
def add_season():
    title = request.form['title']
    desc = request.form['description']
    season = Season(title, desc)
    db.session.add(season)
    db.session.commit()

    return jsonify({'success': True}), 201


@app.route('/api/episodes/add', methods=['POST'])
def add_episodio():
    title = request.form['title']
    sypnosis = request.form['sypnosis']
    url_video = request.form['url_video']
    url_img = request.form['url_img']
    season = request.form['seasonId']
    episodio = Episode(title, sypnosis, url_video, url_img, season)
    db.session.add(episodio)
    db.session.commit()

    return jsonify({'success': True}), 201


@app.route('/api/seasons/<int:season_id>', methods = ['DELETE'])
def delete_season(season_id):
    db.session.delete(Season.query.get(season_id))
    db.session.commit()

    return jsonify({'success': True})

@app.route('/api/episodes/<int:episode_id>', methods = ['DELETE'])
def delete_episode(episode_id):
    db.session.delete(Episode.query.get(episode_id))
    db.session.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()



"""
ref: https://www.theodo.fr/blog/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/
ref: http://blog.mmast.net/sqlalchemy-serialize-json

http://blog.vero4ka.info/blog/2017/01/20/flask-con-todas-las-arandelas/

"""
