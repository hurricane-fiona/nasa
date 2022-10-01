import json
import NTRSClient
import glob
import os

JSON_DIR_PATH = "/home/ubuntu/nasa/metadata/"
FULL_TEXT_DIR_PATH = "/home/ubuntu/nasa/data/real/fulltext/"

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
            URL = each['links']['fulltext']
            download_and_save(URL)


def download_and_save(url):
    content = NTRSClient.download(url)
    open(os.path.join(FULL_TEXT_DIR_PATH, url.split("/")[-1]), "wb").write(content)

def download_from_dir(dir_path):
    json_files = glob.glob(JSON_DIR_PATH + "*.json")
    txt_files = glob.glob(FULL_TEXT_DIR_PATH + "*.txt")
    to_download = list(set([each.split("/")[-1].replace(".json", "") for each in json_files]) - set([each.split("/")[-1].replace(".txt", "") for each in txt_files]))
    to_download = [JSON_DIR_PATH + each+".json" for each in to_download]
    
    print("{} files exist. Downloading {}".format(len(txt_files), len(to_download)))

    print(to_download)
    for index, metadata_file in enumerate(to_download):
        print("Downloading {} of {} files".format(index, len(json_files)))
        for each in metadata[index]["downloads"]:
            URL = each['links']['fulltext']
            download_and_save(URL)


if __name__ == "__main__":
    # download_n_full_textfiles('collected_data.json', 100)
    
    download_from_dir(JSON_DIR_PATH)
