from vehicle import Vehicle

class Car(Vehicle):

    def brag(self):
        print('Look how cool my car is!')


car1 = Car()
car1.drive()

car1.add_warning('New warning')
print(car1)

car2 = Car(200)
car2.drive()
# Cannot access __warnings from outside the class
# print(car2.__warnings)
print(car2.get_warnings())

car3 = Car(250)
car3.drive()
# Cannot access __warnings from outside the class
# print(car3.__warnings)
print(car3.get_warnings())