# Assignment 13 - Data Gathering, Preprocessing & EDA

## Dataset used

**Dataset:** Students Performance in Exams

**Kaggle source:**  
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

The Kaggle page describes the dataset as student marks in different
subjects and includes demographic/background columns. citeturn0search0

The same `StudentsPerformance.csv` dataset was used in the previous
assignments so that the preprocessing and EDA work continues with the same
data.

---

## Files in this folder

- `Assignment_13_Data_Gathering_Preprocessing_EDA.py`
- `StudentsPerformance.csv`
- `students_sample.json`
- `employees.db`
- `README.md`
- `Revision_Notes.txt`

`tmdb_movies.csv` is created when Task 4 is run with a valid TMDB API key.

---

## Part 1 - Data Gathering

### Task 1 - CSV

Loaded `StudentsPerformance.csv` using Pandas and checked:

- Shape
- Column names
- First five rows
- Data types

### Task 2 - JSON

Created a small JSON file and loaded it into a DataFrame.

### Task 3 - SQL

Created a SQLite database containing an `employees` table with:

- id
- name
- department
- salary

Inserted five records and read the table using a SQL query.

### Task 4 - TMDB API

The Python file contains a simple `requests` example for the TMDB popular
movies API.

To use it:

1. Create a free TMDB account.
2. Get an API key.
3. Put the key in `TMDB_API_KEY` in the Python file.
4. Run the file.
5. The movie information is saved as `tmdb_movies.csv`.

The API section extracts:

- Movie title
- Release date
- Rating
- Popularity
- Overview

---

## Part 2 - Data Preprocessing

The following checks/steps are included:

- Dataset shape
- Data types
- Numerical columns
- Categorical columns
- Missing values
- Duplicate values
- Median for numerical missing values
- Mode for categorical missing values
- Lowercase column names
- Snake_case column names
- Numeric conversion for score columns
- Label encoding for gender
- One-hot encoding for lunch
- Feature and target separation

Target selected for practice:

`math_score`

---

## Part 3 - EDA

### Univariate analysis

- Math score histogram + KDE
- Gender count plot
- Math score boxplot

### Bivariate analysis

- Math score vs reading score scatter plot
- Correlation heatmap
- Gender vs math score bar plot
- Gender vs math score box plot

---

## My revision / learning notes

The mentor feedback said that the previous work looked too polished and
production-like. I changed this version to keep the steps close to the
assignment questions.

I also avoided unnecessary functions/classes and kept the main work in
simple sections so I can explain it.

### What I learned

**CSV:** Pandas can read a CSV directly into a DataFrame.

**JSON:** JSON data can also be converted into a DataFrame.

**SQL:** `read_sql_query()` can run a SQL query and return a DataFrame.

**Missing values:** Numerical values can use the median and categorical
values can use the mode.

**Encoding:** A category can be changed to numbers with `map()`, while
`get_dummies()` can create separate columns for categories.

**EDA:** Graphs help me understand distributions, relationships and possible
outliers before building a model.

### About the revision process

I did not add fake errors or fake screenshots to make the work look
"student-written". Instead, the revision record explains the actual changes
made after the mentor feedback:

1. Simplified the code structure.
2. Kept each task in its own section.
3. Removed unnecessary production-style functions.
4. Added the Kaggle source clearly.
5. Added simple comments explaining why a step is being done.
6. Kept the EDA focused on the concepts in the assignment.

---

## Libraries allowed by the assignment

The script uses:

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Requests
- SQLite (`sqlite3`)

No machine-learning model is trained in this assignment.

---

## How to run

Install the libraries:

```bash
pip install pandas numpy matplotlib seaborn requests
```

Then run:

```bash
python Assignment_13_Data_Gathering_Preprocessing_EDA.py
```

For the TMDB task, add your own TMDB API key before running that section.

---

## Important for mentor discussion

I should be able to explain:

- Difference between numerical and categorical data
- Why missing values need treatment
- Mean vs median
- Mode for categorical data
- What duplicate rows mean
- Label encoding vs one-hot encoding
- Why a boxplot can help identify outliers
- What a correlation value means
- Difference between univariate and bivariate analysis
- Why EDA is performed before ML
