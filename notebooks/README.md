# Notebooks

**Note**: Code in this directory may not be up-to-date with the final version of the decryption algorithm and may contain errors or inefficiencies. If you are looking for the final decryption logic, please refer to the [`../scripts`](../scripts/) directory.

This directory contains Jupyter notebooks I created during the development of the decryption algorithm. As a result, the functionality of these notebooks is not intended to be used a standalone tool, but rather as a documentation of my thought process and the steps I took. The final decryption logic can be found in the [`../scripts`](../scripts/) directory. The notebooks are organized in the following way:

- `01_data-prep.ipynb`: This notebook contains the data preprocessing steps I took to prepare the data for decryption, including separating artists by lines and converting the data to an organized csv file.

- `02_decryption.ipynb`: This notebook contains the decryption process I used to decrypt the lineup data. The decryption process is based on the assumption that the lineup  is encrypted with a simple substitution cipher. Further information on the algorithm can be found [here](../README.md#algorithm)

- `03_encryption.ipynb`: This notebook contains the process of encrypting plaintext lineup data into ciphertext. This procedure was mainly used to generate test ciphertext data for the decryption process. It is not necessary for the decryption process or the primary goal of the project.

The data used in [`02_decryption.ipynb`](02_decryption.ipynb) is the encoded lineup from Countdown NYE 2024, assumed to be encrypted with a simple substitution cipher. Based on assets available on the website with mappings for `NEW YEARS INVASION` and `SOUTHERN CALIFORNIA 18+` I was able to create an rudimentary dictionary, which expedited the decryption process.

![New Years Invasion](../data/countdown_24/new_years_invasion.png)
![Southern California 18+](../data/countdown_24/southern_california.png)
![Assets](../data/countdown_24/assets.JPG)
![Teaser](../data/countdown_24/teaser.JPG)