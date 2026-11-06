# Task 3: Append New Sales

file = open("sales_data.txt", "a")
file.write("5000\n")
file.write("2500\n")
file.write("1700\n")
file.close()

file = open("sales_data.txt", "r")
print(file.read())
file.close()
