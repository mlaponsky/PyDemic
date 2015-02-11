import constants

class City:
    cubes = {}

    def __init__(self, name, color):
        self.name = name
        self.color = color
        for i in range(0,4):
            self.cubes[i] = 0

    def add_cubes(self, color, number):
        self.cubes[color] += number

    def remove_cubes(self, color, number):
        self.cubes[color] -= number

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_cubes(self, color):
        return cubes[color]
