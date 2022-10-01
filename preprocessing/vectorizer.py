from sklearn.feature_extraction.text import TfidfVectorizer
import os
import spacy
import string
import pickle 
from scipy import sparse


def vectorize(files, store=False):

    nlp = spacy.load('en_core_web_sm')

    def lemmatize(text):
        text_list=[]
        for ini in range(0, len(text), 1000000): # 1000000
            fin = min(ini+1000000, len(text))
            text_fragment = text[ini:fin] 
            tokens = nlp(text_fragment)
            for token in list(tokens)[::-1]:
                if token.lemma_ != token.text:
                    text_fragment = text_fragment[:token.idx] + token.lemma_ + text_fragment[token.idx+len(token.text):]
            text_list.append(text_fragment)
        return ''.join(text_list).lower()

    vectorizer = TfidfVectorizer(input='filename',
                                 ngram_range=(1, 3), 
                                 max_features=10000, 
                                 max_df=0.8, 
                                 min_df=0.01, 
                                 preprocessor=lemmatize,
                                 stop_words='english', 
                                 token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z][a-zA-Z]+\b" ) 
    X = vectorizer.fit_transform(files)


    if store:
        pickle.dump(vectorizer , open('vectorizer.pkl', 'wb'))

        for idx,file in enumerate(files):
            file = file.replace('txt','npz')
            sparse.save_npz(file, X[idx,:])

    return vectorizer, X