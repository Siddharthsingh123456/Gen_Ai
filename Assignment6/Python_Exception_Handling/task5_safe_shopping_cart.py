cart = []
total_bill = 0

while True:
    value = input("Enter price (q to quit): ")

    if value.lower() == "q":
        break

    try:
        price = float(value)

        if price < 0:
            raise ValueError("Price cannot be negative")

        cart.append(price)
        total_bill += price

    except ValueError as e:
        print(e)

print("Total Items:", len(cart))
print("Total Bill:", total_bill)
