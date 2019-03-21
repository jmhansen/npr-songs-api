import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from interludes.models import Artist, Song

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                      client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artist_thumbnail(artist_pk, session):
    artist = Artist.query.get(artist_pk)
    r = spotify.search(q='artist:' + artist.name, limit=1, type='artist')

    if len(r['artists']['items']) > 0:
        artist_dict = r['artists']['items'][0]
        if artist_dict['images'] and (len(artist_dict['images']) > 0):
            artist.thumbnail = artist_dict['images'][-1]['url']
            session.add(artist)
            session.commit()


def get_song_preview(song_pk, session):
    song = Song.query.get(song_pk)
    r = spotify.search(q='track:' + song.name + ' ' + 'artist:' + song.artist.name, limit=1, type='track')
    if (len(r['tracks']['items']) > 0) and (r['tracks']['items'][0]['preview_url']):
        track_dict = r['tracks']['items'][0]
        song.preview = track_dict['preview_url']
        session.add(song)
        session.commit()
