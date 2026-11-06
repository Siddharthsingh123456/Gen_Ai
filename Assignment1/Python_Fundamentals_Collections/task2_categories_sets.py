# Task 2: Categories (Sets)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam"]

categories_list = ["Electronics", "Accessories", "Accessories", "Electronics", "Audio", "Electronics"]
categories_set = set(categories_list)

print("Unique Categories:", categories_set)

categories_set.add("Audio")
print("After Adding Duplicate:", categories_set)

print("Is 'Electronics' present?", "Electronics" in categories_set)

print("Total Unique Categories:", len(categories_set))
