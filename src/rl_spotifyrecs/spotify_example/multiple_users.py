import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
import requests
from dotenv import load_dotenv
load_dotenv()
# Define your Spotify API credentials

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI_CALLBACK")# This should match the one you set in your Spotify Developer Application
Users=os.getenv("USERS")

# If you used a comma-separated list:
Users = Users.split(",")


# Remove any empty or whitespace elements
Users = [element.strip() for element in Users if element.strip()]


# Create a list of user usernames or IDs


# Create a list to store the Spotify API objects for each user
sp_users = []
playlist_name = 'Playlist by Aayush'
playlist_description = 'A dynamic playlist'



# Authenticate and create Spotify API objects for each user
# for user in Users:
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-read-playback-state', username=user))
#     sp_users.append(sp)

for user in Users:
    

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-library-read user-read-playback-state user-read-currently-playing user-modify-playback-state playlist-modify-public playlist-modify-private', username=user))
    #get user playlist
    playlists = sp.user_playlists(user)
    #get user current track
    current_track = sp.current_playback()
    target_playlist = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            target_playlist = playlist
            break
    #delete playlist
    if current_track is not None:
        if target_playlist:
            sp.user_playlist_unfollow(user, target_playlist['id'])
     
        seed_tracks = [current_track['item']['uri']]
        print(f"User {user} is listening to {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")

        #get recommendations
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)
        all_tracks = recommendations['tracks']
        # print(all_tracks)
        # all_tracks = [item for item in all_tracks if 'track' in item]
        # Shuffle the combined tracks
        random.shuffle(all_tracks)

        playlist = sp.user_playlist_create(sp.me()['id'], name=playlist_name, public=True, description=playlist_description)
        # print(all_tracks)
        track_uris = [track['uri'] for track in all_tracks]
        
        sp.playlist_add_items(playlist['id'], track_uris)
    else:
        print(f"User {user} is not currently listening to anything.")




