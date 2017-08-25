import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from ext.database import manager as database_manager
from ext.runner import run_scrapy
from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command("database", database_manager)

@manager.command
def scrapy():
    run_scrapy()


if __name__ == '__main__':
    manager.run()
