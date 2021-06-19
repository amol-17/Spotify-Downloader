## Enter spotify **playlist/album/track URL**

# Enter Playlist/Album/track URL inside double quotes " "
URL = ""
# Example: URL = "https://open.spotify.com/playlist/21ff4YweZbISUbJWtfcfKQ?si=ef3121403c4a454d"
# Example2: URL = "https://open.spotify.com/album/2gNPnKP1PDkB5SZz3IMKuX?si=Nfnt4HP4Q6O_-1yeZVOjiA&dl_branch=1&nd=1"
# Example3: URL = "https://open.spotify.com/track/4yR2z3JafnCo86THA6ISZ4?si=784f1a4afd4844da"

### Click on Runtime and select **Run All**"""

# !pip install --upgrade google-api-python-client
# !pip install git+https://github.com/ssuwani/pytube 
# !pip install pytube
# !pip install spotipy

# mkdir songs

# importing libraries
import requests
import json
from pytube import YouTube
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# web scraping part instead of API
def youtube_Search(query):
  query = query.replace(" ", "+")
  url = "https://youtube-scrape.herokuapp.com/api/search?q="+query+"&page=1"
  

  page = requests.get(url)
  txt = page.text
  js = json.loads(txt)
  for i in range(len(js['results'])):
      vid_URL_ = (js['results'][i]['video']['url'])
      break
  download(vid_URL_)

# pytube

def download(video_id):
  URL = video_id
  print(URL)
  yt = YouTube(URL)
  # aud = yt.streams.filter(only_audio=True).all()
  aud = yt.streams.filter(only_audio = True).first()
   
  output = aud.download()
  base, ext = os.path.splitext(output)
  new = base + ".mp3"
  os.rename(output, new)

def try_yt_search(vid_name): #trying to search our song and handling exception for 3 times
  try:
    youtube_Search(vid_name)
    print("Download finished.")
    time.sleep(1)
  except Exception as e:
    print("error: ", vid_name, e)
    i = 0
    while i<3:
      try:
        youtube_Search(vid_name)
        print("Download finished.")
        break
      except:
        print("exception no: ", i)
        time.sleep(1)
        i+=1
        pass

# Getting info from Spotify API
client_id = "89bfb2d10c5549e7962657ef9d52e7fd"
client_secret = "878fee4f9baa424eafe05b298f5a69a1"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
       client_secret=client_secret))

# playlist download
def sp_playlist_search():
  results = sp.playlist_items(URL)
  playlist=results['items']

  while results['next']:
    results=sp.next(results)

  playlist.extend(results['items'])

  for song in playlist:
    artist_name = song['track']['artists'][0]['name']
    song_name = song['track']['name']
    print("\nDownloading ...")
    print(artist_name + " " + song_name)
    vid_name = artist_name + " " + song_name
    try_yt_search(vid_name)

# album downlaod
def sp_album_search():
  results = sp.album_tracks(URL)
  albums = results['items']
  while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

  for song in albums:
    artist_name = song['artists'][0]['name']
    song_name = song['name']
    print("\nDownloading ...")
    print(artist_name + " " + song_name)
    vid_name = artist_name + "+" + song_name
    try_yt_search(vid_name)

def sp_track_search():
  result = sp.track(URL)
  song_name = result['name']
  artist_name = result['artists'][0]['name']
  print("\nDownloading ...")
  print(artist_name + " " + song_name)
  vid_name = artist_name + " " + song_name
  try_yt_search(vid_name)

if "album" in URL:
  sp_album_search()

if "playlist" in URL:
  sp_playlist_search()

if "track" in URL:
  sp_track_search()

"""#To download the folder"""

# Skip this part if you are running on a local machine instead.
# !zip -r /content/songs.zip /content/songs
#
# from google.colab import files
# files.download("/content/songs.zip")

