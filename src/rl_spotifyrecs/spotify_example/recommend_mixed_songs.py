import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
from dotenv import load_dotenv
load_dotenv()


SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
# Initialize Spotipy with your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='playlist-modify-public'
))

# Get the user's saved tracks
saved_tracks = sp.current_user_saved_tracks(limit=50)  # Adjust the limit as needed
seed_tracks = [track['track']['uri'] for track in saved_tracks['items']]
seed_tracks = seed_tracks[:5]
# print(seed_tracks) 
# Get Spotify recommendations
recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)
# recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10) 
#print(recommendations)
# try:
#     # Make the request to Spotify recommendations
#     recommendations = sp.recommendations(seed_tracks=['track_id_1', 'track_id_2'], limit=10)
# except spotipy.SpotifyException as e:
#     print(f"Spotify API error: {e}")
#     print(f"HTTP status code: {e.http_status}")
#     print(f"Error reason: {e.reason}")
#     print(f"Error message: {e.msg}") # Adjust the limit as needed

# Combine saved tracks and recommendations
all_tracks = saved_tracks['items'] + recommendations['tracks']
all_tracks = [item for item in all_tracks if 'track' in item]

# Shuffle the combined tracks
random.shuffle(all_tracks)

# Create a new playlist
playlist_name = 'Recommended Playlist'
playlist_description = 'A playlist created from saved tracks and recommendations'
playlist = sp.user_playlist_create(sp.me()['id'], name=playlist_name, public=True, description=playlist_description)

# Add tracks to the playlist
track_uris = [track['track']['uri'] for track in all_tracks]
sp.playlist_add_items(playlist['id'], track_uris)

print(f'Playlist created: {playlist_name}')