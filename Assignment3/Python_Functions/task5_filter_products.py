# Task 5

prices = [100, 250, 400, 1200, 50, 2000, 850]

greater_than_500 = list(filter(lambda x: x > 500, prices))
less_equal_500 = list(filter(lambda x: x <= 500, prices))

print("Greater Than 500:", greater_than_500)
print("Less Than Or Equal To 500:", less_equal_500)
