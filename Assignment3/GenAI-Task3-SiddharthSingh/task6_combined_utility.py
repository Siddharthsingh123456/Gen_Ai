# Task 6

def process_prices(prices):
    discounted_prices = list(map(lambda x: x - (x * 10 / 100), prices))
    filtered_prices = list(filter(lambda x: x > 300, discounted_prices))

    return discounted_prices, filtered_prices

print(process_prices([100, 500, 900, 50, 750]))
