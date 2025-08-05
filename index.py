# class Person:
#     def __init__(self,*args,**kwargs):
#         print(args) 
#         print(kwargs)
# slala=Person('sala',20,name='sophonie',age=23)

class Animal:
    def __init__(self,name,sound):
        self.name = name
        self.sound = sound

class Dog(Animal):
    def __init__(self,*args,**kwargs):
        breed = kwargs.pop('breed', None)
        print(kwargs)
        super().__init__(*args, **kwargs)
        self.breed = breed
        print(kwargs)

dog = Dog(name="Rex", sound="Woof", breed="German Shepherd")
print(dog.name)
print(dog.sound)
print(dog.breed)