import os

from flask import Flask
from flask_migrate import Migrate

from interludes.config import config
from interludes.database import db, migrate, ma
from interludes.models import Program, Episode, Artist, Song, Interlude
from interludes.resources import api
from interludes.resources.songs import SongResource, SongListResource
from interludes.resources.artists import ArtistResource, ArtistListResource
from interludes.resources.programs import ProgramResource, ProgramListResource


def create_app():
    """
    The flask application factory. To run the app somewhere else you can:

        from api import create_app
        app = create_app()
        if __main__ == "__name__":
            app.run()
    """
    environment = os.getenv('FLASK_CONFIG')
    app = Flask(__name__)
    app.config.from_object(config[environment])
    config[environment].init_app(app)

    # register sqlalchemy
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # import and register blueprints
    from interludes.views import main
    app.register_blueprint(main.main)

    # register api
    api.add_resource(ArtistResource, '/artists/<artist_id>')
    api.add_resource(ArtistListResource, '/artists')
    api.add_resource(ProgramResource, '/programs/<program_id>')
    api.add_resource(ProgramListResource, '/programs')
    api.add_resource(SongResource, '/songs/<song_id>')
    api.add_resource(SongListResource, '/songs')

    api.init_app(app)

    return app
