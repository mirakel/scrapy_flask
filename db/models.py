from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
import json

db = SQLAlchemy()

class BaseModel(object):
    """ Para todos los modelos """

    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}

        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref = self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref = self.__table__) for i in value]

        return res


class Season(BaseModel, db.Model):
    """ Model for the Seasons table """

    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text)
    episodes = db.relationship('Episode', backref='season', lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, title, desc = None):
        self.title = title
        self.description = desc
        self.updated = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Episode(BaseModel, db.Model):
    """ Model for the Episodes table """

    __tablename__ = 'episodes'

    RELATIONSHIPS_TO_DICT = True

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180), nullable = False)
    title_original = db.Column(db.String(180), nullable = False)
    synopsis = db.Column(db.Text)
    url_video = db.Column(db.String(200))
    type_video = db.Column(db.String(80))
    name_video = db.Column(db.String(120))
    url_img = db.Column(db.String(200))
    season_id = db.Column('seasonId',db.Integer, db.ForeignKey('seasons.id'))
    n_episode = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, title, title_original, synopsis, season, n_episode = None, video = None, type_video = None, name = None, img = None):
        self.title = title
        self.title_original = title_original
        self.synopsis = synopsis
        self.url_video = video
        self.type_video = type_video
        self.name_video = name
        self.url_img = img
        self.season_id = season
        self.n_episode = n_episode
        self.updated = datetime.utcnow()
