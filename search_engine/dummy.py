import numpy as np
import pandas as pd

corpus = pd.read_pickle("data/dummy/dummy.pkl")

def compute_relevance(
    query,
):
    scores = np.random.rand(corpus.shape[0])
    output = corpus.assign(
        relevance = scores
    ).\
    sort_values("relevance", ascending = False)

    return output
