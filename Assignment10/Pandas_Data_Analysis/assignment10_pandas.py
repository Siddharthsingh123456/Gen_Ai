
import pandas as pd

print("TASK 1: Pandas Series")
marks = pd.Series([78, 85, 90, 66, 72])

print(marks)
print("Index:", marks.index)
print("Data Type:", marks.dtype)
print("First Element:", marks.iloc[0])
print("Last Two Elements:")
print(marks.tail(2))

print("\nTASK 2: Mathematical Operations")
print("Add 5:\n", marks + 5)
print("Subtract 2:\n", marks - 2)
print("Multiply by 1.5:\n", marks * 1.5)
print("Divide by 2:\n", marks / 2)

print("\nTASK 3: Python Functions on Series")
print("Maximum:", marks.max())
print("Minimum:", marks.min())
print("Sum:", marks.sum())
print("Mean:", marks.mean())

passed = marks.apply(lambda x: x >= 70)
print("Passed Students:", passed.sum())

print("\nTASK 4: Create DataFrame")

students = pd.DataFrame({
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
})

print(students)
print(students.head(3))
print(students.tail(2))
print("Shape:", students.shape)
print("Columns:", students.columns)

print("\nTASK 5: Important DataFrame Functions")
print(students.info())
print(students.describe())
print(students.head())
print(students.tail())

print(students.sort_values(by="Marks", ascending=False))
print(students.sort_values(by="Marks"))

print("\nTASK 6: Filtering")
print(students[students["Marks"] > 75])
print(students[students["Subject"] == "Math"])

average_marks = students["Marks"].mean()
print(students[students["Marks"] > average_marks])
print(students[students["Marks"] < 70])

print("\nTASK 7: Grouping & Analysis")
grouped = students.groupby("Subject")["Marks"]
print(grouped.mean())
print(grouped.count())
print(grouped.max())

print("\nTASK 8: Pandas Plotting")
marks.plot(title="Marks")
marks.hist()

print("\nTASK 9: Sales Data Analysis")

sales = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Revenue": [1200, 1500, 900, 2000, 1800]
})

print("Total Revenue:", sales["Revenue"].sum())
print("Average Revenue:", sales["Revenue"].mean())

highest = sales.loc[sales["Revenue"].idxmax()]
print("Highest Revenue Day:")
print(highest)

avg_revenue = sales["Revenue"].mean()
print(sales[sales["Revenue"] > avg_revenue])

sales.plot(x="Day", y="Revenue")
