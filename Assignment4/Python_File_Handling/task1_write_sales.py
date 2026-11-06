# Task 1: Write Sales Record

sales = [100, 450, 900, 1500, 3000]

file = open("sales_data.txt", "w")

for sale in sales:
    file.write(str(sale) + "\n")

file.close()

file = open("sales_data.txt", "r")
print(file.read())
file.close()
