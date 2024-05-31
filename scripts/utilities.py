import os


# removes duplicates and sorts reference artists
def process_ref_artists():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "..", "data", "artists.txt")

    with open(path, "r", encoding="utf-8") as f:
        artists = f.readlines()
    artists = sorted(set(artist.strip() for artist in artists))

    with open(path, "w", encoding="utf-8") as file:
        for artist in artists:
            file.write(artist + "\n")


if __name__ == "__main__":
    process_ref_artists()
