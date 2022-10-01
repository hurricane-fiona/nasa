from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import string
import json
import re
import sys
import os


##################
# CREATING INDEX #
##################
if __name__=='__main__':    
    input_=' '.join(sys.argv[1:])
    ########
    # HELP #
    ########
    if re.search('--help',input_):
        print('USAGE: python whoosh_engine.py --data-folder=example_folder/')
        sys.exit(0)

    ###############
    # DATA FOLDER #
    ###############
    if not re.search('--data-folder=[^\ ][^\ ]*',input_):
        print('Please provide a valid data folder (--data-folder=example_folder/)')
        sys.exit(1)
    
    data_folder = re.findall('--data-folder=([^\ ][^\ ]*)',input_)[0]
    if not os.path.exists(data_folder):
        print('Data folder does not exist, please provide valid data folder.')
        sys.exit(2)

    ###################
    # METADATA FOLDER #
    ###################
    if not re.search('--metadata-folder=[^\ ][^\ ]*',input_):
        print('Please provide a valid data folder (--data-metadata=example_folder/)')
        sys.exit(3)
    
    metadata_folder = re.findall('--metadata-folder=([^\ ][^\ ]*)',input_)[0]
    if not os.path.exists(data_folder):
        print('Data folder does not exist, please provide valid data folder.')
        sys.exit(4)
    
    ###########
    # RUNNING #
    ###########
    print('Defining Schema ...',end='')
    schema = Schema(ID=ID(stored=True),
                    title=TEXT(analyzer=StemmingAnalyzer(), sortable=True),
                    abstract=TEXT(analyzer=StemmingAnalyzer(), sortable=True),
                    body=TEXT(analyzer=StemmingAnalyzer(), sortable=True),
                    authors=KEYWORD(stored=False,),
                   )
    print('[OK]')


    # CREATING INDEX
    import os
    from whoosh import index

    if not os.path.exists("index"):
        print('Creating index folder ...',end='')
        os.mkdir("index")
    else:
        print('Using index/ folder ...',end='')
    print('[OK]')
    ix = index.create_in("index", schema)


    print(f'Using data folder: {data_folder}')
    files = [os.path.join(metadata_folder,file) for file in os.listdir(metadata_folder) if file.endswith('json')]
    print(f'Processing {len(files)} JSON files ....',end='')

    writer = ix.writer()

    def parse_authors(author_list):
        str_=' '.join(author_list)
        str_= str_.translate(str.maketrans('', '', string.punctuation))
        return ' '.join(elem for elem in  str_.split(' ') if len(elem)>1)


    count_txt = 0
    for file in files: 
        id_ = file.split('/')[-1][:-len('.json')]

        data = json.load(open(file))
        text=''
        if os.path.isfile(file.replace('.json','.txt').replace(metadata_folder, data_folder)):
            text = open(file.replace('.json','.txt').replace(metadata_folder,data_folder),'r').read()
            count_txt+=1

        title = data['title'] if 'title' in data else ''
        abstract = data['abstract'] if 'abstract' in data else ''
        try:
            authors = [author['meta']['author']['name'] for author in data['authorAffiliations']]
        except:
            authors=[]
        authors = parse_authors(authors)

        writer.add_document(ID=id_, title=title, abstract=abstract, body=text,
                            authors=authors,)
    print('[OK]')

    print(f'All JSON files processed, found {count_txt} TXT files associated.')
    writer.commit()


    print('Index built!')

#############
# SEARCHING #
#############
import whoosh.index as index
from whoosh.qparser import QueryParser,MultifieldParser
from whoosh.scoring import MultiWeighting

def get_data_path():
    return 'data/real/fulltext/'
def get_metadata_path():
    return 'metadata'
def get_index_path():
    return  'data/real/index/'


def _search(query, limit):
    ix = index.open_dir(get_index_path())
    searcher = ix.searcher()

    qp = MultifieldParser(['ID', 'title', 'abstract', 'body', 'authors'], schema=ix.schema)
    q = qp.parse(query)

    hits=[]
    with ix.searcher( ) as s:
        results = s.search(q, limit=limit)
        hits=[(result['ID'], result.score) for result in results]
    return hits


import pandas as pd


BASE_NTRS_URL = "https://ntrs.nasa.gov"

def compute_relevance(query,limit=20):
    hits = _search(query, limit=limit)
    d = {
    'title': [],
    'abstract': [], 
    'id': [],
    'keywords':[],
    'score': [],
    'text_link':[],
    'pdf_link':[],
    'authors':[],
            }
    for id_, score in hits:
        f = open(os.path.join(get_metadata_path(),f'{id_}.json'))

        # returns JSON object as 
        # a dictionary

        data_item = json.load(f)

        d['score'].append(score)

        # Iterating through the json
        # list
    #             for data_item in data:
        title = data_item['title'] if 'title' in data_item else ''
        abstract = data_item['abstract'] if 'abstract' in data_item else ''
        id_ = data_item['id'] if 'id' in data_item else ''
        keywords = ';'.join(data_item['subjectCategories']) if 'subjectCategories' in data_item else ''

        d['title'].append(title)
        d['abstract'].append(abstract)
        d['id'].append(id_)
        d['keywords'].append(keywords)
        
        try:
            authors = [author['meta']['author']['name'] for author in data['authorAffiliations']]
        except:
            authors = []
        authors = ';'.join(authors)
        d['authors'].append(authors)

        try: 
            text_link = BASE_NTRS_URL + data_item['downloads'][0]['links']['fulltext']
        except:
            text_link=''

        try:
            pdf_link = BASE_NTRS_URL + data_item['downloads'][0]['links']['pdf'] 
        except:
            pdf_link=''
        d['text_link'].append(text_link)
        d['pdf_link'].append(pdf_link)
        
        # Closing file
        f.close()

    df = pd.DataFrame(d)
    return df.set_index('id')
    
    
# import numpy as np

# def compute_relevance(
#     query,
#     documents
# ):
#     return np.random.rand(len(documents))



