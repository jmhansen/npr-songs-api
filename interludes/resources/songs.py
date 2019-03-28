from flask_restful import Resource

from interludes.models import Song
from interludes.schema import song_schema, songs_schema


class SongResource(Resource):
    def get(self, song_id):
        song = Song.query.get(song_id)
        data = song_schema.dump(song).data
        return data


class SongListResource(Resource):
    def get(self):
        songs = Song.query.all()
        data = songs_schema.dump(songs).data
        return data
