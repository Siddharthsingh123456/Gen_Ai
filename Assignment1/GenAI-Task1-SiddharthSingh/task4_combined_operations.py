# Task 4: Combined Operations

catalog = [
    ("Laptop", 55000, "Electronics"),
    ("Mouse", 500, "Accessories"),
    ("Keyboard", 1200, "Accessories"),
    ("Monitor", 10000, "Electronics"),
    ("Headphones", 2500, "Audio"),
    ("Webcam", 1800, "Electronics")
]

category_to_products = {}

for product, price, category in catalog:
    if category not in category_to_products:
        category_to_products[category] = []
    category_to_products[category].append(product)

print("Category Mapping:")
for category, products in category_to_products.items():
    print(category, ":", products)

max_category = max(category_to_products, key=lambda c: len(category_to_products[c]))

print("Category with Maximum Products:", max_category)
print("Products:", category_to_products[max_category])
