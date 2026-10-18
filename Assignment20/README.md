# Assignment 20 – Building & Deploying a Recommendation System

## Project
Content-based Movie Recommendation System using:
- Python
- Pandas
- scikit-learn
- Streamlit
- Git/GitHub
- Render

## Dataset
**TMDB 5000 Movie Dataset**

Original Kaggle source:
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

The included `data/tmdb_5000_movies_sample.csv` is a compact sample of records from the same TMDB 5000 dataset so the project can be executed and tested without requiring Kaggle credentials.

For the complete assignment dataset, run:
`python download_kaggle_dataset.py`

The application then uses the complete `tmdb_5000_movies.csv` file.

## Task mapping
### Task 1 – Load & Understand Dataset
`inspect_dataset.py` prints shape, column names, first five rows and text-column missing values.

### Task 2 – Text Preprocessing
The recommender lowercases text, removes special characters, removes extra spaces and replaces missing text with empty strings.

### Task 3 – TF-IDF
`TfidfVectorizer(stop_words="english", ngram_range=(1, 2))` converts combined overview/genres/keywords text into vectors.

### Task 4 – Similarity
Cosine similarity is calculated between all movie vectors.

### Task 5 – Recommendation
`recommend(movie_name, n=5)` sorts cosine scores and returns the top recommendations.

### Task 6 – Streamlit
`app.py` provides a movie selector and displays recommendations and similarity scores.

### Task 7 – GitHub
Push all project files to your GitHub repository.

### Task 8 – Render
Use the included `Procfile`:
`web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Task 9 – Validation
The project tests three different movies:
- Avatar
- The Dark Knight Rises
- Interstellar

See `tests/TEST_RESULTS.csv`.

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important
GitHub repository creation/push and Render deployment require access to the student's own accounts. This ZIP contains the deployment-ready configuration, but it does not falsely claim an external deployment that has not been performed.
