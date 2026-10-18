# Task 3: Product Pricing (Dictionaries)

price_dict = {
    "Laptop": 55000,
    "Mouse": 500,
    "Keyboard": 1200,
    "Monitor": 10000,
    "Headphones": 2500,
    "Webcam": 1800
}

price_dict["Printer"] = 7000
price_dict["Mouse"] = 600

remove_product = "Speaker"

if remove_product in price_dict:
    del price_dict[remove_product]
else:
    print(remove_product, "not found")

average_price = sum(price_dict.values()) / len(price_dict)

print("Average Price:", average_price)

max_product = max(price_dict, key=price_dict.get)
min_product = min(price_dict, key=price_dict.get)

print("Maximum Price Product:", max_product, price_dict[max_product])
print("Minimum Price Product:", min_product, price_dict[min_product])
