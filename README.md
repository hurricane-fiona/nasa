# Towards preserving our science legacy: Building a topically-aware, searchable, and accessible system
![Contributors](https://img.shields.io/github/contributors/mmaisonnave/unplanned-hospital-readmission-prediction?style=plastic)
![Forks](https://img.shields.io/github/forks/mmaisonnave/unplanned-hospital-readmission-prediction)
![Stars](https://img.shields.io/github/stars/mmaisonnave/unplanned-hospital-readmission-prediction)
![GitHub](https://img.shields.io/github/license/mmaisonnave/unplanned-hospital-readmission-prediction?style=round-square)
![Issues](https://img.shields.io/github/issues/mmaisonnave/unplanned-hospital-readmission-prediction)


The current state of the NASA Technical Report Server (NTRS) repository limits its usability, since the current filter-based system is only useful when the user knows exactly what he/she is looking for. To address this issue, we created an enhanced search engine that displays the topics in the collection before showing the relevant documents. Being able to compare the search results in terms of their topics allows the user to explore the results more efficiently and have a better understanding of them. In our system, users submit a query and then select the topics they are interested in, which are then used to guide the retrieval process, enhancing the results from a state-of-the-art search engine.

[Project submission](https://2022.spaceappschallenge.org/challenges/2022-challenges/science-legacy/teams/fiona/project)

[Prototype](http://fionaai.earth:37639/)

[30-second Pitch](https://www.youtube.com/watch?v=LcE-qipy2kk)

# Features

Our system models the topics in the corpus by estimating their distribution on the whole corpus using the implementation of Latent Dirichlet Allocation of the Scikit-Learn library. When a user searches for a key phrase, the system maps that query into the same representation as the topics, i.e., the same topic space, and displays the topics related to the query in a 2D scatter plot. The user can then filter the desired topics through a visualization displayed on our application’s dashboard. Once the topics are filtered, the user receives query results based on the desired topics. Statistics for each of the search results like word frequency count and summary are also displayed to summarize the query results to inform the user of the contents of the document.

# Installation

    git clone https://github.com/hurricane-fiona/nasa.git
    cd nasa
    pip install -r requirements.txt
    python article_downloader/metadata_fetcher.py
    python article_downloader/download_fulltext.py
    python search_engine/whoosh_engine.py
    
# Usage

    python app.py

# Contribute and Support

- [Issue Tracker](https://github.com/hurricane-fiona/nasa/issues)
- [Pull Requests](https://github.com/hurricane-fiona/nasa/pulls)

# License

This project is licensed under the MIT License
