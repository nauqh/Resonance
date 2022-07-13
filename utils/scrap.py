""" Utility module for Spotify API """

__author__ = "Nauqh"
__last_modified__ = "13 July 2022"

import re
import os
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


dotenv.load_dotenv()

cid = os.environ["CID"]
secret = os.environ["SECRET"]


def features_extract(ari: str):
    """
    Extract song features using track URI
    """
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Audio features
    features = sp.audio_features(ari)[0]

    # Artist of the track, for genres and popularity
    artist = sp.track(ari)["artists"][0]["id"]
    artist_pop = sp.artist(artist)["popularity"]
    artist_genres = sp.artist(artist)["genres"]

    # Track popularity
    track_pop = sp.track(ari)["popularity"]

    # Add extra features (artist_pop, genres, track_pop)
    features["artist_pop"] = artist_pop
    if artist_genres:
        features["genres"] = " ".join(
            [re.sub(' ', '_', i) for i in artist_genres])
    else:
        features["genres"] = "unknown"
    features["track_pop"] = track_pop

    return features


def search(track_name: str, artist: str, limit: int):
    """
    Search for song URI using song name and artist name
    """
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    searchResults = sp.search(q="artist:" + artist +
                              " track:" + track_name, type="track", limit=limit)
    return searchResults["tracks"]["items"][0]["uri"]


if __name__ == "__main__":
    result = features_extract("1o0nAjgZwMDK9TI4TTUSNn")
    print(result)
    # print(search("Wrecked", "Imagine Dragons", 1))
