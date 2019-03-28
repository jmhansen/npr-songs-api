from flask_restful import Resource

from interludes.models import Artist
from interludes.schema import artist_schema, artists_schema


class ArtistResource(Resource):
    def get(self, artist_id):
        artist = Artist.query.get(artist_id)
        data = artist_schema.dump(artist).data
        return data


class ArtistListResource(Resource):
    def get(self):
        artists = Artist.query.all()
        data = artists_schema.dump(artists).data
        return data
