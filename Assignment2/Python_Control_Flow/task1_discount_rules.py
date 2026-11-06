# Task 1: Discount Rules (if / elif / else)

user_input = input("Enter order amount: ")

try:
    order_amount = float(user_input)

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

    print("Order Amount:", order_amount)
    print("Discount:", str(discount) + "%")
    print("Final Amount:", final_amount)

except ValueError:
    print("Invalid input. Please enter a number.")
