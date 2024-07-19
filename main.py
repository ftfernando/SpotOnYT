from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from tqdm import tqdm
import pandas as pd
import csv
import os
from dotenv import load_dotenv

# Install the libraries with the command "pip install spotipy ytmusicapi python-dotenv" in the terminal

# Authentication with YTMusic:
# To create "oauth.json", use the command "ytmusicapi oauth" in the terminal and follow the instructions.
ytmusic = YTMusic("oauth.json")

# Load .env file if it exists
load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# Request new values from the user if environment variables are not set
if not client_id or not client_secret or not redirect_uri:
    client_id = input("Enter the Spotify Client ID: ")
    client_secret = input("Enter the Spotify Client Secret: ")
    redirect_uri = input("Enter the Spotify Redirect URI: ")

    # Create or update the .env file with new values
    with open('.env', 'w') as f:
        f.write(f"SPOTIPY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIPY_CLIENT_SECRET={client_secret}\n")
        f.write(f"SPOTIPY_REDIRECT_URI={redirect_uri}\n")
        print("Successfully created .env file.")

else:
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")
    print(f"Redirect URI: {redirect_uri}")


# Authenticate credentials
sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri,
                                       scope='playlist-read-private'))

# Request the Spotify playlist ID
playlist_id = input("Enter the Spotify playlist link/ID: ")

# Retrieve playlist information
playlist = sp.playlist(playlist_id)
playlist_name = playlist['name']


# Function to retrieve all tracks from the playlist
def get_all_playlist_tracks(spotify, internal_playlist_id, limit=100):
    tracks = []
    offset = 0
    while True:
        response = spotify.playlist_tracks(internal_playlist_id, limit=limit, offset=offset)
        tracks.extend(response['items'])
        if len(response['items']) < limit:
            break
        offset += limit
    return tracks


# Retrieve all tracks from the playlist
playlist_tracks = get_all_playlist_tracks(sp, playlist_id)

# Store the Spotify playlist data
spotify_tracks = []
for item in playlist_tracks:
    track = item['track']
    track_data = {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name']
    }
    spotify_tracks.append(track_data)

# Request the name for the new playlist
yt_playlist_name = input("Enter the name of the new playlist on YouTube Music: ")

# Create a playlist on YTMusic
yt_playlist_id = ytmusic.create_playlist(yt_playlist_name, f'Created by App | Spot on YT - by Fernando Thompson | Spotify Playlist: {playlist_name}', 'PUBLIC')

# Add tracks to the playlist on YTMusic
for track in tqdm(spotify_tracks, desc="Adding tracks to the playlist on YouTube Music", unit="track"):
    search_results = ytmusic.search(f"{track['name']} {track['artist']}", filter='songs')
    if not search_results:
        print(f"No search results for {track['name']} - {track['artist']}")
        continue

    track_id = search_results[0]['videoId']
    try:
        ytmusic.add_playlist_items(yt_playlist_id, [track_id])
    except Exception as e:
        print(f"Error adding {track['name']} - {track['artist']}: {e}")

# Get information from the new playlist on YouTube Music
yt_playlist_tracks = ytmusic.get_playlist(yt_playlist_id)['tracks']

# Store the YouTube Music playlist data
yt_tracks = []
for item in yt_playlist_tracks:
    track_data = {
        'name': item['title'],
        'artist': item['artists'][0]['name'],
        'album': item['album']['name'] if 'album' in item else 'Unknown Album'
    }
    yt_tracks.append(track_data)


# Function: save tracks not added to a CSV file
def save_tracks_to_csv(tracks, filename):
    fieldnames = ['name', 'artist', 'album']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tracks)


save_tracks_to_csv(spotify_tracks, 'spotify_tracks.csv')
save_tracks_to_csv(yt_tracks, 'yt_tracks.csv')


# Load CSV files into dataframes
spotify_df = pd.read_csv('spotify_tracks.csv')
yt_df = pd.read_csv('yt_tracks.csv')

# Extract only the 'name' column (or the corresponding column name)
spotify_names = spotify_df['name']
yt_names = yt_df['name']

# Find tracks that are in Spotify but not in YouTube Music
not_in_yt = spotify_df[~spotify_df['name'].isin(yt_names)].drop_duplicates()


# Save the result to a new CSV file
not_in_yt.to_csv('not_added_tracks.csv', index=False)


print(f"Playlist '{playlist_name}' successfully copied to YouTube Music!")
print(f"Tracks not added have been saved to 'not_added_tracks.csv'.")
print(f"YouTube Music playlist link: https://music.youtube.com/playlist?list={yt_playlist_id}")


# In the future, I will add update functions
# *** YTMusic.add_playlist_items (playlistId: str, videoIds: List[str] | None = None, source_playlist: str | None = None, duplicates: bool = False)
# *** - duplicates – false
#
#
# In the future, I plan to add more interactions:
# Error Handling
# Check for Existing Playlists
# Songs/Playlists info
# Podcasts - Check availability on YouTube
# Front-end of the application
