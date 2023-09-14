import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
# username='7blo8ovgelmvittn4ht2uqvjt'#Aayush
username='sx3djnk4f14mgkeqr6swvj91l'
# print(sys.argv)
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Whoops, need a username!")
#     print("usage: python user_playlists.py [username]")
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#     sys.exit()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

playlists = sp.user_playlists(username)

# for playlist in playlists['items']:
#     print(playlist['name'])
for playlist in playlists['items']:
    print("Playlist Name:", playlist['name'])
    print("Total Tracks:", playlist['tracks']['total'])
    print("Tracks:")
    
    # Get the tracks in the playlist
    results = sp.playlist_tracks(playlist['id'])
    
    for track in results['items']:
        track_name = track['track']['name']
        artist_names = [artist['name'] for artist in track['track']['artists']]
        artists = ', '.join(artist_names)
        print(f"{track_name} by {artists}")
    
    print("\n")
LIMIT=50
results = sp.current_user_saved_tracks(limit=LIMIT)

# Iterate through the saved tracks and print their details
for idx, item in enumerate(results['items']):
    track = item['track']
    track_name = track['name']
    artist_names = [artist['name'] for artist in track['artists']]
    artists = ', '.join(artist_names)
    print(f"{idx + 1}. {track_name} by {artists}")