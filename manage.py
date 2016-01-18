import os
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from config import DevelopmentConfig
from models import User
from app_factory import app, db

app.config.from_object(os.environ.get('APP_SETTINGS', DevelopmentConfig))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    return dict(app=app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == '__main__':
    manager.run()
