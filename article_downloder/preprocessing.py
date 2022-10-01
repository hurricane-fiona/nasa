from sklearn.feature_extraction.text import TfidfVectorizer
import os
import string
import pickle 
import spacy



files = [file for file in  os.listdir('.')  if file.endswith('txt')]

print(f'Processing {len(files)} files (txt).')

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


print('Lemmatizing corpus and building TF-IDF')
vectorizer = TfidfVectorizer(input='filename',
                             ngram_range=(1, 3), 
                             max_features=10000, 
                             max_df=0.8, 
                             min_df=0.01, 
                             preprocessor=lemmatize,
                             stop_words='english', 
                             token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z][a-zA-Z]+\b" ) 
X = vectorizer.fit_transform(files)


print('Saving vectorizer object')
pickle.dump(vectorizer , open('vectorizer.pkl', 'wb'))

print('Saving NPZ files')
from scipy import sparse
for idx,file in enumerate(files):
    file = file.replace('txt','npz')
    sparse.save_npz(file, X[idx,:])
    
    
print('FINISH')
