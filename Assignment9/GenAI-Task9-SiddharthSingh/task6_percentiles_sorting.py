import numpy as np

marks = np.array([78, 85, 90, 66, 72, 88, 95, 60])

print("Sorted:", np.sort(marks))
print("25th Percentile:", np.percentile(marks, 25))
print("50th Percentile:", np.percentile(marks, 50))
print("75th Percentile:", np.percentile(marks, 75))

average = np.mean(marks)
print("Above Average Count:", np.sum(marks > average))
