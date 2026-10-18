# Assignment 14
# Feature Engineering, Encoding, Scaling and Pipelines
#
# Dataset: Students Performance in Exams
# Kaggle:
# https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
#
# I kept the code simple and used the same dataset as the previous task.

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression


# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("StudentsPerformance.csv")

print("Shape:")
print(df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nColumns:")
print(df.columns)


# -----------------------------
# Task 1 - Feature Engineering
# -----------------------------

# I used math and reading scores to make a new total.
# I did not include writing score here because writing score
# is the target that I will predict later.

df["total_score"] = df["math score"] + df["reading score"]

df["average_score"] = df["total_score"] / 2

print("\nNew columns:")
print(df[[
    "math score",
    "reading score",
    "total_score",
    "average_score"
]].head())


# -----------------------------
# Task 2 - Date and text
# -----------------------------

# There is no date column in this dataset.
# There is also no long free-text column.
# So date extraction and text length are skipped.

print("\nDate/text task:")
print("No date column is available.")
print("No free-text column is available.")


# -----------------------------
# Task 3 - One-Hot Encoding
# -----------------------------

categorical_columns = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course"
]

encoded = pd.get_dummies(
    df[categorical_columns],
    dtype=int
)

print("\nOne-hot encoded data:")
print(encoded.head())

print("\nEncoded columns:")
print(encoded.columns)


# -----------------------------
# Task 4 - ColumnTransformer
# -----------------------------

numeric_columns = [
    "math score",
    "reading score",
    "total_score",
    "average_score"
]

# Writing score is the target.
target = df["writing score"]

X = df[numeric_columns + categorical_columns]

preprocessor = ColumnTransformer([
    ("numbers", "passthrough", numeric_columns),
    ("categories", OneHotEncoder(handle_unknown="ignore"),
     categorical_columns)
])

X_ready = preprocessor.fit_transform(X)

print("\nColumnTransformer result:")
print("Rows:", X_ready.shape[0])
print("Columns:", X_ready.shape[1])


# -----------------------------
# Task 5 - StandardScaler
# -----------------------------

scaler = StandardScaler()

scaled = scaler.fit_transform(
    df[["math score", "reading score"]]
)

scaled_df = pd.DataFrame(
    scaled,
    columns=["math score", "reading score"]
)

print("\nStandardScaler:")
print(scaled_df.head())

print("\nMean after scaling:")
print(scaled_df.mean())


# -----------------------------
# Task 6 - MinMaxScaler
# -----------------------------

minmax = MinMaxScaler()

normal = minmax.fit_transform(
    df[["math score", "reading score"]]
)

normal_df = pd.DataFrame(
    normal,
    columns=["math score", "reading score"]
)

print("\nMinMaxScaler:")
print(normal_df.head())

print("\nMinimum values:")
print(normal_df.min())

print("\nMaximum values:")
print(normal_df.max())


# -----------------------------
# Task 7 - Preprocessing Pipeline
# -----------------------------

number_pipe = Pipeline([
    ("scale", StandardScaler())
])

category_pipe = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocess = ColumnTransformer([
    ("number", number_pipe, numeric_columns),
    ("category", category_pipe, categorical_columns)
])

print("\nPreprocessing pipeline created.")


# -----------------------------
# Task 8 - Full Pipeline
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    target,
    test_size=0.2,
    random_state=42
)

model = Pipeline([
    ("preprocess", preprocess),
    ("linear_regression", LinearRegression())
])

model.fit(X_train, y_train)

prediction = model.predict(X_test)

print("\nFirst five actual values:")
print(y_test.head().values)

print("\nFirst five predictions:")
print(prediction[:5])


# -----------------------------
# Task 9 - Pipeline Benefits
# -----------------------------

print("\nPipeline benefits:")

print("1. It keeps preprocessing and the model together.")
print("2. The same preprocessing is used during prediction.")
print("3. It reduces repeated preprocessing code.")
print("4. It helps avoid applying different transformations to train and test data.")


# -----------------------------
# Small comparison
# -----------------------------

print("\nComparison:")
print("StandardScaler changes values around mean 0.")
print("MinMaxScaler changes values to a range from 0 to 1.")
print("The pipeline combines preprocessing with Linear Regression.")

print("\nAssignment 14 completed.")
