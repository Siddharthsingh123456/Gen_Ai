
class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        print(self.name, self.price, self.category)

    def apply_discount(self, percent):
        return self.price - (self.price * percent / 100)

p1 = Product("Mouse", 500, "Electronics")
p2 = Product("Keyboard", 1000, "Electronics")

p1.get_info()
p2.get_info()
print(p1.apply_discount(10))
