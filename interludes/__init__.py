import os

from flask import Flask
from flask_migrate import Migrate

from interludes.config import config
from interludes.database import db
from interludes.models import Program, Episode, Artist, Song, Interlude


def create_app(config_name):
    """
    The flask application factory. To run the app somewhere else you can:

        from api import create_app
        app = create_app()
        if __main__ == "__name__":
            app.run()
    """
    app = Flask(__name__)
    app.config.from_object(config['local'])
    config['local'].init_app(app)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jon.hansen@localhost/npr_music_local'

    # register sqlalchemy
    db.init_app(app)
    migrate = Migrate(app, db)

    # import and register blueprints
    from interludes.views import main
    app.register_blueprint(main.main)

    return app
