# Task 3: User Menu (while loop + break/continue)

orders = []

while True:
    print("\n1 - Add order amount")
    print("2 - Show orders and totals")
    print("q - Quit")

    choice = input("Choose: ")

    if choice == "1":
        amount = float(input("Enter order amount: "))
        orders.append(amount)

    elif choice == "2":
        total = 0

        for order_amount in orders:
            if order_amount >= 2000:
                discount = 15
            elif order_amount >= 1500:
                discount = 10
            elif order_amount >= 1000:
                discount = 7
            else:
                discount = 0

            final_amount = order_amount - (order_amount * discount / 100)
            total += final_amount

            print("Order:", order_amount, "Final:", final_amount)

        print("Total After Discounts:", total)

    elif choice == "q":
        print("Exiting Program")
        break

    else:
        print("Invalid choice")
        continue
