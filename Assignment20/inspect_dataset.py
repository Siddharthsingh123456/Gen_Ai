import pandas as pd

path = "data/tmdb_5000_movies_sample.csv"
movies = pd.read_csv(path)

print("DATASET SHAPE:")
print(movies.shape)

print("\nCOLUMN NAMES:")
print(movies.columns.tolist())

print("\nFIRST 5 ROWS:")
print(movies.head())

print("\nTEXT COLUMN DETAILS:")
for col in ["overview", "genres", "keywords"]:
    print(col, "missing values:", movies[col].isna().sum())
