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
    def __init__(self, grid=Vector2(30, 30)):
        # No. of cells in the world (1 cell occupied by 1 entity)
        self.GRID = grid
        self.cell_size = 25
        self.RESOLUTION = Vector2(
            self.GRID.x * self.cell_size, self.GRID.y * self.cell_size
        )
        self.map = [
            [Cell(Vector2(x, y)) for x in range(int(self.GRID.x))]
            for y in range(int(self.GRID.y))
        ]
        # Amt of sunlight in the world
        self.luminance = 100.0

        # pygame variables
        self.screen = pygame.display.set_mode(self.RESOLUTION)
