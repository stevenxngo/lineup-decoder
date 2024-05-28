import argparse
from scripts.data_prep import data_prep

# parse file name from the command line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Decode a lineup cyphertext file to plaintext."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="Name of the encrypted artist txt file. \
            Note: must be in /data/raw folder and without the .txt extension.",
    )
    args = parser.parse_args()
    file_name = args.file_name
    return file_name


def main():
    file_name = parse_args()
    data_prep(file_name)


if __name__ == "__main__":
    main()
