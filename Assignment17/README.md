# Assignment 17 - Text Cleaning, Preprocessing & NLP Pipeline

This folder follows the 10 tasks in the supplied TuteDude brief.

## Dataset
A 30-sample text dataset was made from the supplied movie-review CSV.

- File: `data/text_dataset_30.csv`
- Samples used: 30
- Text column: `text`
- Source: Large Movie Review Dataset (IMDb), Andrew Maas et al., Stanford AI Lab.
- Source page: https://ai.stanford.edu/~amaas/data/sentiment/

## Tasks
1. Understand raw text data
2. Basic cleaning
3. Advanced noise removal
4. Stopword removal
5. Repeated characters and slang
6. Word and sentence tokenization
7. Porter stemming
8. WordNet lemmatization
9. Final `nlp_preprocess(text)` function
10. Observations and insights

The notebook and Python file use the same straightforward implementation so the steps can be followed easily.

## Run
```bash
python assignment_17.py
```

The run notes contain actual execution observations from this environment. The environment did not have the NLTK corpora downloaded, so the script records that issue and uses small fallbacks for the offline run. On a local machine with NLTK data installed, the NLTK resources will be used.
