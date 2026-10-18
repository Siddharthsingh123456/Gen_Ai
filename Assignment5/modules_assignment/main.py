from math_utils import add
from math_utils import square

from string_utils import capitalize_words
from string_utils import reverse_string
from string_utils import word_count

from shop_package.discount import apply_discount
from shop_package.billing import calculate_total

print("Math Functions")
print(add(10, 5))
print(square(6))

print("\nString Functions")
print(capitalize_words("hello world"))
print(reverse_string("python"))
print(word_count("python modules package"))

print("\nPackage Functions")
print(apply_discount(1000, 10))
print(calculate_total([100, 200, 300]))
