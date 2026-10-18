prices = [120, 350, 'abc', 500, -200, 800]

total = 0

for item in prices:
    try:
        if not isinstance(item, (int, float)):
            raise TypeError("Value is not a number")
        if item < 0:
            raise ValueError("Negative price not allowed")
        total += item
    except TypeError as e:
        print(e)
    except ValueError as e:
        print(e)

print("Final Total:", total)
