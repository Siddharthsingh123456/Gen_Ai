# Assignment 15
# Basic ML algorithms and model evaluation
#
# Dataset:
# Students Performance in Exams
# Kaggle:
# https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
#
# I wrote the steps separately first so I can see what each model is doing.

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# ------------------------------------------------------------
# 1. Load the data
# ------------------------------------------------------------

df = pd.read_csv("StudentsPerformance.csv")

print("Dataset shape:", df.shape)
print(df.head())


# ------------------------------------------------------------
# 2. Make a simple average score
# ------------------------------------------------------------

df["average_score"] = (
    df["math score"]
    + df["reading score"]
    + df["writing score"]
) / 3

print("\nAverage score:")
print(df[["math score", "reading score",
          "writing score", "average_score"]].head())


# ------------------------------------------------------------
# 3. Linear Regression
# Predict writing score
# ------------------------------------------------------------

X_reg = df[["math score", "reading score"]]
y_reg = df["writing score"]

X_train, X_test, y_train, y_test = train_test_split(
    X_reg,
    y_reg,
    test_size=0.2,
    random_state=42
)

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

predicted = linear_model.predict(X_test)

mae = mean_absolute_error(y_test, predicted)
mse = mean_squared_error(y_test, predicted)
rmse = mse ** 0.5

print("\nLinear Regression")
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)


# Actual vs predicted
plt.scatter(y_test, predicted)
plt.xlabel("Actual Writing Score")
plt.ylabel("Predicted Writing Score")
plt.title("Actual vs Predicted Writing Score")
plt.show()


# ------------------------------------------------------------
# 4. Make a classification target
# ------------------------------------------------------------

# The original file does not have a ready-made pass/fail column.
# I made a simple class from average score.
#
# 0 = below 50
# 1 = 50 or above

df["performance_class"] = 0

df.loc[
    df["average_score"] >= 50,
    "performance_class"
] = 1

print("\nClass counts:")
print(df["performance_class"].value_counts())


# ------------------------------------------------------------
# 5. Prepare classification data
# ------------------------------------------------------------

X = df[[
    "math score",
    "reading score",
    "writing score"
]]

y = df["performance_class"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ------------------------------------------------------------
# 6. Logistic Regression
# ------------------------------------------------------------

log_model = LogisticRegression(max_iter=1000)

log_model.fit(X_train, y_train)

log_pred = log_model.predict(X_test)

print("\nLogistic Regression Accuracy:")
print(accuracy_score(y_test, log_pred))


# ------------------------------------------------------------
# 7. Gaussian Naive Bayes
# ------------------------------------------------------------

nb_model = GaussianNB()

nb_model.fit(X_train, y_train)

nb_pred = nb_model.predict(X_test)

print("\nNaive Bayes Accuracy:")
print(accuracy_score(y_test, nb_pred))


# ------------------------------------------------------------
# 8. KNN
# ------------------------------------------------------------

for k in [3, 5, 7]:

    knn = KNeighborsClassifier(n_neighbors=k)

    knn.fit(X_train, y_train)

    knn_pred = knn.predict(X_test)

    score = accuracy_score(y_test, knn_pred)

    print("K =", k, "Accuracy =", score)


# I checked the three values and selected the best one.
best_k = 3

knn = KNeighborsClassifier(n_neighbors=best_k)

knn.fit(X_train, y_train)

knn_pred = knn.predict(X_test)

print("\nSelected K:", best_k)
print("KNN Accuracy:", accuracy_score(y_test, knn_pred))


# ------------------------------------------------------------
# 9. Evaluation metrics
# ------------------------------------------------------------

print("\nClassification Metrics")

print("Accuracy:",
      accuracy_score(y_test, knn_pred))

print("Precision:",
      precision_score(y_test, knn_pred, zero_division=0))

print("Recall:",
      recall_score(y_test, knn_pred, zero_division=0))

print("F1:",
      f1_score(y_test, knn_pred, zero_division=0))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        knn_pred,
        zero_division=0
    )
)


# ------------------------------------------------------------
# 10. Confusion matrix
# ------------------------------------------------------------

cm = confusion_matrix(y_test, knn_pred)

print("\nConfusion Matrix:")
print(cm)

plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()
plt.show()


# ------------------------------------------------------------
# 11. Underfitting and overfitting
# ------------------------------------------------------------

# I compare a small K and a larger K.
# This is only a simple demonstration.

small_knn = KNeighborsClassifier(n_neighbors=1)
large_knn = KNeighborsClassifier(n_neighbors=25)

small_knn.fit(X_train, y_train)
large_knn.fit(X_train, y_train)

small_train = small_knn.predict(X_train)
small_test = small_knn.predict(X_test)

large_train = large_knn.predict(X_train)
large_test = large_knn.predict(X_test)

print("\nK = 1")
print("Train accuracy:",
      accuracy_score(y_train, small_train))
print("Test accuracy:",
      accuracy_score(y_test, small_test))

print("\nK = 25")
print("Train accuracy:",
      accuracy_score(y_train, large_train))
print("Test accuracy:",
      accuracy_score(y_test, large_test))


# ------------------------------------------------------------
# 12. Bias and variance
# ------------------------------------------------------------

print("\nBias and Variance")

print("High bias usually means the model is too simple.")
print("High variance usually means the model changes a lot with the data.")
print("Underfitting is commonly related to high bias.")
print("Overfitting is commonly related to high variance.")

print("\nAssignment 15 completed.")
