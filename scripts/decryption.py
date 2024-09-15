import os
import re
import pandas as pd
from .heuristics import (
    extract_dj_set,
    extract_sunset_set,
    extract_throwback_set,
    extract_b2b,
)


# load data from input file
def load_data(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(
        script_dir, "..", "data", "processed", f"{file_name}.csv"
    )
    output_path = os.path.join(
        script_dir, "..", "data", "decoded_plaintext", f"{file_name}.txt"
    )
    df = pd.read_csv(input_path)
    artists_path = os.path.join(script_dir, "..", "data", "artists.txt")
    with open(artists_path, "r", encoding="utf-8") as file:
        artists = file.read().splitlines()
    return df, output_path, artists


# extract heuristic patterns from artist names
def extract_patterns(df, text):
    mappings = {}
    extract_funcs = [
        extract_dj_set,
        extract_sunset_set,
        extract_throwback_set,
        extract_b2b,
    ]

    for func in extract_funcs:
        df, func_mappings = func(df, text)
        mappings.update(func_mappings)

    return df, mappings


# initialize mappings with heuristics
def init_mappings(df):
    mappings = {}
    for artist in df["cyphertext"]:
        df, new_mappings = extract_patterns(df, artist)
        mappings.update(new_mappings)
    return df, mappings


# create plaintext column
def create_plaintext(df):
    df["plaintext"] = df["cyphertext"].apply(
        lambda row: re.sub(r"[A-Z0-9]", "-", row)
    )


# update plaintext of row with new mappings
def replace_decoded(row, mappings):
    updated_decoded = []
    for ct, dc in zip(row["cyphertext"], row["plaintext"]):
        if ct in mappings:
            updated_decoded.append(mappings[ct])
        else:
            updated_decoded.append(dc)
    return "".join(updated_decoded)


# update plaintext with new mappings
def update_plaintext(df, mappings):
    df["plaintext"] = df.apply(
        lambda row: replace_decoded(row, mappings), axis=1
    )


# match plaintext pattern with artist
def match_pattern(pattern, artist, mappings):
    # check if pattern and name have the same length
    if len(pattern) != len(artist):
        return False

    # check if pattern and name match
    for p_char, n_char in zip(pattern, artist):
        if p_char == "-":
            if n_char in mappings.values() or n_char == " ":
                return False
        elif p_char == " " and n_char != " ":
            return False
        else:
            if p_char != n_char:
                return False
    return True


# match pattern with all artists
def match_artist(pattern, mappings, artists):
    matches = [
        artist for artist in artists if match_pattern(pattern, artist, mappings)
    ]
    return ", ".join(matches) if matches else None


# match all plaintext patterns with artists
def match_artists(df, mappings, artists):
    df["matches"] = df["plaintext"].apply(
        match_artist, args=(mappings, artists)
    )


# update row with artist and mappings
def update_row(df, row_num, mappings, artist, artists):
    # set artist for row
    df.at[row_num, "plaintext"] = artist
    cyphertext = df.at[row_num, "cyphertext"]

    # update mappings
    for ct_char, pt_char in zip(cyphertext, artist):
        if (
            ct_char.isalnum()
            and ct_char not in mappings
            and pt_char not in mappings.values()
        ):
            mappings[ct_char] = pt_char
    df["plaintext"] = df.apply(
        lambda row: replace_decoded(row, mappings), axis=1
    )

    # update matches
    match_artists(df, mappings, artists)


# sort mappings in alphabetical order
def sort_mappings(mappings):
    return dict(sorted(mappings.items(), key=lambda item: item[1]))


# save data to output file
def save_data(path, df, mappings):
    with open(path, "w", encoding="utf-8") as f:
        # write lineup
        for _, row in df.iterrows():
            f.write(f"{row['cyphertext']} -> {row['plaintext']}\n")

        f.write("\n")

        # write mappings
        for key, value in mappings.items():
            f.write(f"{key} -> {value}\n")


# recursively decrypt artists
def recursive_decrypt(df, mappings, artists):
    def match_and_update(df, mappings, artists):
        for row_num, row in df.iterrows():
            if not row["matches"]:
                continue

            plaintext = row["plaintext"]
            matches = row["matches"].split(", ")
            blanks = plaintext.count("-")

            if len(matches) == 1 and blanks / len(plaintext) < 0.5:
                artist = matches[0]

                if artist not in df["plaintext"].tolist():
                    update_row(df, row_num, mappings, artist, artists)
                    return True
        return False

    match_artists(df, mappings, artists)
    while match_and_update(df, mappings, artists):
        pass
    return df.drop(columns=["matches"])


# main decryption function
def decrypt(file_name):
    df, output_path, artists = load_data(file_name)
    num_artists = len(df)
    df, mappings = init_mappings(df)
    create_plaintext(df)
    update_plaintext(df, mappings)
    df = recursive_decrypt(df, mappings, artists).head(num_artists)
    mappings = sort_mappings(mappings)
    save_data(output_path, df, mappings)
