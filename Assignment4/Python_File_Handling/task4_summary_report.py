# Task 4: Generate Summary Report

with open("sales_data.txt", "r") as file:
    sales = []

    for line in file:
        sales.append(int(line.strip()))

total_sales = sum(sales)
highest_sale = max(sales)
lowest_sale = min(sales)
average_sale = total_sales / len(sales)

print("Total Sales:", total_sales)
print("Highest Sale:", highest_sale)
print("Lowest Sale:", lowest_sale)
print("Average Sale:", average_sale)
