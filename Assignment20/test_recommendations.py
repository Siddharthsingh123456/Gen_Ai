from recommender import load_data, build_model, recommend

df = load_data()
df, vectorizer, matrix, similarity = build_model(df)

test_movies = ["Avatar", "The Dark Knight Rises", "Interstellar"]

for movie in test_movies:
    print("\nINPUT:", movie)
    results = recommend(movie, df, similarity, n=5)
    for title, score in results:
        print(f"{title}: {score:.4f}")
