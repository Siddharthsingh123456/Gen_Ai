# Assignment 11 - Matplotlib

## Dataset attribution

**Dataset:** SuperStore Dataset

**Kaggle source:** https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

**Kaggle dataset author:** Vivek Chowdhury

The dataset contains 9,994 sales records and fields such as Order Date,
Region, Category, Sales, Quantity, Discount and Profit.

The CSV included in this folder is the Superstore dataset used for the
assignment. The Kaggle page is included above for proper attribution.

## Why this dataset was selected

The assignment asks for a sales dataset and a monthly sales trend. This
dataset has an `Order Date` column and a `Sales` column. It also contains
different years (2015-2018), so Task 4 can compare sales between years.

## Tasks completed

1. Line plot - monthly sales trend
2. Scatter plot - Quantity vs Sales
3. Vertical and horizontal bar plots - Sales by Region
4. Multiple bar plot - monthly sales comparison for 2015-2018
5. Stacked bar chart - Sales by Region and Category
6. Histogram - Sales distribution
7. Pie chart - Sales share by Category

## Code style

The code intentionally uses beginner-level Python:

- `csv.DictReader`
- lists
- simple dictionaries
- `for` loops
- `if/else`
- basic string `split()`
- `matplotlib.pyplot`

It does not use:

- Seaborn
- Pandas plotting
- `defaultdict`
- advanced data-processing libraries
- professional plotting styles

## How to run

Install Matplotlib:

```bash
pip install matplotlib
```

Keep these two files in the same folder:

- `Assignment_11_Matplotlib.py`
- `Superstore.csv`

Run:

```bash
python Assignment_11_Matplotlib.py
```

The seven plots will appear one after another.

## What to understand before submission

Be able to explain:

- How `csv.DictReader` reads each row
- Why `float()` is used for Sales and Quantity
- How the month is taken from `Order Date`
- How the dictionaries store total sales
- Why `plt.plot()` is used for a trend
- Why `plt.scatter()` is used for two numerical columns
- Difference between `plt.bar()` and `plt.barh()`
- How `bottom` creates a stacked bar
- What bins mean in a histogram
- Why percentages are displayed in the pie chart

## Learning note

This version is deliberately simple rather than optimized. The goal is to
make each task easy to read and explain during a mentor discussion.
