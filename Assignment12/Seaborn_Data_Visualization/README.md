# Assignment 12 - Seaborn
## Relational, Distribution, Categorical & Multi-Plots

### Student
Siddharth Singh

---

## 1. Dataset Source

**Dataset name:** Students Performance in Exams

**Kaggle source:**  
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

The dataset contains 1,000 student records and includes categorical columns
such as gender, race/ethnicity, parental level of education, lunch and test
preparation course. It also has numerical columns for math, reading and
writing scores.

This is the Kaggle dataset used for the assignment, rather than a dataset
described only as a "supplied dataset".

---

## 2. Why I selected this dataset

I used this dataset because it has both types of columns needed for the
assignment:

- Numerical: math score, reading score, writing score
- Categorical: gender, lunch, test preparation course, etc.

This makes it possible to practice relational, distribution, categorical,
regression and multi-plot Seaborn graphs using the same dataset.

---

## 3. Libraries

Only the libraries allowed in the assignment are used:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

No Plotly or other visualization library is used.

---

## 4. Tasks completed

### Task 1 - Relational Plot
- `relplot()` with two numerical columns
- Scatter style
- Gender used as a categorical variable

### Task 2 - Line Plot as Scatter & Facet
- `lineplot()`
- Same relationship shown using scatter points
- `col="gender"` used for faceting

### Task 3 - Distribution Plots
- Histogram
- KDE plot
- Rug plot
- Histogram + KDE

### Task 4 - Bivariate Distribution
- Bivariate histogram
- Bivariate KDE

### Task 5 - Matrix Plots
- `pairplot()`
- Correlation heatmap

### Task 6 - Categorical Plots
- Bar plot
- Box plot
- Violin plot
- Count plot

### Task 7 - Regression Plots
- `regplot()`
- `lmplot()` with gender

### Task 8 - Multi-Plots
- `FacetGrid`
- `relplot()`
- `catplot()`
- `displot()`

---

## 5. Revision / Learning Record

This section records the changes made after mentor feedback. It is not
intended to pretend that mistakes happened if they did not.

### Revision 1 - Dataset source

The earlier submission did not clearly show a Kaggle source. I changed this
version so the README contains the Kaggle dataset name and direct source link.

### Revision 2 - Dataset description

The earlier README referred to a "supplied dataset". This version clearly
states that `StudentsPerformance.csv` is the Students Performance in Exams
dataset and gives its Kaggle source.

### Revision 3 - Simpler code

The previous code had a very uniform presentation style. I reduced the
extra formatting and kept each Seaborn example close to the corresponding
task so that the purpose of each plot is easier to follow.

### Revision 4 - Understanding the plots

While revising, I focused on understanding what each argument does:

- `x` and `y` select the variables
- `hue` separates observations by a category
- `col` creates separate panels
- `kind` changes the type of figure-level plot
- `kde=True` adds a KDE curve to a histogram
- `annot=True` writes correlation values in the heatmap

### What I should be able to explain

Before submitting, I should be able to explain:

1. Difference between `relplot()` and `scatterplot()`
2. What a KDE plot represents
3. Why a histogram uses bins
4. Difference between box plot and violin plot
5. What a heatmap correlation value means
6. What the regression line shows
7. What `hue` does
8. What a FacetGrid is
9. Difference between `catplot()` and `catplot(..., kind="box")`
10. Difference between axes-level and figure-level Seaborn functions

---

## 6. How to run

Keep these files in the same folder:

- `Assignment_12_Seaborn.py`
- `StudentsPerformance.csv`
- `README.md`

Install the required packages:

```bash
pip install pandas matplotlib seaborn
```

Run:

```bash
python Assignment_12_Seaborn.py
```

The plots will appear one by one.

---

## 7. Submission note

The code is intentionally kept at a beginner/intermediate level. It is
better to understand and explain every plot than to use complicated code
that is difficult to explain during a mentor discussion.
