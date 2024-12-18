import random
import pygame
from abc import ABC, abstractmethod
from pygame import Vector2


class Entity:
    def __init__(self, pos: Vector2, world):
        self.world = world
        self.Energy = 100.0
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
        self.eat_gain = 20

    def get_vision(self):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                if self.world.map[int(self.pos.x)][int(self.pos.y) - i].entity is None:
                    continue
                elif self.world.map[int(self.pos.x)][int(self.pos.y) - i].entity == "Prey":
                    # Certainty of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                if self.world.map[int(self.pos.x)][int(self.pos.y) + i].entity is None:
                    continue
                elif self.world.map[int(self.pos.x)][int(self.pos.y) + i].entity == "Prey":

                    # Certainty of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                if self.world.map[self.pos.x + i][self.pos.y].entity is None:
                    continue
                elif self.world.map[int(self.pos.x + i)][int(self.pos.y)].entity == "Prey":
                    # Certainty of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                if self.world.map[int(self.pos.x - i)][int(self.pos.y)].entity is None:
                    continue
                elif self.world.map[int(self.pos.x - i)][int(self.pos.y)].entity == "Prey":
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret

    def move_and_collide(self, direction: Vector2, speed):
        # Check if cought a pery
        if (
                self.world.map[int(self.pos.x)][int(self.pos.y)].entity is not None
                and self.world.map[int(self.pos.x)][int(self.pos.y)].entity.type == "Prey"
        ):
            self.Energy += self.eat_gain
            self.world.map[int(self.pos.x)][int(self.pos.y)].entity = None
        self.pos += direction * speed
        self.world.map[int(self.pos.x)][int(self.pos.y)].entity = self.type
        pass


class Prey(Entity):
    def __init__(self, pos: Vector2, world):
        super().__init__(pos, world)
        self.speed = 1
        self.type = "Prey"
        self.exists = 10

    def get_vision(self):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                if self.world.map[int(int(self.pos.x))][int(int(self.pos.y - i))].entity is None:
                    continue
                elif self.world.map[int(self.pos.x)][int(self.pos.y - i)].entity == "Predator":
                    # Certainty of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                if self.world.map[int(int(self.pos.x))][int(int(self.pos.y + i))].entity is None:
                    continue
                elif self.world.map[int(self.pos.x)][int(self.pos.y + i)].entity == "Predator":
                    # Certainty of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                if self.world.map[int(self.pos.x + i)][int(self.pos.y)].entity is None:
                    continue
                elif self.world.map[int(self.pos.x + i)][int(self.pos.y)].entity == "Predator":
                    # Certainty of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                if self.world.map[int(self.pos.x - i)][int(self.pos.y)].entity is None:
                    continue
                elif self.world.map[int(self.pos.x - i)][int(self.pos.y)].entity == "Predator":
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret

    def move_and_collide(self, direction: Vector2, speed):

        self.pos += direction * speed
        self.world.map[int(self.pos.x)][int(self.pos.y)].entity = self.type

        pass
