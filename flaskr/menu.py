from z3 import *

class Dish:
    def __init__(self, name, price) -> None:
        self.name = name
        self.price = price
        self.picked = Bool(name)

    def smt_price(self):
        return If(self.picked, self.price, 0)

    def smt_is_picked(self):
        return If(self.picked, 1, 0)

class Menu:
    def __init__(self) -> None:
        self.dishes = []

    def __init__(self, dishes) -> None:
        self.dishes = dishes

    def add_dish(self, dish: Dish) -> None:
        self.dishes.append(dish)
    
    def smt_price_constraints(self, max_price, min_price = 0):
        total_price = Sum([If(d.picked, d.price, 0) for d in self.dishes])
        return [total_price <= max_price, total_price >= min_price]

    def smt_count(self, max_count, min_count = 1):
        count = Sum([If(d.picked, 1, 0) for d in self.dishes])
        return [count >= min_count, count <= max_count]


dishes = [Dish('chicken', 10), Dish('pork', 20), Dish('fish', 30), Dish('tofu', 10), Dish('bok choy', 10),
    Dish('fried rice', 5), Dish('rice', 2)]

menu = Menu(dishes=dishes)

s = Solver()
s.add(menu.smt_price_constraints(max_price=50, min_price=10))
s.add(menu.smt_count(max_count=10, min_count=5))

print(s.check())
print(s.model())