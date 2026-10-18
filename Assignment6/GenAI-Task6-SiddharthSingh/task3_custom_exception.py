def check_age(age):
    if age < 1 or age > 120:
        raise ValueError("Age must be between 1 and 120")

try:
    age = int(input("Enter age: "))
    check_age(age)
    print("Valid Age")
except ValueError as e:
    print(e)
