from interludes.database import ma
from interludes.models import Program, Episode, Artist, Song, Interlude


class ProgramSchema(ma.ModelSchema):
    class Meta:
        model = Program


program_schema = ProgramSchema()
programs_schema = ProgramSchema(many=True)


class EpisodeSchema(ma.ModelSchema):
    class Meta:
        model = Episode


episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)


class ArtistSchema(ma.ModelSchema):
    class Meta:
        model = Artist


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song


song_schema = SongSchema()
songs_schema = SongSchema(many=True)


class InterludeSchema(ma.ModelSchema):
    class Meta:
        model = Interlude


interlude_schema = InterludeSchema()
interludes_schema = InterludeSchema(many=True)
