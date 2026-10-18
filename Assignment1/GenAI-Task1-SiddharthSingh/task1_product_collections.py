# Task 1: Product Collections (Lists & Tuples)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam"]

sample_product = ("Laptop", 55000, "Electronics")

print("2nd Product:", products[1])
print("Last Product:", products[-1])

products.append("Printer")
products.append("Speaker")

print("Updated Products List:", products)

temp = list(sample_product)
temp[1] = 60000
sample_product = tuple(temp)

print("Updated Tuple:", sample_product)
