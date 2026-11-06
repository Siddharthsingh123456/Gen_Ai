# Assignment 12 - Seaborn
# Dataset: Students Performance in Exams
# Kaggle: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
#
# I kept this version simple and changed the code after mentor feedback.
# I am using Pandas for loading the CSV and Seaborn for the plots.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# Load the data
# -----------------------------

df = pd.read_csv("StudentsPerformance.csv")

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())


# ============================================================
# Task 1 - Relational Plot
# ============================================================

# First I tried math score and reading score because both are numbers.
sns.relplot(
    data=df,
    x="math score",
    y="reading score",
    hue="gender"
)
plt.show()


# Same relationship using scatter style.
sns.relplot(
    data=df,
    x="math score",
    y="reading score",
    hue="gender",
    kind="scatter"
)
plt.show()


# ============================================================
# Task 2 - Line Plot as Scatter & Facet
# ============================================================

# I used lineplot here to see the relationship across the rows.
sns.lineplot(
    data=df,
    x="math score",
    y="reading score"
)
plt.show()


# Now I changed the same relationship to scatter points.
# col divides the graph by the categorical column.
sns.relplot(
    data=df,
    x="math score",
    y="reading score",
    col="gender",
    kind="scatter"
)
plt.show()


# ============================================================
# Task 3 - Distribution Plots
# ============================================================

# Histogram
sns.histplot(
    data=df,
    x="math score"
)
plt.show()


# KDE
sns.kdeplot(
    data=df,
    x="math score"
)
plt.show()


# Rug plot
sns.rugplot(
    data=df,
    x="math score"
)
plt.show()


# Histogram + KDE in one graph
sns.histplot(
    data=df,
    x="math score",
    kde=True
)
plt.show()


# ============================================================
# Task 4 - Bivariate Distribution Plots
# ============================================================

# Bivariate histogram
sns.histplot(
    data=df,
    x="math score",
    y="reading score"
)
plt.show()


# Bivariate KDE
sns.kdeplot(
    data=df,
    x="math score",
    y="reading score"
)
plt.show()


# ============================================================
# Task 5 - Matrix Plots
# ============================================================

# Pair plot
sns.pairplot(
    df[
        [
            "math score",
            "reading score",
            "writing score"
        ]
    ]
)
plt.show()


# Correlation heatmap
correlation = df[
    [
        "math score",
        "reading score",
        "writing score"
    ]
].corr()

sns.heatmap(
    correlation,
    annot=True
)
plt.show()


# ============================================================
# Task 6 - Categorical Plots
# ============================================================

# Bar plot
sns.barplot(
    data=df,
    x="gender",
    y="math score"
)
plt.show()


# Box plot
sns.boxplot(
    data=df,
    x="gender",
    y="math score"
)
plt.show()


# Violin plot
sns.violinplot(
    data=df,
    x="gender",
    y="math score"
)
plt.show()


# Count plot
sns.countplot(
    data=df,
    x="gender"
)
plt.show()


# ============================================================
# Task 7 - Regression Plots
# ============================================================

# Regression plot
sns.regplot(
    data=df,
    x="math score",
    y="reading score"
)
plt.show()


# Regression plot with hue
sns.lmplot(
    data=df,
    x="math score",
    y="reading score",
    hue="gender"
)
plt.show()


# ============================================================
# Task 8 - Multi-Plots and Figure-Level Plots
# ============================================================

# FacetGrid
g = sns.FacetGrid(
    df,
    col="gender"
)

g.map_dataframe(
    sns.scatterplot,
    x="math score",
    y="reading score"
)

plt.show()


# relplot
sns.relplot(
    data=df,
    x="math score",
    y="writing score",
    col="gender",
    kind="scatter"
)
plt.show()


# catplot
sns.catplot(
    data=df,
    x="gender",
    y="math score",
    kind="box"
)
plt.show()


# displot
sns.displot(
    data=df,
    x="math score",
    col="gender",
    kde=True
)
plt.show()


print("Assignment 12 completed.")
