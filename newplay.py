import spotipy
from spotipy.oauth2 import SpotifyOAuth
import schedule
import time


Client_ID = '851fd71f86fd4f5b9408941654a1238f'
Client_Secret = '0897b21fb9da4823be19b9617b350681'
Redirect_URI = 'http://localhost:8888/callback'
scope = 'playlist-modify-public'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = Client_ID,
                                                        client_secret = Client_Secret,
                                                        redirect_uri = Redirect_URI,
                                                        scope = scope))


User_ID = sp.current_user()['id']

#create a new playlist
playlist = sp.user_playlist_create(user=User_ID, name='Popular tracks in kenya', public=True, description='Listen and move to the timeless hits and top hits trending in Kenya')
print('Playlist created:', playlist['name'])

playlist_ID = playlist['id']

def updateplaylist():
    top_tracks = sp.search( q='Kenya', type='track', limit=100, offset=1, market='KE')
    popularity_threshold = 30 
    popular_tracks = [track for track in top_tracks['tracks']['items']
                      if track['popularity'] >= popularity_threshold]
    track_uris = [track['uri'] for track in popular_tracks]

    # Updating the playlist with the extracted tracks
    sp.user_playlist_add_tracks(user=User_ID, playlist_id=playlist_ID, tracks=track_uris)
    print(f"{len(track_uris)} tracks have been added to your playlist")

updateplaylist()

schedule.every(2).days.do(updateplaylist)
while True:
    schedule.run_pending()
    time.sleep(1)
    


