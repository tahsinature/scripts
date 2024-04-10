import spotipy
import osascript
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from time import sleep
import signal
import os

signal.signal(signal.SIGINT, signal.SIG_DFL)

scopes = ['user-read-currently-playing']
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

if not client_id or not client_secret:
    raise Exception('SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set')

spotify = spotipy.Spotify(
    oauth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:3000',
        scope=' '.join(scopes),
        client_id=client_id,
        client_secret=client_secret,
    ))


def get_currently_playing() -> dict:
    try:
        current = spotify.current_user_playing_track()
        if not current:
            return None

        type = current['currently_playing_type']

        d = {
            "type": type,
            "title": None,
            "artist": None,
            "album": None,
        }

        if type == 'track':
            d['title'] = current['item']['name']
            d['artist'] = current['item']['artists'][0]['name']
            d['album'] = current['item']['album']['name']
    except:
        return None

    return d


def toggle_system_mute(value: bool):
    osascript.osascript(f'set volume output muted {value}')


def is_muted() -> bool:
    return osascript.osascript('output muted of (get volume settings)')[1] == 'true'


if __name__ == '__main__':
    is_system_muted = is_muted()
    previous = None

    while True:
        sleep(1)
        current = get_currently_playing()

        if current is None or current == previous:
            continue

        previous = current
        currently_playing_type = current['type']

        print(f'Currently playing: {current}')
        toggle_system_mute(currently_playing_type == 'ad')
