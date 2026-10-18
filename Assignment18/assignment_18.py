
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

print("="*65)
print("ASSIGNMENT 18: TEXT VECTORIZATION TECHNIQUES")
print("="*65)

# Load the same dataset used for the previous NLP assignment.
df = pd.read_csv("data/movie_reviews.csv")
texts = df["text"].fillna("").astype(str).tolist()
print("\nDATASET")
print("Shape:", df.shape)
print("Columns:", list(df.columns))

# ================================================================
# TASK 1 - MANUAL ONE-HOT ENCODING
# ================================================================
print("\nTASK 1 - MANUAL ONE-HOT ENCODING")

sentences = [
    "I love this movie",
    "This movie is good",
    "I love good movies",
    "The movie is interesting",
    "I like this movie"
]

vocab_list = []
for sentence in sentences:
    for word in sentence.lower().split():
        if word not in vocab_list:
            vocab_list.append(word)

vocab_dict = {word: index for index, word in enumerate(vocab_list)}

manual_rows = []
for sentence in sentences:
    words = set(sentence.lower().split())
    manual_rows.append([1 if word in words else 0 for word in vocab_list])

manual_df = pd.DataFrame(manual_rows, columns=vocab_list,
                         index=[f"Sentence {i}" for i in range(1, 6)])
print("Manual vocabulary:", vocab_dict)
print("Manual one-hot matrix:")
print(manual_df)

# ================================================================
# TASK 2 - CountVectorizer(binary=True)
# ================================================================
print("\nTASK 2 - CountVectorizer(binary=True)")

binary = CountVectorizer(binary=True)
binary_matrix = binary.fit_transform(sentences)
binary_vocab = binary.get_feature_names_out()
binary_df = pd.DataFrame(binary_matrix.toarray(), columns=binary_vocab,
                         index=[f"Sentence {i}" for i in range(1, 6)])
print("Vocabulary:", list(binary_vocab))
print("Encoded matrix:")
print(binary_df)

# ================================================================
# TASK 3 - BAG OF WORDS
# ================================================================
print("\nTASK 3 - BAG OF WORDS")

bow = CountVectorizer()
bow_matrix = bow.fit_transform(texts)
print("Vocabulary size:", len(bow.vocabulary_))
print("Matrix shape:", bow_matrix.shape)
print("First document vector (first 20 features):")
print(bow_matrix[0, :20].toarray())

# ================================================================
# TASK 4 - WORD FREQUENCY
# ================================================================
print("\nTASK 4 - UNDERSTANDING WORD FREQUENCY")

counts = np.asarray(bow_matrix.sum(axis=0)).ravel()
freq = pd.DataFrame({
    "word": bow.get_feature_names_out(),
    "frequency": counts
}).sort_values(["frequency", "word"], ascending=[False, True])

print("Top 10 most frequent words:")
print(freq.head(10).to_string(index=False))
print("\n10 least frequent words:")
print(freq.tail(10).sort_values(["frequency", "word"]).to_string(index=False))
print("\nBoW captures frequency because every document has one value for each vocabulary word.")
print("If a word appears several times in a document, its count is larger than 1.")

# Use a 5,000-review sample for n-gram experiments so the assignment runs
# comfortably on ordinary student laptops.
ngram_texts = texts[:5000]

# ================================================================
# TASK 5 - UNIGRAMS, BIGRAMS, TRIGRAMS
# ================================================================
print("\nTASK 5 - UNIGRAMS, BIGRAMS AND TRIGRAMS")

uni = CountVectorizer(ngram_range=(1,1), max_features=15000)
bi = CountVectorizer(ngram_range=(2,2), max_features=15000)
tri = CountVectorizer(ngram_range=(3,3), max_features=15000)

uni_m = uni.fit_transform(ngram_texts)
bi_m = bi.fit_transform(ngram_texts)
tri_m = tri.fit_transform(ngram_texts)

print("Unigram vocabulary:", len(uni.vocabulary_))
print("Bigram vocabulary:", len(bi.vocabulary_))
print("Trigram vocabulary:", len(tri.vocabulary_))
print("Example bigrams:", list(bi.get_feature_names_out()[:10]))
print("Example trigrams:", list(tri.get_feature_names_out()[:10]))

