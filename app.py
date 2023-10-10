from flask import Flask, request, jsonify, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
from dotenv import load_dotenv
import random

app = Flask(__name__)
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


# Initialize an empty DataFrame to store the events
event_df = pd.DataFrame(columns=["user_id", "song_selected"])

@app.route('/')
def home():
    return 'Welcome to your Flask app'

@app.route('/favicon.ico')
def favicon():
    return "", 404

@app.route("/callback", methods=["POST"])
def callback():
    # Parse the JSON data sent by Spotify
    data = request.json

    # Extract relevant information (user ID and song selected)
    user_id = data.get("user_id")
    song_selected = data.get("song_selected")

    # Log the event in the DataFrame
    global event_df
    event_df = event_df.append({"user_id": user_id, "song_selected": song_selected}, ignore_index=True)
    event_df.to_csv("event_log.csv", index=False) 
    # You can also perform additional processing or actions here

    return "Event received and logged."

@app.route('/login')
def login():
    return redirect(sp.auth_manager.get_authorize_url())

# Handle the Spotify callback
@app.route('/authentication')
def authentication():
    sp.auth_manager.get_access_token(request.args['code'])
    return "Successfully authenticated with Spotify. You can now access user data."


@app.route('/recommend', methods=['GET','POST'])
def recommend():
    saved_tracks = sp.current_user_saved_tracks(limit=50)  # Adjust the limit as needed
    seed_tracks = [track['track']['uri'] for track in saved_tracks['items']]
    # print(seed_tracks)
    seed_tracks = seed_tracks[:5]
    # print(seed_tracks)
    seed_tracks = [
    'spotify:track:6rqhFgbbKwnb9MLmUQDhG6',  # Seed track 1
    'spotify:track:3n3Ppam7vgaVa1iaRUc9Lp',  # Seed track 2
    'spotify:track:1Ld7nZ9fN4BpkP4tymKkUj',  # Seed track 3
    'spotify:track:7hDc8b7IXETo14hHIHdnhd',  # Seed track 4
    'spotify:track:3a1lNhkSLSkpJE4MSHpDu9'   # Seed track 5
]
    # print(seed_tracks) 
    # Get Spotify recommendations
    
    
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=10)
    print("Tracks added to the playlist successfully.")
   
    
    all_tracks = saved_tracks['items'] + recommendations['tracks']
    all_tracks = [item for item in all_tracks if 'track' in item]

    # Shuffle the combined tracks
    random.shuffle(all_tracks)

    # Create a new playlist
    playlist_name = 'Recommended Playlist by Aayush'
    playlist_description = 'A playlist created from saved tracks and recommendations'
    playlist = sp.user_playlist_create(sp.me()['id'], name=playlist_name, public=True, description=playlist_description)

    # Add tracks to the playlist
    
    track_uris = [track['track']['uri'] for track in all_tracks]
    payload = {
    "uris": track_uris
    }
    sp.playlist_add_items(playlist['id'], track_uris)

    print(f'Playlist created: {playlist_name}')
    return f"Playlist created: {playlist_name}"

@app.route('/playlist-interaction', methods=['POST'])
def playlist_interaction():
    # Process the playlist interaction data here
    # You can log it, respond to it, or perform other actions
    data = request.json
    print("Playlist Interaction Data:", data)
    return "Playlist interaction recorded."

if __name__ == "__main__":
    print(sp.me())
    app.run(host="0.0.0.0", port=4444)