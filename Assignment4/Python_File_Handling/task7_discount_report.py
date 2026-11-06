# Task 7: Mini Project

prices = {
    "Mouse": 500,
    "Keyboard": 800,
    "Monitor": 7000,
    "Pendrive": 400,
    "Camera": 5000
}

discount = float(input("Enter discount percentage: "))

file = open("discount_report.txt", "w")

total = 0
count = 0

file.write("Product | Original Price | Discounted Price\n")

for product in prices:
    original = prices[product]
    discounted = original - (original * discount / 100)

    total += discounted
    count += 1

    file.write(product + " | " + str(original) + " | " + str(discounted) + "\n")

average = total / count

file.write("\nTotal Items: " + str(count))
file.write("\nAverage Discounted Price: " + str(average))

file.close()

print("discount_report.txt created successfully.")
