# python에서의 상속

class Human:
    def __init__(self, name):
        # print("Human initialized")
        self.name = name

    def say_hello(self):
        print(f"hello my name is {self.name}")

class Player(Human):
    def __init__(self, name, xp):
        super().__init__(name)
        self.xp = xp

class Fan(Human):
    def __init__(self, name, fav_team):
        super().__init__(name)
        self.fav_team = fav_team


# nico_player = Player("nico_p", 10)
# nico_player.say_hello()
# nico_fan = Fan("nico_fan", "dontknow")
# nico_fan.say_hello()

nico_p = Player("nico", 10)

nico = Fan("nico", "blue")
nico.say_hello()

# ==========================================================================================

class Dog:
    def woof(self):
        print("woof woof")

class Beagle(Dog):
    # def jump(self):
    #     print("jump")
    def woof(self):
        super().woof() # __init__()을 사용할 때 뿐만 아니라 부모 클래스를 사용하고 싶을 때 super 사용.
        print("super woof")

beagle = Beagle()
beagle.woof()

# ==========================================================================================
class Dog2:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        print(super().__str__())
        return f"Dog: {self.name}"
    def __getattribute__(self, name):
        print(f"they want to get {name}")
        return "@@@"

rang = Dog2("rang")
print(rang)
paul = Dog2("paul")
print(paul)

print(dir(rang))
print(rang.name)