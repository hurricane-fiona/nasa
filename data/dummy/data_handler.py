import pandas as pd
import json

BASE_NTRS_URL = "https://ntrs.nasa.gov"

def get_dummy_data():
    # Opening JSON file
    f = open('JSONs/collected_data.json')

    # returns JSON object as 
    # a dictionary
    d = {
        'title': [],
        'abstract': [],
        'id': [],
        'keywords':[],
        'text_link': [],
        'pdf_link': []
    }
    data = json.load(f)

    # Iterating through the json
    # list
    for data_item in data:
        title = data_item['title'] if 'title' in data_item else ''
        abstract = data_item['abstract'] if 'abstract' in data_item else ''
        id_ = data_item['id'] if 'id' in data_item else ''
        keywords = ';'.join(data_item['subjectCategories']) if 'subjectCategories' in data_item else ''
        text_link = BASE_NTRS_URL + data_item['downloads'][0]['links']['fulltext'] if 'downloads' in data_item and 'fulltext' in data_item['downloads'][0]['links'] else ''
        pdf_link = BASE_NTRS_URL + data_item['downloads'][0]['links']['pdf'] if 'downloads' in data_item and 'pdf' in data_item['downloads'][0]['links'] else ''

        d['title'].append(title)
        d['abstract'].append(abstract)
        d['id'].append(id_)
        d['keywords'].append(keywords)
        d['text_link'].append(text_link)
        d['pdf_link'].append(pdf_link)


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
