# Assignment 14 - Feature Engineering, Encoding, Scaling & Pipelines

## Dataset

**Students Performance in Exams**

Kaggle source:

https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

The same dataset from the previous assignment is used here.

### Columns used

Numerical:
- math score
- reading score
- writing score

Categorical:
- gender
- race/ethnicity
- parental level of education
- lunch
- test preparation course

### Target

`writing score`

This is a regression problem because the target is a numerical score.

---

## Task 1 - Feature Engineering

Two new features are created:

### total_score

`math score + reading score`

### average_score

`total_score / 2`

I used math and reading for these features because `writing score` is the
target. This avoids directly putting the target into a newly created feature.

---

## Task 2 - Date and Text Features

The dataset does not contain a date column or a free-text column.

Therefore:

- Date extraction is skipped.
- Text length/word count is skipped.

---

## Task 3 - One-Hot Encoding

Categorical columns are converted using:

```python
pd.get_dummies()
```

This creates 0/1 columns for the categories.

---

## Task 4 - ColumnTransformer

`ColumnTransformer` is used to keep numerical and categorical columns
separate.

- Numerical columns are passed through.
- Categorical columns are changed with `OneHotEncoder`.

---

## Task 5 - Standardization

`StandardScaler` is applied to math and reading scores.

The result has values centered around mean 0.

---

## Task 6 - Normalization

`MinMaxScaler` is applied to the same numerical columns.

The values are changed to a range between 0 and 1.

---

## Task 7 - Preprocessing Pipeline

Two small pipelines are created:

**Numerical pipeline**

StandardScaler

**Categorical pipeline**

OneHotEncoder

They are combined using `ColumnTransformer`.

---

## Task 8 - Full Pipeline

The data is split into training and testing data.

The final pipeline is:

```text
Preprocessing
     ↓
Linear Regression
```

The pipeline is fitted on the training data and predictions are made on
the test data.

No hyperparameter tuning is performed.

---

## Task 9 - Pipeline Benefits

1. Preprocessing and model steps stay together.
2. The same transformations are used during prediction.
3. Repeated preprocessing code is reduced.
4. It helps keep the train/test preprocessing consistent.

---

## Why this version was simplified

The previous submission was too polished and contained more code than was
needed for a learning assignment.

This version intentionally uses:

- simple variable names
- small sections
- direct Pandas/scikit-learn statements
- basic comments
- no custom classes
- no unnecessary functions
- no hyperparameter tuning
- no production-style error handling

### Important

Do not submit a made-up "learning journey" or fake mistakes. Run the script
yourself and add your own genuine notes if your mentor asks for your personal
debugging process.

For example, after running it, record:

- one thing that worked
- one thing you initially did not understand
- what you changed
- what the output showed

These should be your actual observations.

---

## Installation

```text
pip install pandas scikit-learn
```

## Run

Keep these files in the same folder:

```text
Assignment_14_Feature_Engineering_Pipelines.py
StudentsPerformance.csv
```

Then run:

```text
python Assignment_14_Feature_Engineering_Pipelines.py
```
