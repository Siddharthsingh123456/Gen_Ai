# Task 1

def apply_discount(price, discount_percent=5):
    if discount_percent > 60:
        discount_percent = 60
    return price - (price * discount_percent / 100)

print(apply_discount(1000, 10))
print(apply_discount(500))
