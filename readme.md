# 📻Resonance - A tiny recommendation system

![Python](https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge&logo=Python)
![Pandas](https://img.shields.io/badge/plotly%20-%2300416A.svg?&style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/pandas%20-%23150458.svg?&style=for-the-badge&logo=plotly&logoColor=white)

**Update** (13 July 2022): Try implementing Collaborative Filtering

## About the project

**Resonance** is a Content-based Recommendation System which suggests songs given user playlists. It has approximately *60,000* songs in its database extracted and transformed using the **Spotify 1 Million Dataset**

### Spotify Million Playlist Dataset

A dataset of 1 million playlists consisting of over 2 million unique tracks by nearly 300,000 artists. For simplicity, I will just extract the first 1000 playlists which contain approximately 60,000 tracks.

## Requirements

There are some general library requirements for the project and some which are specific to individual methods. The general requirements are as follows.

- `Spotify Developers`
- `regex`
- `plotly`
- `sklearn`

**Note**: It is recommended to use ***Streamlit*** for deploying the application

## Usage

We will run the whole `model` package 

```shell
python -m model  
```

## Development

### Datasets
- `songs.csv`: songs extracted using playlists from **Spotify 1 Million Dataset**
- `features.csv`: normalized features only for recomendation system

### Scripts
- `normalize.py`: Transform json into csv using `json_normalise()`
- `scrap.py`: Extract song features from **Spotify API** 

### Modules
- `extract.py`: Extract playlist data and song features
- `preprocess.py`: Transform audio features, generate addition features and normalize the data
- `recommend.py`: Perform recommendation

## Data scraping

### Authentication

We need an URI to perform any function with the API referring to an object in Spotify. The URI of any Spotify object is contained in its shareable link

```python
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
```
**Note**: When working directly with Spotify API, the song URI has the format `spotify:track:[id]`

### Scrapping

*The process including*:

- Extract URI from share link
- Use Spotify API to request song features from playlist using playlist URI
- Read json files and select song features

## Data preprocess

### Genre preprocess

### TF-IDF encoding

### Normalization
<!--eof>