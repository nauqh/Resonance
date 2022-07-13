__last_modified__ = "13 July 2022"

import os
import dotenv
import spotipy
import re
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
from utils.scrap import features_extract

dotenv.load_dotenv()

cid = os.environ["CID"]
secret = os.environ["SECRET"]

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def playlist_extract(url: str) -> pd.DataFrame:
    """
    Extract playlist data

    Return a Dataframe of playlist's tracks    
    """

    playlist_URI = url.split("/")[-1].split("?")[0]

    artist, trackid, trackname = [], [], []

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # Main Artist
        artist_name = track["track"]["artists"][0]["name"]
        artist.append(artist_name)

        # URI
        track_uri = track["track"]["uri"]
        trackid.append(track_uri)

        # Track name
        track_name = track["track"]["name"]
        trackname.append(track_name)

    data = {'artist_name': artist, 'id': trackid, 'track_name': trackname}
    df = pd.DataFrame(data)
    df["id"] = df["id"].apply(
        lambda x: re.findall(r'\w+$', x)[0])

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add audio features for each songs into the playlist Dataframe

    Using features_extract() to retrieve data from Spotify API
    """
    features = []

    print(f"\n📦 Extracting {len(df)} songs from playlist..")

    for i in tqdm([uri for uri in df['id']]):
        try:
            features.append(features_extract(i))
        except:
            continue
    featureDF = pd.DataFrame(features)
    newDF = pd.merge(df, featureDF)

    return newDF


if __name__ == "__main__":
    x = playlist_extract(
        "https://open.spotify.com/playlist/4mih0AxheCVcIQaIMf1YAK?si=a4d76224b4cc479b")
    y = add_features(x)
    y.to_csv('./data/sommars.csv')
