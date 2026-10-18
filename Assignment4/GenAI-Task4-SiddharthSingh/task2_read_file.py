# Task 2: Read File in Different Ways

file = open("sales_data.txt", "r")

print("Read Entire File:")
print(file.read())
file.close()

file = open("sales_data.txt", "r")
print("First Line:")
print(file.readline())
file.close()

file = open("sales_data.txt", "r")
sales = []

for line in file.readlines():
    sales.append(int(line.strip()))

print("Sales List:", sales)
file.close()
