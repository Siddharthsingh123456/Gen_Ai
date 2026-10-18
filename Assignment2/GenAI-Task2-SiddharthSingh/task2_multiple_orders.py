# Task 2: Process Multiple Orders (for loop)

orders = [1200, 2500, 800, 1750, 3000]

total_revenue = 0
discounted_orders = 0

for order_amount in orders:

    if order_amount >= 2000:
        discount = 15
    elif order_amount >= 1500:
        discount = 10
    elif order_amount >= 1000:
        discount = 7
    else:
        discount = 0

    discount_amount = order_amount * discount / 100
    final_amount = order_amount - discount_amount

    if discount > 0:
        discounted_orders += 1

    total_revenue += final_amount

    print("Order:", order_amount,
          "Discount:", str(discount) + "%",
          "Final:", final_amount)

print("\nTotal Revenue:", total_revenue)
print("Orders With Discount:", discounted_orders)
