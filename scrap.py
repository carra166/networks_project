class Parent:
    def __init__(self, name):
        self.name = name
        print(f"Parent initialized with name: {self.name}")
        self.status = True

    def greet(self):
        print(f"Hello, I am {self.name}, a parent.")

    def goofy_greet(self):
        print(f"Hello, I am {self.name}, a pee pee poo poo.")

    def set_offline(self):
        self.status = False

    def get_status(self):
        return self.status


class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Call the parent class's constructor
        self.age = age
        print(f"Child initialized with age: {self.age}")

    def greet(self):
        print(f"Hello, I am {self.name}, a child, and I am {self.age} years old.")


class Friend(Child):
    def __init__(self, name, age, rank):
        super().__init__(name, age)  # Call the parent class's constructor
        self.rank = rank
        print(f"Friend initialized with rank: {self.rank}")

# Example of a parent instance
parent_instance = Parent("Alice")
parent_instance.greet()

# Later, we "convert" the parent instance to a child instance
child_instance = Child(parent_instance.name, 10)  # Create a new child instance
parent_instance = child_instance  # Switch the parent instance to the child instance

parent_instance.greet()  # Now the parent instance is actually a child instance
parent_instance.goofy_greet()
parent_instance.set_offline()
print(parent_instance.get_status())