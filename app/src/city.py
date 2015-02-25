import constants

class City:
    def __init__(self, name, population, primary, secondary, tertiary):
        self.name = name
        self.color = primary
        self.secondary = secondary
        self.tertiary = tertiary
        self.population = population

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
