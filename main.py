import argparse
from scripts.data_prep import data_prep
from scripts.decryption import decrypt
from scripts.encryption import encrypt


# parse file name from the command line
def parse_args():
    parser = argparse.ArgumentParser(
        description="Decode a lineup cyphertext file to plaintext."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="Name of the encrypted artist txt file. Note: must be in \
            /data/ciphertext folder and without the .txt extension.",
    )
    parser.add_argument(
        "-e",
        "--encrypt",
        action="store_true",
        help="Encrypt the specified lineup file instead of decrypting it.",
    )
    args = parser.parse_args()
    file_name = args.file_name
    to_encrypt = args.encrypt
    return file_name, to_encrypt


def main():
    file_name, to_encrypt = parse_args()
    if to_encrypt:
        encrypt(file_name)
    else:
        data_prep(file_name)
        decrypt(file_name)


if __name__ == "__main__":
    main()
