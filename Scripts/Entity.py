import random
import pygame
from pygame import Vector2


class Entity:
    def __init__(self, pos: Vector2,world):
        self.world=world
        self.Energy = 100.0
        self.pos: Vector2 = pos
        self.top_speed = 20.0
        self.vision = 3

    # To get the grid position for computation as entities can have different speed
    # The movement of entities is not gird wise rather pixel wise
    # def get_pos(self):
    #     pass

    def get_vision(self):
        return []

    def network_inputs(self):
        to_ret = []
        entity_info = [
            self.Energy,
            self.pos.x,
            self.pos.y,
        ]
        self.world= [self.world.luminance]
        entity_vision = self.get_vision()
        to_ret.extend(entity_info)
        to_ret.extend(self.world)
        to_ret.extend(entity_vision)
        return to_ret

    def move(self,direction):



class Preditor(Entity):
    def __init__(self, pos: Vector2):
        super().__init__(pos)

    def get_vision(self ):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                if self.world.map[self.pos.x][self.pos.y - i].entity is None:
                    continue
                elif self.world.map[self.pos.x][self.pos.y - i].entity == "Prey":
                    # Centanity of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                if self.world.map[self.pos.x][self.pos.y + i].entity is None:
                    continue
                elif self.world.map[self.pos.x][self.pos.y + i].entity == "Prey":
                    # Centanity of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                if self.world.map[self.pos.x + i][self.pos.y].entity is None:
                    continue
                elif self.world.map[self.pos.x + i][self.pos.y].entity == "Prey":
                    # Centanity of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                if self.world.map[self.pos.x - i][self.pos.y].entity is None:
                    continue
                elif self.world.map[self.pos.x - i][self.pos.y].entity == "Prey":
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret


class Prey(Entity):
    def __init__(self, pos: Vector2):
        super().__init__(pos)

    def get_vision(self):
        probability = self.world.luminance / 100

        # to_ret = [opposite species in north till vision, south, east, west,]
        to_ret = [0 for _ in range(4)]

        for i in range(1, self.vision + 1):

            # North vision
            if self.pos.y - i >= 0 and to_ret[i] == 0:
                if self.world.map[self.pos.x][self.pos.y - i].entity is None:
                    continue
                elif self.world.map[self.pos.x][self.pos.y - i].entity == "Preditor":
                    # Centanity of vision depends on luminance
                    to_ret[0] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # South Vision
            if self.pos.y + i < self.world.GRID.y and to_ret[1] == 0:
                if self.world.map[self.pos.x][self.pos.y + i].entity is None:
                    continue
                elif self.world.map[self.pos.x][self.pos.y + i].entity == "Preditor":
                    # Centanity of vision depends on luminance
                    to_ret[1] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # East Vision
            if self.pos.x + i < self.world.GRID.x and to_ret[2] == 0:
                if self.world.map[self.pos.x + i][self.pos.y].entity is None:
                    continue
                elif self.world.map[self.pos.x + i][self.pos.y].entity == "Preditor":
                    # Centanity of vision depends on luminance
                    to_ret[2] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )[0]

            # West Vision
            if self.pos.x - i < 0 and to_ret[3] == 0:
                if self.world.map[self.pos.x - i][self.pos.y].entity is None:
                    continue
                elif self.world.map[self.pos.x - i][self.pos.y].entity == "Preditor":
                    to_ret[3] = random.choices(
                        [self.vision + 1 - i, 0], weights=[probability, 1 - probability]
                    )

            return to_ret
