
class Laptop:
    def get_info(self):
        print("Laptop Object")

class Mobile:
    def get_info(self):
        print("Mobile Object")

items = [Laptop(), Mobile()]

for item in items:
    item.get_info()
