"""
Single responsibility
Open / Closed
Liskov substitution
Interface segregation
Dependency inversion
"""

from abc import ABC, abstractmethod


class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        return sum(
            self.quantities[i] * self.prices[i]
            for i in range(len(self.prices))
        )


class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass


class SMSAuth(Authorizer):

    authorized = False

    def verify_code(self, code):
        print(f"Verifyng code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class NotARobot(Authorizer):
    authorized = False

    def not_a_robot(self):
        print(f"Are you a robot? Naaaa...")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authorizer: Authorizer):
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")

        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email, authorizer: Authorizer):
        self.authorizer = authorizer
        self.email = email

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")

        print("Processing paypal payment type")
        print(f"Verifying email address: {self.email}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
authorizer = NotARobot()
processor = PaypalPaymentProcessor("eltonfd@gmail.com", authorizer)
authorizer.not_a_robot()
processor.pay(order)
