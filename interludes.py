import os

from flask_migrate import Migrate

from dotenv import load_dotenv

from interludes import create_app
from interludes.database import db
from interludes.models import Program, Episode, Artist, Song, Interlude


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(config_name='local')
# migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Program=Program, Episode=Episode, Artist=Artist, Song=Song, Interlude=Interlude)
