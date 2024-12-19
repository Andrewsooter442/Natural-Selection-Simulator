import random
import pygame
from abc import ABC, abstractmethod
from pygame import Vector2


class Entity(ABC):
    def __init__(self, pos: Vector2, world):
        self.Max_Energy = 100
        self.world = world
        self.Energy = 100
        self.movement_cost = 0
        self.pos: Vector2 = pos
        self.top_speed = 20.0
        self.vision = 3

    # Check of other species in the neighbour
    @abstractmethod
    def get_vision(self) -> []: ...

    # Get the input for the neural network
    def network_inputs(self):
        to_ret = []
        entity_info = [
            self.Energy,
            self.pos.x,
            self.pos.y,
        ]
        self.world = [self.world.luminance]
        entity_vision = self.get_vision()
        to_ret.extend(entity_info)
        to_ret.extend(self.world)
        to_ret.extend(entity_vision)
        return to_ret

    # Implements movement and collision and feeding
    @abstractmethod
    def move_and_collide(self, direction, speed): ...


class Predator(Entity):
    def __init__(self, pos: Vector2, world):
        super().__init__(pos, world)
        self.speed = 1
        self.type = "Predator"
        self.eat_gain = 50
        self.exists = 1.5

    def get_vision(self):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                pos = (self.pos.x, self.pos.y - 1)
                if pos in self.world.prey_set:
                    # Certainty of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                pos = (self.pos.x, self.pos.y + 1)
                if pos in self.world.prey_set:
                    # Certainty of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                pos = (self.pos.x + 1, self.pos.y)
                if pos in self.world.prey_set:
                    # Certainty of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                pos = (self.pos.x - 1, self.pos.y)
                if pos in self.world.prey_set:
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret

    def move_and_collide(self, direction: Vector2, speed):
        # Eat prey
        if (self.pos.x, self.pos.y) in self.world.prey_set:
            del self.world.prey_set[(self.pos.x, self.pos.y)]
            self.Energy += self.eat_gain
        # Move
        pos = self.pos + direction * speed
        if (
                (pos.x, pos.y) not in self.world.predator_set
                and pos[0] < self.world.GRID.x
                and pos[1] < self.world.GRID.y
        ):
            del self.world.predator_set[(self.pos.x, self.pos.y)]
            self.pos = pos
            self.world.predator_set[(self.pos.x, self.pos.y)] = self
            self.Energy -= self.movement_cost


class Prey(Entity):
    def __init__(self, pos: Vector2, world):
        super().__init__(pos, world)
        self.speed = 1
        self.type = "Prey"
        self.exists = 1

    def get_vision(self):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                pos = (self.pos.x, self.pos.y - 1)
                if pos in self.world.predator_set:
                    # Certainty of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                pos = (self.pos.x, self.pos.y + 1)
                if pos in self.world.predator_set:
                    # Certainty of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                pos = (self.pos.x + 1, self.pos.y)
                if pos in self.world.predator_set:
                    # Certainty of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                pos = (self.pos.x - 1, self.pos.y)
                if pos in self.world.predator_set:
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret

    def move_and_collide(self, direction: Vector2, speed):
        pos = self.pos + direction * speed
        if (
                (pos.x, pos.y) not in self.world.prey_set
                and pos[0] < self.world.GRID.x
                and pos[1] < self.world.GRID.y
        ):
            del self.world.prey_set[(self.pos.x, self.pos.y)]
            self.pos = pos
            self.world.prey_set[(self.pos.x, self.pos.y)] = self
