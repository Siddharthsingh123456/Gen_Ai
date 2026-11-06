# Task 5: Loop Control with Conditions (break & continue)

daily_sales = [200, 150, 0, 400, 50, -1, 300]

total_sales = 0

for sale in daily_sales:

    if sale == -1:
        print("Corrupted data found. Stopping processing.")
        break

    if sale == 0:
        print("No sales today. Skipping.")
        continue

    total_sales += sale
    print("Added:", sale, "Running Total:", total_sales)

print("Final Total Sales:", total_sales)
