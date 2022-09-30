import json
import requests

PREFIX = "https://ntrs.nasa.gov/"
def read_json(metadata_file):
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    return metadata

def download_n_full_textfiles(metadata_file, n=-1):
    metadata = read_json(metadata_file)
    n = len(metadata) if n == -1 else n

    print("Downloading {} of {} files".format(n, len(metadata)))

    for index in range(n):
        for each in metadata[index]["downloads"]:
            URL = PREFIX + each['links']['fulltext']
            response = requests.get(URL)
            open(URL.split("/")[-1], "wb").write(response.content)

if __name__ == "__main__":
    download_n_full_textfiles('collected_data.json', 100)
