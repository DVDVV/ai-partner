class Dog:
    """一次模拟小狗的简单尝试"""

    def __init__(self,name,age):
        self.name = name
        self.age = age
        print(f"{self.name} is created.")

    def sit(self):
        print(f"{self.name} is now sitting.")

    def roll_over(self):
        print(f"{self.name} is now rolling over.")

a = Dog("dog1",18)
a.sit()
print(a.age,"age！")

class DogSon(Dog):
    def __init__(self,name,age):
        super().__init__(name,age)
        self.battery ="electric"
        print(f"{self.battery} is now battery.")

    def sit(self):
        print(f"{self.name} is now electric sitting.")
b = DogSon("dog2",18)
b.sit()
