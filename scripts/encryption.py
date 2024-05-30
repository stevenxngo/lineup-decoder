import os
import string
import random


# load the plaintext data from a file
def load_data(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(
        script_dir, "..", "data", "plaintext", f"{file_name}.txt"
    )
    output_path = os.path.join(
        script_dir, "..", "data", "ciphertext", f"{file_name}.txt"
    )
    with open(input_path, "r", encoding="utf-8") as file:
        artists = file.read().splitlines()
    return artists, output_path


# generate a random substitution mapping
def generate_mapping():
    chars = string.ascii_uppercase + string.digits
    shuffled = list(chars)
    random.shuffle(shuffled)

    mapping = dict(zip(chars, shuffled))
    return mapping


# encrypt an artist with a substitution mapping
def encrypt_artist(artist, mapping):
    encrypted = "".join(mapping.get(char, char) for char in artist)
    return encrypted


# encrypt a list of artists with a substitution mapping
def encrypt_list(artists, mapping):
    return [encrypt_artist(artist, mapping) for artist in artists]


# save the encrypted data to a file
def save_data(artists, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for artist in artists:
            f.write(artist + "\n")


# main encryption function
def encrypt(file_name):
    artists, output_path = load_data(file_name)
    mapping = generate_mapping()
    encrypted_artists = encrypt_list(artists, mapping)
    save_data(encrypted_artists, output_path)
