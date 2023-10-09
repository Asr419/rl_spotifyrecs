import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-top-read"))

playlists = sp.current_user_top_tracks(limit=50)
print(playlists)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None