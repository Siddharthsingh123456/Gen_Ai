import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "data/tmdb_5000_movies_sample.csv"

def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value).lower()
    value = re.sub(r"[^a-z0-9\\s]", " ", value)
    value = re.sub(r"\\s+", " ", value)
    return value.strip()

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    required = ["title", "overview", "genres", "keywords"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    return df

def build_model(df):
    df = df.copy()
    df["text"] = (
        df["overview"].fillna("") + " " +
        df["genres"].fillna("") + " " +
        df["keywords"].fillna("")
    ).map(clean_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )
    matrix = vectorizer.fit_transform(df["text"])
    similarity = cosine_similarity(matrix)
    return df, vectorizer, matrix, similarity

def recommend(movie_name, df, similarity, n=5):
    matches = df.index[df["title"].str.lower() == movie_name.lower()].tolist()
    if not matches:
        return []

    movie_index = matches[0]
    scores = list(enumerate(similarity[movie_index]))
    scores.sort(key=lambda item: item[1], reverse=True)

    results = []
    for index, score in scores:
        if index == movie_index:
            continue
        results.append((df.iloc[index]["title"], float(score)))
        if len(results) == n:
            break
    return results
