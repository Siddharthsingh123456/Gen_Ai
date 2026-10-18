
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process_payment(self):
        pass

class CreditCardPayment(Payment):
    def process_payment(self):
        print("Credit Card Payment Processed")

class UPIPayment(Payment):
    def process_payment(self):
        print("UPI Payment Processed")

c = CreditCardPayment()
u = UPIPayment()

c.process_payment()
u.process_payment()
