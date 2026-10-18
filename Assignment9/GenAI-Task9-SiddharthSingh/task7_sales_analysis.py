import numpy as np

sales = np.array([1200, 1500, 900, 2000, 1800, 1700, 1600])

print("Total Weekly Sales:", np.sum(sales))
print("Average Daily Sales:", np.mean(sales))
print("Highest Sales Day:", np.max(sales))
print("Standard Deviation:", np.std(sales))

average = np.mean(sales)
print("Days Above Average:", sales[sales > average])
