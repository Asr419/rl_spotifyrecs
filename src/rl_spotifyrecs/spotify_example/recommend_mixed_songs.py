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
    scope='user-library-read user-read-playback-state user-read-currently-playing user-modify-playback-state playlist-modify-public playlist-modify-private'
))
print(SPOTIPY_CLIENT_ID)
# Get the user's saved tracks
saved_tracks = sp.current_user_saved_tracks(limit=50) 
print(saved_tracks) # Adjust the limit as needed
seed_tracks = [track['track']['uri'] for track in saved_tracks['items']]
seed_tracks = seed_tracks[:5]
print(seed_tracks)
# seed_tracks = [
#     'spotify:track:6rqhFgbbKwnb9MLmUQDhG6',  # Seed track 1
#     'spotify:track:3n3Ppam7vgaVa1iaRUc9Lp',  # Seed track 2
#     'spotify:track:1Ld7nZ9fN4BpkP4tymKkUj',  # Seed track 3
#     'spotify:track:7hDc8b7IXETo14hHIHdnhd',  # Seed track 4
#     'spotify:track:3a1lNhkSLSkpJE4MSHpDu9'   # Seed track 5
# ]
# print(seed_tracks) 
# Get Spotify recommendations
recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)


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

#AQCn5jbgg9UKgnm6YVcTVdzn3dq6q4L6kAsmaRR0kZf7RYyykqWvxtIVtwzzkI2rh6hYwID-SfCZWKQnq5R-uKDcs2Bu5TLHyuSlzWemot5r_1SuGiK5b3AcuQ0cKfXx1iFzBE8C73DXZu4ypwMzpKkkNXgjPrR9