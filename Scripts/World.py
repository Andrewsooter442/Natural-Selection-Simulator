from Tools.scripts.summarize_stats import pretty

from Entity import *


class Cell:
    def __init__(
            self,
            pos: Vector2,
    ):
        self.position: Vector2 = pos
        # Land, Water, Forest
        self.element: str = "Land"


class World:
    def __init__(
            self, grid=Vector2(int(100), int(70)), prey_size=100, predator_size=300
    ):
        # World variables
        # No. of cells in the world (1 cell occupied by 1 entity)
        self.GRID = grid
        self.cell_size = 10
        self.RESOLUTION = Vector2(
            self.GRID.x * self.cell_size, self.GRID.y * self.cell_size
        )
        self.map = [
            [Cell(Vector2(int(x), int(y))) for x in range(int(self.GRID.x))]
            for y in range(int(self.GRID.y))
        ]

        # Entities
        self.prey_size = prey_size
        self.prey_set = {}
        self.predator_set = {}
        self.predator_size = predator_size
        # Amt of sunlight in the world
        self.luminance = 100.0

        # pygame variables

    def populate(self):
        # Populate with Prey
        for _ in range(self.prey_size):
            x = random.randint(0, int(self.GRID.x) - 2)
            y = random.randint(0, int(self.GRID.y) - 2)
            self.prey_set[(x, y)] = Prey(Vector2(int(x), int(y)), self)

        # Population with Predator
        for _ in range(self.predator_size):
            x = random.randint(0, int(self.GRID.x) - 2)
            y = random.randint(0, int(self.GRID.y) - 2)
            self.predator_set[(x, y)] = Predator(Vector2(int(x), int(y)), self)

        pass

    def test_move(self):
        keys = list(self.prey_set.keys())
        for j in keys:
            if j in self.prey_set:
                self.prey_set[j].move_and_collide(Vector2(1, 0), 1)
        key = list(self.predator_set.keys())
        for j in key:
            if j in self.predator_set:
                self.predator_set[j].move_and_collide(Vector2(1, 0), 1)


test = World()
test.populate()
