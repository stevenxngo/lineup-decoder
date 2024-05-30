import re
import pandas as pd

# define heuristic patterns
DJ_SET_PATTERN = re.compile(r"\([A-Z0-9]{2} [A-Z0-9]{3}\)")  # DJ SET
SUNSET_PATTERN = re.compile(
    r"\(([A-Z0-9])([A-Z0-9])([A-Z0-9])(\1)([A-Z0-9])([A-Z0-9])\s(\1)(\5)(\6)\)"
)  # SUNSET SET
THROWBACK_PATTERN = re.compile(
    r"\(([A-Z0-9])([A-Z0-9]{8}\s[A-Z0-9]{2})(\1)\)"
)  # THROWBACK SET
B2B_PATTERN = re.compile(r"(\w+\s)([A-Z0-9])([A-Z0-9])(\2)(\s\w+)")  # B2B


# DJ SET
def extract_dj_set(df, text):
    mappings = {}
    dj_set_matches = DJ_SET_PATTERN.findall(text)
    for match in dj_set_matches:
        cypher_dj_set = match[1:-1]
        plain_dj_set = "DJ SET"
        for c, p in zip(
            cypher_dj_set.replace(" ", ""), plain_dj_set.replace(" ", "")
        ):
            mappings[c] = p

        artist = text[:-8].strip()
        new_row = pd.DataFrame([{"cyphertext": artist}])
        df = pd.concat([df, new_row], ignore_index=True)
    return df, mappings


# SUNSET SET
def extract_sunset_set(df, text):
    mappings = {}
    sunset_matches = SUNSET_PATTERN.findall(text)
    for match in sunset_matches:
        cypher_sunset = match[:-3]
        plain_dj_set = "SUNSET"
        for c, p in zip(cypher_sunset, plain_dj_set):
            mappings[c] = p

        artist = text[:-13].strip()
        new_row = pd.DataFrame([{"cyphertext": artist}])
        df = pd.concat([df, new_row], ignore_index=True)
    return df, mappings


# THROWBACK SET
def extract_throwback_set(df, text):
    mappings = {}
    throwback_matches = THROWBACK_PATTERN.findall(text)
    for match in throwback_matches:
        match = "".join(match).replace(" ", "")
        cypher_throwback = match[:-1]
        for c, p in zip(cypher_throwback.replace(" ", ""), "THROWBACKSE"):
            mappings[c] = p
        artist = text[:-16].strip()
        new_row = pd.DataFrame([{"cyphertext": artist}])
        df = pd.concat([df, new_row], ignore_index=True)
    return df, mappings


# B2B
def extract_b2b(df, text):
    mappings = {}
    b2b_matches = B2B_PATTERN.findall(text)
    for match in b2b_matches:
        cypher_b2b = match[1] + match[2]
        plain_b2b = "B2"
        for c, p in zip(cypher_b2b, plain_b2b):
            mappings[c] = p

        # create new rows for b2b artists
        artists = [match[i].strip() for i in range(0, len(match), 4)]
        new_df = pd.DataFrame(artists, columns=["cyphertext"])
        df = pd.concat([df, new_df], ignore_index=True)
    return df, mappings
