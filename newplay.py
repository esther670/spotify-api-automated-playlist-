import spotipy
from spotipy.oauth2 import SpotifyOAuth
import schedule
import time

Client_ID = '851fd71f86fd4f5b9408941654a1238f'
Client_Secret = '0897b21fb9da4823be19b9617b350681'
Redirect_URI = 'http://localhost:3000/callback'
scope = 'playlist-modify-public'

User_ID = 'ng51hzuyuie769u3h9g6eo824'

spotify_auth= spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = Client_ID,
                                                        client_secret = Client_Secret,
                                                        redirect_uri = Redirect_URI,
                                                        scope = scope))

#create a new playlist
playlist = spotify_auth.user_playlist_create(user=User_ID, name='Top hits in kenya', public=True, description='Listen and move to the top hits trending in Kenya')
print('Playlist created:', playlist['name'])

playlist_ID = playlist['id']

def updateplaylist():
    top_playlists = spotify_auth.category_playlists(category_id='toplists', country='KE', limit=10)
    
    # Extract track URIs from the first playlist
    first_playlist_tracks = spotify_auth.playlist_tracks(playlist_id=top_playlists['playlists']['items'][0]['id'])
    track_uris = [track['track']['uri'] for track in first_playlist_tracks['items']]
        
    # Updating the playlist with the extracted tracks
    spotify_auth.playlist_replace_items(playlist_id=playlist_ID, items=track_uris)
    print(f"{len(track_uris)} tracks have been added to your playlist")

updateplaylist()

schedule.every(1).day.do(updateplaylist)
while True:
    schedule.run_pending()
    time.sleep(1)
    


