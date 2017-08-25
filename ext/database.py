from flask_script import Manager, prompt_bool
from app import db

manager = Manager(usage='Database operations')

@manager.command
def dropdb():
    """ Drops database tables """
    if prompt_bool('Estas seguro que quieres eliminar las tablas de la BD (True)'):
        db.drop_all()

@manager.command
def createdb():
     """ Creates database tables from sqlalchemy models """
     db.create_all()

@manager.command
def recreate():
    """ Recreate database tables """
    dropdb()
    createdb()
