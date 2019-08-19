class Dog():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def p_name(self):
        return self.name

    def p_age(self):
        print(self.age)


my_dog = Dog('haha', 2)
print(my_dog.name)
print(my_dog.p_name())
my_dog.p_age()
