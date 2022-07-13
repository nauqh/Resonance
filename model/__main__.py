__last_modified__ = "13 July 2022"

import pandas as pd

from model.extract import playlist_extract, add_features
from model.preprocess import playlist_preprocess, create_feature_set
from model.recommend import generate_playlist_feature, generate_playlist_recos


songs = pd.read_csv("./data/allsong_data.csv")
features = pd.read_csv("./data/complete_feature.csv")


def pipeline(url: str) -> pd.DataFrame:
    # Extract
    playlist = add_features(playlist_extract(url))

    # Preprocess
    df = playlist_preprocess(playlist)
    float_cols = df.dtypes[df.dtypes == 'float64'].index.values
    complete_feature_set = create_feature_set(df, float_cols)

    # Recommend
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(
        features, complete_feature_set)
    top = generate_playlist_recos(
        songs, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)
    print("\n🎵 Here is your recommendation playlist!")
    # return top[['artist_name', 'track_name', 'sim']]
    return top


if __name__ == "__main__":
    url = input("Enter playlist url: ")
    print(pipeline(url))
