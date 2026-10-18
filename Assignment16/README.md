# Assignment 16 - NLP Text Preprocessing

This submission follows the 10 NLP preprocessing tasks described in the tutor feedback.

## Dataset
A 30-sample text dataset was created from the previously supplied 25,000-row IMDb-style movie-review CSV. The text column is `text`.

Source information:
- Large Movie Review Dataset (IMDb)
- Andrew Maas et al., Stanford AI Lab
- https://ai.stanford.edu/~amaas/data/sentiment/

## Tasks covered
1. Load text dataset, first five samples, text lengths and raw-text issues
2. Basic cleaning: lowercase, punctuation, numbers, whitespace
3. Advanced noise removal: URLs, emails, HTML, special characters/emojis
4. NLTK stopwords and `text_no_stopwords`
5. Repeated-character normalization and slang dictionary
6. Word and sentence tokenization, with 3 sample demonstrations
7. Porter stemming and original/stem comparison
8. WordNet lemmatization and stemming/lemmatization comparison
9. `nlp_preprocess(text)` applied to the complete 30-row assignment dataset
10. Detailed observations and insights

## Important
The code uses NLTK. The execution environment used for this package did not have the NLTK corpora downloaded and had no network access, so the code records that fact and uses small fallbacks for stopwords/tokenization/lemmatization so the assignment can still execute. On a normal NLTK installation, the NLTK resources are used directly.

Run:
```bash
python assignment_16_nlp.py
```
