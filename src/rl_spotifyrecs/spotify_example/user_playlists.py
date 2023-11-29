import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()
# Define your Spotify API credentials

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI_CALLBACK")
username = "31f55uwdngi55iadbqlvq6ewm64q"  # Aayush
# # username='sx3djnk4f14mgkeqr6swvj91l'
# print(sys.argv)
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# else:
#     print("Whoops, need a username!")
#     print("usage: python user_playlists.py [username]")
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# custom_cache_path = "/path/to/custom/cache/.cache-myapp"
#     sys.exit()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))
sprp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-recently-played"))

playlists = sp.user_playlists(username)

for playlist in playlists["items"]:
    print(playlist["name"])
for playlist in playlists["items"]:
    print("Playlist Name:", playlist["name"])
    print("Total Tracks:", playlist["tracks"]["total"])
    print("Tracks:")

    # Get the tracks in the playlist
    results = sp.playlist_tracks(playlist["id"])

    for track in results["items"]:
        track_name = track["track"]["name"]
        artist_names = [artist["name"] for artist in track["track"]["artists"]]
        artists = ", ".join(artist_names)
        print(f"{track_name} by {artists}")

    print("\n")
LIMIT = 50
# results = sp.current_user_saved_tracks(limit=50)
# print(results)

# # Iterate through the saved tracks and print their details
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     track_name = track['name']
#     artist_names = [artist['name'] for artist in track['artists']]
#     artists = ', '.join(artist_names)
#     print(f"{idx + 1}. {track_name} by {artists}")

# recently_played = sprp.current_user_recently_played(limit=50)

# # # Print the results
# # for item in recently_played['items']:
# #     track = item['track']
# #     print(f"Track Name: {track['name']}")
# #     print(f"Artist(s): {', '.join([artist['name'] for artist in track['artists']])}")
#     print()


# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# auth_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-top-read",username=username))

# playlists = sp.current_user_top_tracks(limit=50)
# print(playlists)
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None
