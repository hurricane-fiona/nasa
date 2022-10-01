import pandas as pd
import json
  
def get_dummy_data():
    # Opening JSON file
    f = open('JSONs/collected_data.json')

    # returns JSON object as 
    # a dictionary
    d = {
        'title': [],
        'abstract': [], 
        'id': [],
    }
    data = json.load(f)

    # Iterating through the json
    # list
    for data_item in data:
        title = data_item['title'] if 'title' in data_item else ''
        abstract = data_item['abstract'] if 'abstract' in data_item else ''
        id_ = data_item['id'] if 'id' in data_item else ''

        d['title'].append(title)
        d['abstract'].append(abstract)
        d['id'].append(id_)

    # Closing file
    f.close()

    df = pd.DataFrame(d)
    return df.set_index('id')

if __name__ == "__main__":
    corpus = get_dummy_data()
    print("corpus", corpus.shape)
    print("writing corpus as pickle...")
    corpus.to_pickle("dummy.pkl")
    print(corpus.head())
    print("\ndone!")
