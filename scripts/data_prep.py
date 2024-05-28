import pandas as pd
import os


# load the data from the txt file
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.readlines()
    return data


# split the data into a list of artists, separated by "|"
def split_data(data):
    lines = [line.strip().split("|") for line in data]
    lines = [[artist.strip() for artist in line] for line in lines]
    artists = [
        {"cyphertext": artist.upper()} for line in lines for artist in line
    ]
    return artists


# save the data to a csv file
def save_data(artists, path):
    df = pd.DataFrame(artists)
    df.to_csv(path, index=False)


# data prep function
def data_prep(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(
        script_dir, "..", "data", "raw", f"{file_name}.txt"
    )
    output_path = os.path.join(
        script_dir, "..", "data", "processed", f"{file_name}.csv"
    )

    data = load_data(input_path)
    artists = split_data(data)
    save_data(artists, output_path)
