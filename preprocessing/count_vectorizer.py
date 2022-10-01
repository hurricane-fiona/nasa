from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def high_frequency_words(file, max_words=15):
    text=open(file,'r').read()
    vectorizer = CountVectorizer(stop_words='english', 
                                 input='content',
                                 ngram_range=(1, 3), 
                                 token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z][a-zA-Z]+\b" )
    X = vectorizer.fit_transform([text])
    words = vectorizer.get_feature_names_out()[np.argsort(X.toarray()[0,:])[::-1]]
    scores = X.toarray()[0,:][np.argsort(X.toarray()[0,:])[::-1]]
    return list(zip(words,scores))[:max_words]