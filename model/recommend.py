__last_modified__ = "13 July 2022"

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# songs = pd.read_csv("./data/allsong_data.csv")
# features = pd.read_csv("./data/complete_feature.csv")
# playlistDF_test = pd.read_csv("./data/sommars_features.csv")


def generate_playlist_feature(features: pd.DataFrame, playlist: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize a user's playlist into a single vector
    """

    # Find all non-playlist song features
    # if "genre|gen_z_singer" in playlist_df:
    #     playlist_df = playlist_df.drop(columns="genre|gen_z_singer")

    playlist_vector = playlist
    cols = list(playlist_vector.columns)

    feature_repo = features[~features['id'].isin(
        playlist['id'].values)]

    for col in cols:
        if col not in feature_repo.columns:
            feature_repo[col] = 0

    feature_repo = feature_repo[cols]

    playlist_vector = playlist_vector.drop(
        columns="id")

    return playlist_vector.sum(axis=0), feature_repo


def generate_playlist_recos(songs: pd.DataFrame, playlist_vector: list, feature_repo: pd.DataFrame) -> pd.DataFrame:
    '''
    Generated recommendation based on songs in a specific playlist.

    Args: 
        df (pandas dataframe): spotify dataframe
        playlist_vector (pandas series): summarized playlist feature (single vector)
        repository (pandas dataframe): feature set of songs that are not in the selected playlist

    Return: 
        non_playlist_df_top_10: Top 10 recommendations for that playlist
    '''
    repository = songs[songs['id'].isin(feature_repo['id'].values)]

    # Find cosine similarity between the playlist and the complete song set
    repository['sim'] = cosine_similarity(feature_repo.drop(
        'id', axis=1).values, playlist_vector.values.reshape(1, -1))[:, 0]

    non_playlist_df_top_10 = repository.sort_values(
        'sim', ascending=False).head(10)
    return non_playlist_df_top_10


if __name__ == "__main__":

    # complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(
    #     features, playlistDF_test)
    # print(complete_feature_set_playlist_vector)
    # print(complete_feature_set_nonplaylist)

    # top = generate_playlist_recos(
    #     songs, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)
    # print(top[['artist_name', 'track_name']])
    pass
