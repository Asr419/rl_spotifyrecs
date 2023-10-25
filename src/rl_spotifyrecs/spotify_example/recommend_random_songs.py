import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve the environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# # Spotify API credentials and user authentication
# SPOTIPY_CLIENT_ID = 'your_client_id'
# SPOTIPY_CLIENT_SECRET = 'your_client_secret'
# SPOTIPY_REDIRECT_URI = 'your_redirect_uri'

# Initialize Spotipy with user authentication
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     scope='user-library-read',  # Required scope for accessing user's saved tracks
# ))

# # Function to recommend a random list of 10 songs to the user
# def recommend_random_songs():
#     # Get the user's saved tracks (you can customize this based on your needs)
#     saved_tracks = sp.current_user_saved_tracks()
    
#     # Extract the track IDs from the saved tracks
#     track_ids = [item['track']['id'] for item in saved_tracks['items']]
    
#     # Shuffle the track IDs randomly
#     random.shuffle(track_ids)
    
#     # Take the first 10 shuffled track IDs (or fewer if the user has fewer saved tracks)
#     recommended_track_ids = track_ids[:10]
    
#     # Get the track details for the recommended track IDs
#     recommended_tracks = sp.tracks(recommended_track_ids)
    
#     # Print the recommended track names
#     for track in recommended_tracks['tracks']:
#         print(track['name'])

# # Call the function to recommend random songs to the user
# recommend_random_songs()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-library-read user-read-recently-played playlist-modify-public playlist-modify-private',  # Required scope for modifying user's library
))
print(sp.me()['id'])
user_id = sp.me()['id'] 
# Function to recommend and add random songs to the user's Spotify library 'user-library-read user-read-recently-played playlist-modify-public playlist-modify-private'
# def recommend_and_add_songs():
#     # Get the user's saved tracks (you can customize this based on your needs)
#     saved_tracks = sp.current_user_saved_tracks()
    
#     # Extract the track IDs from the saved tracks
#     track_ids = [item['track']['id'] for item in saved_tracks['items']]
    
#     # Shuffle the track IDs randomly
#     random.shuffle(track_ids)
    
#     # Take the first 10 shuffled track IDs (or fewer if the user has fewer saved tracks)
#     recommended_track_ids = track_ids[:10]
    
#     # Add the recommended tracks to the user's library
#     for track_id in recommended_track_ids:
#         sp.current_user_saved_tracks_add(tracks=[track_id])

#     print("Recommended songs added to your Spotify library!")

# # Call the function to recommend and add random songs to the user's library
# recommend_and_add_songs()

# def recommend_and_suggest():
#     # Get the user's recently played tracks
#     recently_played = sp.current_user_recently_played(limit=50)  # Limit to 50 recently played tracks

#     # Check the structure of the response and extract the relevant track information
#     recommended_tracks = []
#     for item in recently_played['items']:
#         track_info = item['track']
#         recommended_tracks.append(f"{track_info['name']} by {', '.join([artist['name'] for artist in track_info['artists']])}")

#     # Shuffle the recommended tracks
#     random.shuffle(recommended_tracks)

#     # Select the first 10 randomly shuffled tracks (or fewer if there are fewer than 10)
#     recommended_selection = recommended_tracks[:10]

#     # Display and suggest the recommended songs to the user
#     print("Recommended Songs:")
#     for idx, track in enumerate(recommended_selection, start=1):
#         print(f"{idx}. {track}")

#     print("\nTo add these songs to your library, please visit the Spotify app and follow the steps.")

# # Call the function to recommend and suggest songs to the user
# recommend_and_suggest()
def create_and_add_to_playlist():
    # Create a new playlist
    playlist_name = 'Test4'  # Replace with your desired playlist name
    playlist_description = 'Recommended songs generated by script'  # Replace with your desired playlist description
    user_id = sp.me()['id']
    
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=playlist_description)
    
    # Get the user's recently played tracks
    recently_played = sp.current_user_recently_played(limit=10)  # Limit to 10 recently played tracks

    # Extract the track URIs
    track_uris = [track['track']['uri'] for track in recently_played['items']]
    
    # Add the recently played tracks to the new playlist
    sp.playlist_add_items(playlist['id'], track_uris)

    print(f"Recommended songs added to the playlist: {playlist_name}")

# Call the function to create a playlist and add random songs
create_and_add_to_playlist()




