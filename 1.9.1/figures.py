from Classes import Rectangle, Square, Circle

rect_1 = Rectangle(3, 4)
rect_2 = Rectangle(12, 5)

print(rect_1.get_area())
print(rect_2.get_area())
print()

sq_1=Square(5)
sq_2=Square(10)

print(sq_1.get_area_square())
print(sq_2.get_area_square())
print()

ci_1=Circle(6)
ci_2=Circle(9)

print(ci_1.get_area_circle())
print(ci_2.get_area_circle())
print()

