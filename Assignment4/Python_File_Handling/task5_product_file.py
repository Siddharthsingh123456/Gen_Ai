# Task 5: Create Product Info File

file = open("products.txt", "w")

for i in range(3):
    name = input("Enter Product Name: ")
    price = input("Enter Product Price: ")
    file.write(name + " - " + price + "\n")

file.close()

file = open("products.txt", "r")

for line in file:
    print(line.strip())

file.close()
