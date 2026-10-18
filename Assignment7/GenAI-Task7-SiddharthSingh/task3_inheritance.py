
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_info(self):
        print(self.name, self.price)

class ElectronicProduct(Product):
    def __init__(self, name, price, warranty_years):
        super().__init__(name, price)
        self.warranty_years = warranty_years

    def get_info(self):
        print(self.name, self.price, self.warranty_years)

e = ElectronicProduct("Laptop", 50000, 2)
e.get_info()
