# Assignment A20 - Word2Vec Text Embeddings

This is the corrected notebook submission based on the supplied Assignment 19 brief and tutor requirements.

## Files
- Assignment_20_Word2Vec_Embeddings.ipynb — executed notebook
- MY_RUN_NOTES.txt — actual execution results
- data/custom_word2vec_corpus.csv — 40-sentence custom dataset
- similarity_results.csv — three similarity pairs
- analogy_results.csv — king - man + woman results
- plots/word2vec_pca.png — PCA visualization
- plots/word2vec_tsne.png — t-SNE visualization

## Dataset source
Custom educational corpus created specifically for this assignment. It is not copied from an external dataset.

## Model settings
vector_size=100
window=5
min_count=1
CBOW sg=0
Skip-Gram sg=1
workers=1
seed=42
epochs=50

The 40 sentences are repeated during training to give the model more training examples. Repetition does not add new vocabulary or new text content.
