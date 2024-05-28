import pandas as pd
import argparse


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
        "input_file", type=str, help="Path to the input TXT file"
    )
    parser.add_argument(
        "output_file", type=str, help="Path to the input TXT file"
    )
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    return input_file, output_file


# main function
def data_prep():
    input_file, output_file = parse_args()
    data = load_data(input_file)
    artists = split_data(data)
    save_data(artists, output_file)


if __name__ == "__main__":
    data_prep()
