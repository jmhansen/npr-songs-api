import datetime

from slugify import slugify

from spotipy.client import SpotifyException
from sqlalchemy.sql import ClauseElement

from interludes.database import db
from interludes.models import Program, Episode, Artist, Song, Interlude
from interludes.utils.spotify_client import get_artist_thumbnail, get_song_preview


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance, True


def create_from_dict(song_dict):
    """
    example dict:
        {'date': 'April 20, 2016', '
        program': 'Morning Edition',
        'order': 19,
        'song_title': 'Delphium',
        'artist': 'Aphex Twin'}
    """
    session = db.session
    artist_name = song_dict['artist']
    song_name = song_dict['song_title']

    # check for empty artist and song keys
    if not (artist_name and song_name):
        return "skipping empty dictionary"

    # Check and reconcile known variations
    various = ['various artists', 'various']
    unknown = ['unknown artist', 'unknown']

    if artist_name.lower() in various:
        artist_name = 'Various Artists'

    if artist_name.lower() in unknown:
        artist_name = 'unknown'

    # Check for empty artist key
    if not artist_name:
        artist_name = 'no artist listed'

    # truncate artist names that violate max length on field
    if len(artist_name) > 125:
        artist_name = artist_name[:125]

    # get or create objects
    program, created = get_or_create(session, Program, name=song_dict['program'], slug=slugify(song_dict['program']))
    episode, created = get_or_create(session, Episode, program_id=program.id,
                                     date=datetime.datetime.strptime(song_dict['date'], '%B %d, %Y').date())
    artist, created = get_or_create(session, Artist, slug=slugify(artist_name), defaults={'name': artist_name})
    if created:
        try:
            get_artist_thumbnail(artist.id, session)
        except SpotifyException:
            pass
    song, created = get_or_create(session, Song, name=song_name, artist_id=artist.id)
    if created:
        try:
            get_song_preview(song.id, session)
        except SpotifyException:
            pass

    get_or_create(session, Interlude, song_id=song.id, order=song_dict['order'], episode_id=episode.id)


def create_from_list(list_of_dicts):

    for song_dict in list_of_dicts:
        _index = list_of_dicts.index(song_dict)
        print("Starting index {} of {}".format(_index, (len(list_of_dicts) - 1)))
        create_from_dict(song_dict=song_dict)
        print("Finished index {}".format(_index))

