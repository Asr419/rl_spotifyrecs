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
    scope=''
))

# Define the Spotify track URI you want to check
track_uri = 'spotify:track:3n3Ppam7vgaVa1iaRUc9Lp'

try:
    # Make the request to get the track information
    track_info = sp.track(track_uri)
    print(f"Track Name: {track_info['name']}")
    print(f"Artist(s): {', '.join([artist['name'] for artist in track_info['artists']])}")
    print(f"Album: {track_info['album']['name']}")
    print("Track is valid.")
except spotipy.SpotifyException as e:
    print(f"Track is invalid or does not exist.")
