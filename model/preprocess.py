__last_modified__ = "13 July 2022"

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer


def select_cols(df):
    return df[['artist_name', 'id', 'track_name', 'danceability', 'energy', 'key', 'loudness', 'mode',
               'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', "artist_pop", "genres", "track_pop"]]


def genre_preprocess(df):
    df['genres_list'] = df['genres'].apply(lambda x: x.split(" "))
    return df


def playlist_preprocess(df):
    """
    Preprocess imported playlist
    """
    df = select_cols(df)
    df = genre_preprocess(df)
    return df


def ohe_prep(df: pd.DataFrame, column: str, new_name: str):
    """
    Create One Hot Encoded features of a specific column

    Args: 
        df: Spotify Dataframe
        column: Column to be processed
        new_name: new column name to be used

    Return: 
        tf_df: One-hot encoded features 
    """

    tf_df = pd.get_dummies(df[column])
    feature_names = tf_df.columns
    tf_df.columns = [new_name + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop=True, inplace=True)
    return tf_df


def create_feature_set(df, float_cols) -> pd.DataFrame:
    """
    Process spotify df to create a final set of features that will be used to generate recommendations

    Args: 
        df: Spotify Dataframe
        float_cols: List of float columns that will be scaled

    Return: 
        final: Final set of features 
    """

    # Tfidf genre lists
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(
        df['genres_list'].apply(lambda x: " ".join(x)))
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    if 'genre|unknown' in genre_df.columns:  # drop unknown genre
        genre_df = genre_df.drop(columns='genre|unknown')
    genre_df.reset_index(drop=True, inplace=True)

    # One-hot Encoding
    key_ohe = ohe_prep(df, 'key', 'key') * 0.5
    mode_ohe = ohe_prep(df, 'mode', 'mode') * 0.5

    # Normalization
    # Scale popularity columns
    pop = df[["artist_pop", "track_pop"]].reset_index(drop=True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(
        scaler.fit_transform(pop), columns=pop.columns) * 0.2

    # Scale audio columns
    floats = df[float_cols].reset_index(drop=True)
    scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(scaler.fit_transform(
        floats), columns=floats.columns) * 0.2

    # Concanenate all features
    final = pd.concat([genre_df, floats_scaled, pop_scaled,
                      key_ohe, mode_ohe], axis=1)

    # Add song id
    final['id'] = df['id'].values

    return final


if __name__ == "__main__":
    df = pd.read_csv("./data/sommars.csv")
    df = playlist_preprocess(df)

    float_cols = df.dtypes[df.dtypes == 'float64'].index.values
    complete_feature_set = create_feature_set(df, float_cols=float_cols)
    complete_feature_set.to_csv("./data/sommars_features.csv", index=False)
    complete_feature_set.head()
