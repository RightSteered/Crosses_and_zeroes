class Client:

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance


client1 = Client("Иван Петров", 50)

print(f"Клиент : {client1.name}")
print(f"Баланс : {client1.balance} руб")


class Guests(Client):  # Задание 1.10.4

    def __init__(self, name, balance, city, status):
        self.name = name
        self.balance = balance
        self.city = city
        self.status = status


client1 = Guests("Иван Петров", 50, "Москва", "Наставник")

print(f"Клиент {client1.name}, {client1.balance} руб, {client1.city}, {client1.status}")
