# Assignment 15 - ML Algorithms, Metrics and Model Behaviour

## Dataset

**Students Performance in Exams**

Kaggle:
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

The dataset has math, reading and writing scores. It also contains
categorical student information.

---

## What I did

I kept this assignment simple and worked through the algorithms one at a
time instead of making one large machine-learning pipeline.

### Part 1 - Linear Regression

I used:

- Math score
- Reading score

to predict:

- Writing score

I calculated:

- MAE
- MSE
- RMSE

I also made an actual-vs-predicted scatter plot.

---

## Part 2 - Classification

The original dataset does not contain a ready-made pass/fail target.

So I created:

`performance_class`

The rule is:

- Average score below 50 = `0`
- Average score 50 or above = `1`

The average uses math, reading and writing scores.

---

## Models used

### Logistic Regression

Used as a basic classification model.

### Gaussian Naive Bayes

Used as another simple classification model.

### KNN

I tested:

- K = 3
- K = 5
- K = 7

Then I selected the K value after looking at the printed accuracy values.

---

## Evaluation

For the KNN model I calculated:

- Accuracy
- Precision
- Recall
- F1 score
- Classification report
- Confusion matrix

---

## Underfitting and overfitting

I compared:

- K = 1
- K = 25

The purpose was to see the difference between a model that is very flexible
and one that is more general.

A very small K can react strongly to individual training examples.

A larger K uses more neighbours and produces a smoother decision.

---

## Bias and variance

My understanding:

- High bias -> model is too simple -> can underfit.
- High variance -> model is too sensitive to the training data -> can
  overfit.

---

## Revision after mentor feedback

The previous version was too polished and had patterns that looked like
professional production code.

For this revision I intentionally kept the steps visible:

1. Load the dataset.
2. Create the average score.
3. Do Linear Regression.
4. Print MAE/MSE/RMSE.
5. Create the classification target.
6. Run Logistic Regression.
7. Run Naive Bayes.
8. Try KNN with three K values.
9. Calculate metrics.
10. Compare K = 1 and K = 25.

There are no custom classes, no large helper framework and no unnecessary
error-handling system.

### Important learning note

I have not invented fake debugging errors just to make the file look human.
The included code is a simple starting version. I should run it myself and
write down any real error, correction and observation before submission.

---

## Things I should be able to explain

1. What Linear Regression predicts.
2. Meaning of MAE.
3. Meaning of MSE.
4. Why RMSE is useful.
5. Difference between regression and classification.
6. What Logistic Regression does.
7. Basic idea of Naive Bayes.
8. How KNN chooses a class.
9. Effect of changing K.
10. Difference between precision and recall.
11. What an F1 score means.
12. How to read a confusion matrix.
13. Meaning of underfitting.
14. Meaning of overfitting.
15. Difference between bias and variance.

---

## Installation

```text
pip install pandas matplotlib scikit-learn
```

## Run

Keep these files together:

```text
Assignment_15_Core_Algorithms_Metrics_Model_Behavior.py
StudentsPerformance.csv
```

Then run:

```text
python Assignment_15_Core_Algorithms_Metrics_Model_Behavior.py
```
