"""
This script is used to transform raw json data from the dataset to csv files 
by using pandas json_normalize() function
"""

__author__ = "Nauqh"
__last_modified__ = "26 June 2022"

import json
import pandas as pd


# Import json
data_path = "./data/million.json"
raw_json = json.loads(open(data_path).read())

# Transform Data
playlists = raw_json["playlists"]
df = pd.json_normalize(playlists, record_path='tracks', meta=['name'])

# Output
df.to_csv("./data/raw_data.csv")

if __name__ == "__main__":
    print(len(playlists))   # 1000 playlist