# ================================================================
# TASK 6 - COMBINED N-GRAMS (1,3)
# ================================================================
print("\nTASK 6 - COMBINED N-GRAMS (1,3)")

combined = CountVectorizer(ngram_range=(1,3), max_features=30000)
combined_m = combined.fit_transform(ngram_texts)

print("ngram_range=(1,3)")
print("Combined vocabulary:", len(combined.vocabulary_))
print("Combined matrix shape:", combined_m.shape)
print("Example combined features:", list(combined.get_feature_names_out()[:15]))
print("Observation: unigrams show individual words, while bigrams/trigrams add local phrase context.")
print("The extra context comes at the cost of a larger feature space.")

# ================================================================
# TASK 7 - TF-IDF
# ================================================================
print("\nTASK 7 - TF-IDF")

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(texts)
print("TF-IDF vocabulary:", len(tfidf.vocabulary_))
print("TF-IDF matrix shape:", tfidf_matrix.shape)

# ================================================================
# TASK 8 - BoW VS TF-IDF
# ================================================================
print("\nTASK 8 - BoW VS TF-IDF")

mean_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
tfidf_df = pd.DataFrame({
    "word": tfidf.get_feature_names_out(),
    "mean_tfidf": mean_scores
})

high = tfidf_df.sort_values("mean_tfidf", ascending=False).head(10)
low = tfidf_df[tfidf_df.mean_tfidf > 0].sort_values("mean_tfidf").head(10)

print("HIGH average TF-IDF words:")
print(high.to_string(index=False))
print("\nLOW non-zero average TF-IDF words:")
print(low.to_string(index=False))
print("\nCommon words are down-weighted because inverse document frequency becomes smaller")
print("when a word occurs in many documents.")
print("BoW uses raw counts; TF-IDF emphasizes words that are more useful for distinguishing documents.")

# ================================================================
# TASK 9 - min_df AND max_df
# ================================================================
print("\nTASK 9 - VECTORIZER PARAMETER EXPLORATION")

print("min_df experiment:")
min_results = []
for value in [1, 5, 10, 20]:
    v = CountVectorizer(min_df=value)
    m = v.fit_transform(texts)
    min_results.append((value, len(v.vocabulary_)))
    print("min_df =", value, "-> vocabulary size =", len(v.vocabulary_))

print("\nmax_df experiment:")
max_results = []
for value in [1.0, 0.95, 0.90, 0.80]:
    v = CountVectorizer(max_df=value)
    m = v.fit_transform(texts)
    max_results.append((value, len(v.vocabulary_)))
    print("max_df =", value, "-> vocabulary size =", len(v.vocabulary_))

print("\nObservation: increasing min_df removes rare words, so vocabulary size falls.")
print("Lowering max_df removes words occurring in too many documents, also reducing vocabulary.")

# ================================================================
# TASK 10 - CONCEPTUAL QUESTIONS
# ================================================================
print("\nTASK 10 - CONCEPTUAL QUESTIONS")

print("1. One-Hot vs BoW:")
print("One-hot encoding marks whether a word is present with 0/1. BoW counts word occurrences in each document.")

print("\n2. Why do N-grams increase dimensionality?")
print("Bigrams and trigrams create extra word-sequence features, so many more features can be produced than with unigrams.")

print("\n3. When prefer TF-IDF over BoW?")
print("Use TF-IDF when common words should have less influence and document-specific words should have more influence.")

print("\n4. Limitations of count-based vectorization:")
print("Vectors can be sparse and high-dimensional; basic BoW does not capture word meaning well and mostly loses word order.")

manual_df.to_csv("task1_manual_one_hot.csv")
binary_df.to_csv("task2_binary_one_hot.csv")
freq.to_csv("task4_word_frequency.csv", index=False)
high.to_csv("task8_high_tfidf.csv", index=False)
low.to_csv("task8_low_tfidf.csv", index=False)

print("\n" + "="*65)
print("ALL 10 TASKS COMPLETED")
print("="*65)
