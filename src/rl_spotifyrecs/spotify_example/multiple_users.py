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



# Authenticate and create Spotify API objects for each user
for user in Users:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-read-playback-state', username=user))
    sp_users.append(sp)

for i, sp in enumerate(sp_users):
    current_track = sp.current_playback()
    if current_track is not None:
        print(f"User {Users[i]} is listening to {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")
    else:
        print(f"User {Users[i]} is not currently listening to anything.")

# # Get the current playing track for each user using Spotify Web API
# for i, sp in enumerate(sp_users):
#     user_id = Users[i]
#     access_token = sp.auth_manager.get_access_token(as_dict=False)
#     headers = {"Authorization": f"Bearer {access_token}"}
    
#     response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    
#     if response.status_code == 200:
#         current_track = response.json()
#         if current_track.get('item'):
#             print(f"User {user_id} is listening to {current_track['item']['name']} by {current_track['item']['artists'][0]['name']}")
#         else:
#             print(f"User {user_id} is not currently listening to anything sorry.")
#     elif response.status_code == 204:
#         print(f"User {user_id} is not currently listening to anything sorry.")
#     else:
#         print(f"Error for User {user_id}: {response.status_code} - {response.text}")



