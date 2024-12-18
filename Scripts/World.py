import random
import pygame
from pygame import Vector2
from Entity import *


class Cell:
    def __init__(
            self,
            pos: Vector2,
    ):
        self.position: Vector2 = pos
        # Land, Water, Forest
        self.element: str = "Land"
        # Preditor, Prey
        self.entity = None
        pass


class World:
    def __init__(self, grid=Vector2(int(30), int(30)), prey_size=100, predator_size=100):
        # World variables
        # No. of cells in the world (1 cell occupied by 1 entity)
        self.GRID = grid
        self.cell_size = 25
        self.RESOLUTION = Vector2(
            self.GRID.x * self.cell_size, self.GRID.y * self.cell_size
        )
        self.map = [
            [Cell(Vector2(int(x), int(y))) for x in range(int(self.GRID.x))]
            for y in range(int(self.GRID.y))
        ]

        # Entities
        self.prey_size = prey_size
        self.prey_set = set()
        self.predator_set = set()
        self.predator_size = predator_size
        # Amt of sunlight in the world
        self.luminance = 100.0

        # pygame variables
        # self.screen = pygame.display.set_mode(self.RESOLUTION)

    def populate(self):
        # Populate with Prey
        for _ in range(self.prey_size):
            x = random.randint(0, int(self.GRID.x) - 1)
            y = random.randint(0, int(self.GRID.y) - 1)
            self.prey_set.add((x, y))
            self.map[x][y].entity = Prey(Vector2(int(x), int(y)), self)

        # Population with Predator
        for _ in range(self.predator_size):
            x = random.randint(0, int(self.GRID.x) - 1)
            y = random.randint(0, int(self.GRID.y) - 1)
            self.predator_set.add((x, y))
            self.map[x][y].entity = Predator(Vector2(int(x), int(y)), self)

        pass


test = World()
test.populate()
a = test.prey_set.pop()
b = test.map[a[0]][a[1]].entity.pos
print(b)
b = test.map[a[0]][a[1]].entity.move_and_collide(Vector2(1, 0), 1)
c = test.map[a[0] + 1][a[1]].entity
print((c))
