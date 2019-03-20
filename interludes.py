import os

from flask_migrate import Migrate

from interludes import create_app
from interludes.database import db
from interludes.models import Program, Episode, Artist, Song, Interlude


app = create_app(config_name='local')
# migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Program=Program, Episode=Episode, Artist=Artist, Song=Song, Interlude=Interlude)
