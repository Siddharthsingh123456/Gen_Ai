# Task 3

gst = lambda price: price + (0.18 * price)

print(gst(100))

gst_discount = lambda price, discount: (price + 0.18 * price) - ((price + 0.18 * price) * discount / 100)

print(gst_discount(100, 10))
