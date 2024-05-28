import pandas as pd
import argparse
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


# parse the arguments: input file and output file
def parse_args():
    parser = argparse.ArgumentParser(
        description="Format the lineup txt file to a CSV file."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="Name of the encrypted artist txt file. Note: must be in /data/raw folder and without the .txt extension.",
    )
    args = parser.parse_args()
    file_name = args.file_name
    return file_name


# main function
def data_prep():
    file_name = parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    input_path = os.path.join(
        script_dir, "..", "data", "raw", f"{file_name}.txt"
    )
    output_path = os.path.join(
        script_dir, "..", "data", "processed", f"{file_name}.csv"
    )

    data = load_data(input_path)
    artists = split_data(data)
    save_data(artists, output_path)


if __name__ == "__main__":
    data_prep()
