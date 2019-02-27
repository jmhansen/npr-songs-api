import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jon.hansen@localhost/npr_music_local'

db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hey I'm using Docker!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
