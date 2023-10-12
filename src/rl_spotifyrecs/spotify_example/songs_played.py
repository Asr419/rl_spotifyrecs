import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import time
import spotipy.util as util

from pprint import pprint

load_dotenv()

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")


SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI_CALLBACK")


# Initialize Spotipy with user authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-recently-played user-read-currently-playing user-library-read user-read-playback-state'))

# p_auth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI,
#                                                scope='user-read-recently-played user-read-currently-playing user-library-read user-read-playback-state')

# access_token = p_auth.get_access_token()
# ACCESS_TOKEN = access_token['access_token']
# User ID
def recently_played():
    user_id = sp.me()['id']
     # Replace with the actual user ID

    # Playlist ID of the recommended playlist
    playlist_url = 'https://open.spotify.com/playlist/0lrEL0eKBDe9uyfQtCLbUO'

    # Extract the playlist ID from the URL or URI
    playlist_id = playlist_url.split('/')[-1]

    # Get playlist details, including the playlist ID
    playlist = sp.playlist(playlist_id)

    # Extract the playlist ID from the playlist details
    recommended_playlist_id = playlist['id']
    playlist_name = playlist['name']
    num_tracks = playlist['tracks']['total']
    # print(recommended_playlist_id)

    # recommended_playlist_id = 'playlist123'  # Replace with the actual playlist ID

    # Get the user's recently played tracks
    recently_played = sp.current_user_recently_played()
    # print(recently_played)
    # Extract the track IDs from the recommended playlist
    playlist_tracks = [track['track']['id'] for track in sp.playlist_tracks(recommended_playlist_id)['items']]

    # Initialize variables for the song ID and its position
    played_song_id = None
    played_song_position = None
    played_song_time=None
    switch=None

    # Check if a song from the recommended playlist was played
    for idx, track in enumerate(recently_played['items']):
        if track['track']['id'] in playlist_tracks:
            switch=1
            played_song_id = track['track']['id']
            played_song_position = playlist_tracks.index(played_song_id)   # 1-based position
            played_song_time = track['played_at']
            duration_ms = track['track']['duration_ms']
        


    # Print the results
    print("Played Song ID:", played_song_id)
    print("Played Song Position:", played_song_position)
    # print(recently_played)

    # Check if any of the recently played tracks belong to the recommended playlist
    # played_from_recommended_playlist = any(track['track']['album']['id'] == recommended_playlist_id for track in recently_played['items'])

    # Create a timestamp
    timestamp = datetime.now()

    # Check if the 'interaction.csv' file exists
    if os.path.isfile('interaction_data.csv'):
        # Load the existing CSV data into a DataFrame
        existing_df = pd.read_csv('interaction_data.csv')
    else:
        # Create a new CSV file with the specified columns
        existing_df = pd.DataFrame(columns=[
            'Timestamp',
            'User_id',
            'Playlist Name',
            'Number of Tracks in Playlist',
            'Played from Recommended Playlist',
            'Playlist Track IDs',
            'Played Song Id',
            'Played Song At',
            'Played Song Position',
        ])
    print(user_id)
    new_data = {
        'Timestamp': [timestamp],
        'User_id': [user_id],  # New column for user ID
        'Playlist Name': [playlist_name],  # New column for playlist name
        'Number of Tracks in Playlist': [num_tracks],
        'Played from Recommended Playlist': [switch],
        'Playlist Track IDs': [", ".join(playlist_tracks)],
        'Played Song Id': [played_song_id],
        'Played Song At': [played_song_time],
        'Played Song Position': [played_song_position]
    }


    new_df = pd.DataFrame(new_data)

    # Append the new data to the existing DataFrame
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Save the updated DataFrame back to the same CSV file
    updated_df.to_csv('interaction_data.csv', index=False)
    return updated_df


def get_current_track(access_token):
    response = requests.get(
    SPOTIFY_GET_CURRENT_TRACK_URL,
    headers={
        "Authorization": f"Bearer {access_token}"
    }
    )
    print(response)
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
    	"id": track_id,
    	"track_name": track_name,
    	"artists": artist_names,
    	"link": link
    }

    return current_track_info
def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)
        if current_track_info['id'] != current_track_id:
            pprint(
                current_track_info,
                indent=4,
            )
            current_track_id = current_track_info['id']

        time.sleep(1)



# def currently_playing():
#     # Initialize the Spotify API client with user authentication
    
#     user_id = sp.me()['id'] 

#     # Get the currently playing track
#     current_track = sp.current_user_playing_track()

#     played_song_id=None
#     played_song_time=None
#     played_song_action=None

#     if current_track is not None and 'item' in current_track:
#         # Extract relevant information from the currently playing track
#         timestamp = pd.Timestamp.now()
#         user_id = sp.me()['id'] 
#         played_song_id = current_track['item']['id']
#         played_song_time = current_track['progress_ms']
#         played_song_action = current_track['actions']

#         # Create a dictionary to hold the data
        
#     timestamp = datetime.now()
#     print(played_song_id)

#     if os.path.isfile('live_data.csv'):
#         # Load the existing CSV data into a DataFrame
#         existing_df = pd.read_csv('interaction_data.csv')
#     else:
#         # Create a new CSV file with the specified columns
#         existing_df = pd.DataFrame(columns=[
#             'Timestamp',
#             'User_id'
#             'Played Song Id',
#             'Played Song At',
#             'Played Song Action',
#         ])

#     data = {
#             'Timestamp': [timestamp],
#             'User_id': [user_id],
#             'Played Song Id': [played_song_id],
#             'Played Song time': [played_song_time],
#             'Played Song Action': [played_song_action]
#         }


#     new_df = pd.DataFrame(data)

#     # Append the new data to the existing DataFrame
#     updated_df = pd.concat([existing_df, new_df], ignore_index=True)

#     # Save the updated DataFrame back to the same CSV file
#     updated_df.to_csv('live_data.csv', index=False)

#     return existing_df

if __name__=='__main__':
    recently_played()
    main()



