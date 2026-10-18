# Assignment 13 - Data Gathering, Preprocessing & EDA
#
# Dataset:
# Students Performance in Exams
# Kaggle:
# https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
#
# I kept the code simple so that each step is easy to understand.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import sqlite3


# ==========================================================
# PART 1 - DATA GATHERING
# ==========================================================

# Task 1 - Load CSV

df = pd.read_csv("StudentsPerformance.csv")

print("Shape of CSV:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)


# Task 2 - Load JSON

# I made a small JSON file for practice.
json_data = [
    {"name": "Aman", "department": "IT", "salary": 35000},
    {"name": "Riya", "department": "HR", "salary": 32000},
    {"name": "Rahul", "department": "Sales", "salary": 30000}
]

with open("students_sample.json", "w") as file:
    import json
    json.dump(json_data, file, indent=4)

json_df = pd.read_json("students_sample.json")

print("\nJSON data:")
print(json_df)


# Task 3 - SQLite database

connection = sqlite3.connect("employees.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

cursor.execute("DELETE FROM employees")

employees = [
    (1, "Aman", "IT", 35000),
    (2, "Riya", "HR", 32000),
    (3, "Rahul", "Sales", 30000),
    (4, "Neha", "IT", 40000),
    (5, "Karan", "Finance", 38000)
]

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    employees
)

connection.commit()

sql_df = pd.read_sql_query(
    "SELECT * FROM employees",
    connection
)

print("\nEmployees from SQL:")
print(sql_df)

connection.close()


# Task 4 - TMDB API mini project
#
# Put your TMDB API key in the variable below before running
# this part. The rest of the assignment does not need an API key.

TMDB_API_KEY = ""

if TMDB_API_KEY != "":
    url = "https://api.themoviedb.org/3/movie/popular"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        movie_data = response.json()

        movies = []

        for movie in movie_data["results"]:
            movies.append({
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "rating": movie.get("vote_average"),
                "popularity": movie.get("popularity"),
                "overview": movie.get("overview")
            })

        movies_df = pd.DataFrame(movies)

        print("\nMovies collected from TMDB:")
        print(movies_df.head())

        movies_df.to_csv(
            "tmdb_movies.csv",
            index=False
        )

        print("\ntmdb_movies.csv saved.")
    else:
        print("TMDB request was not successful.")
else:
    print("\nTMDB API key is empty.")
    print("Add your own TMDB API key to run Task 4.")


# ==========================================================
# PART 2 - DATA PREPROCESSING & CLEANING
# ==========================================================

# Task 5 - Understanding the data

print("\n--- Understanding Data ---")
print("Shape:", df.shape)
print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nNumerical columns:")
print(df.select_dtypes(include=np.number).columns)

print("\nCategorical columns:")
print(df.select_dtypes(include="object").columns)


# Task 6 - Data cleaning

# Check duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

# Remove duplicates if there are any
df = df.drop_duplicates()

# Fill numerical missing values with median
numerical_columns = df.select_dtypes(include=np.number).columns

for column in numerical_columns:
    df[column] = df[column].fillna(df[column].median())

# Fill categorical missing values with mode
categorical_columns = df.select_dtypes(include="object").columns

for column in categorical_columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna(df[column].mode()[0])

# Rename columns
df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumns after renaming:")
print(df.columns)

# Convert score columns to numeric
score_columns = [
    "math_score",
    "reading_score",
    "writing_score"
]

for column in score_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Task 7 - Feature preparation

# Label encoding for one categorical column
df["gender_code"] = df["gender"].map({
    "female": 0,
    "male": 1
})

# One-hot encoding for another categorical column
df = pd.get_dummies(
    df,
    columns=["lunch"],
    dtype=int
)

print("\nData after encoding:")
print(df.head())


# Choose a target for practice
target = "math_score"

X = df.drop(columns=[target])
y = df[target]

print("\nFeature shape:", X.shape)
print("Target shape:", y.shape)


# ==========================================================
# PART 3 - EXPLORATORY DATA ANALYSIS
# ==========================================================

# Task 8 - Univariate analysis

# Histogram + KDE
sns.histplot(
    df["math_score"],
    kde=True
)
plt.title("Math Score Distribution")
plt.xlabel("Math Score")
plt.ylabel("Count")
plt.show()


# Count plot for categorical column
sns.countplot(
    data=df,
    x="gender"
)
plt.title("Number of Students by Gender")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()


# Boxplot for outliers
sns.boxplot(
    data=df,
    y="math_score"
)
plt.title("Math Score Boxplot")
plt.show()


# Task 9 - Bivariate analysis

# Numerical vs numerical
sns.scatterplot(
    data=df,
    x="math_score",
    y="reading_score"
)
plt.title("Math Score vs Reading Score")
plt.xlabel("Math Score")
plt.ylabel("Reading Score")
plt.show()


# Correlation heatmap
correlation = df[
    [
        "math_score",
        "reading_score",
        "writing_score"
    ]
].corr()

sns.heatmap(
    correlation,
    annot=True
)
plt.title("Score Correlation")
plt.show()


# Categorical vs numerical - bar plot
sns.barplot(
    data=df,
    x="gender",
    y="math_score"
)
plt.title("Average Math Score by Gender")
plt.xlabel("Gender")
plt.ylabel("Math Score")
plt.show()


# Categorical vs numerical - box plot
sns.boxplot(
    data=df,
    x="gender",
    y="math_score"
)
plt.title("Math Score by Gender")
plt.xlabel("Gender")
plt.ylabel("Math Score")
plt.show()


# Task 10 - Insights

print("\n--- Insights ---")

print("1. Math, reading and writing scores have a positive relationship.")

print("2. Reading and writing scores are generally higher than math scores.")

print("3. The boxplot can be used to identify unusually low or high scores.")

print("4. Students who completed the test preparation course can be compared")
print("   with students who did not complete it using group analysis.")

print("5. Gender is a categorical variable that can be compared with scores")
print("   using bar plots and box plots.")

print("\nEDA completed.")
