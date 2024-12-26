import random, pygame, neat
from abc import ABC, abstractmethod
from pygame import Vector2


class Entity(ABC):
    def __init__(self, pos: Vector2, world, config, genome=None):
        self.world = world
        self.movement_cost = 2
        self.Energy = 100
        self.pos: Vector2 = pos
        self.top_speed = 20.0
        self.vision = 3
        self.type = genome

        # Neat parameters
        self.config = config
        self.config = config
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, config)

    # Check of other species in the neighbour
    @abstractmethod
    def get_vision(self) -> []:
        ...

    '''
    Get the input for the neural network
    Energy
    world_luminance
    Opposite species in N (0 if no 3-1 if yes (depending of how close it is)) for 3 blocks
                        S
                        E
                        W
    Type of terrain     Land (0 if false 1 if true)
                        Water
                        Forest
    '''

    def network_inputs(self):
        to_ret = []
        entity_info = [self.Energy / 100]
        luminance = [self.world.luminance / 100]
        entity_vision = self.get_vision()
        # print((entity_vision))
        region = []
        x = int(self.pos.x)
        y = int(self.pos.y)
        if self.world.map[x][y].element == "Land":
            region = [1, 0, 0]
        if self.world.map[x][y].element == "Forest":
            region = [0, 1, 0]
        if self.world.map[x][y].element == "Water":
            region = [0, 0, 1]
        to_ret += entity_info
        to_ret += luminance
        to_ret += entity_vision
        to_ret += region
        return to_ret

    # Output action Depends of the species specified on the implementation
    @abstractmethod
    def preform_action(self, output):
        ...

    # Use the neural network to make a decision based on inputs
    def decide(self):
        return self.net.activate(self.network_inputs())

    # Implements movement and collision and feeding
    @abstractmethod
    def move_and_collide(self, direction, speed):
        ...


class Predator(Entity):
    def __init__(self, pos: Vector2, world, predator_config, genome=None):
        super().__init__(pos, world, predator_config, genome)
        self.speed = 1
        self.type = "Predator"
        self.exists = 1
        # self.Max_Energy = self.world.GRID.x * (self.movement_cost)
        self.Max_Energy = 100
        self.eat_gain = self.Max_Energy // 2
        self.fitness = 0
        self.reward = 50
        self.genome.fitness = self.fitness
        self.dies = self.Max_Energy // 2 * 3

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
                    )[0]
        return to_ret

    '''
      Probability of moving North
                            South
                            East
                            West
      Probability of doing nothing
      Probability of killing entity in front
      '''

    def preform_action(self, output):
        max_index = output.index(max(output))
        match max_index:
            case 0:
                self.move_and_collide(Vector2(0, -1), 1)
            case 1:
                self.move_and_collide(Vector2(0, 1), 1)
            case 2:
                self.move_and_collide(Vector2(1, 0), 1)
            case 3:
                self.move_and_collide(Vector2(-1, 0), 1)
            case 4:
                self.move_and_collide(Vector2(0, 0), 1)
        '''Implement the killing mechanism'''

    # Move and kill
    # set the fitness function of prey if it is killed
    def move_and_collide(self, direction: Vector2, speed):
        # Move
        pos = self.pos + direction * speed
        if (
                (pos.x, pos.y) not in self.world.predator_set
                and pos[0] < self.world.GRID.x and pos[0] >= 0
                and pos[1] < self.world.GRID.y and pos[1] >= 0
        ):
            del self.world.predator_set[(self.pos.x, self.pos.y)]
            self.pos = pos
            self.world.predator_set[(self.pos.x, self.pos.y)] = self
            self.Energy -= self.movement_cost

        # Eat prey
        if (self.pos.x, self.pos.y) in self.world.prey_set:
            # Punishment for being eaten
            prey = self.world.prey_set[self.pos.x, self.pos.y]
            prey.fitness -= prey.get_killed / self.world.time
            prey.genome.fitness = prey.fitness
            del self.world.prey_set[(self.pos.x, self.pos.y)]

            self.Energy += self.eat_gain

            # Reward for eating prey
            self.fitness += self.reward
            self.genome.fitness = self.fitness


class Prey(Entity):
    def __init__(self, pos: Vector2, world, prey_config, genome=None):
        super().__init__(pos, world, prey_config, genome)
        self.speed = 1
        self.type = "Prey"
        self.fitness = 50
        self.exists = 1
        # self.Max_Energy = self.world.GRID.x * (self.movement_cost + self.exists)
        self.Max_Energy = 100
        self.get_killed = self.Max_Energy / 2
        self.dies = self.Max_Energy // 6
        self.genome.fitness = self.fitness

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
                    )[0]

        return to_ret

    '''
    Probability of moving North
                          South
                          East
                          West
    Probability of doing nothing
    '''

    def preform_action(self, output):
        max_index = output.index(max(output))
        match max_index:
            case 0:
                self.move_and_collide(Vector2(0, -1), 1)
            case 1:
                self.move_and_collide(Vector2(0, 1), 1)
            case 2:
                self.move_and_collide(Vector2(1, 0), 1)
            case 3:
                self.move_and_collide(Vector2(-1, 0), 1)
            case 4:
                self.move_and_collide(Vector2(0, 0), 1)

    def move_and_collide(self, direction: Vector2, speed):
        self.genome.fitness = self.fitness
        pos = self.pos + direction * speed
        if (
                (pos.x, pos.y) not in self.world.prey_set
                and pos[0] < self.world.GRID.x and pos[0] >= 0
                and pos[1] < self.world.GRID.y and pos[1] >= 0
        ):
            del self.world.prey_set[(self.pos.x, self.pos.y)]
            self.pos = pos
            self.Energy -= self.movement_cost
            self.world.prey_set[(self.pos.x, self.pos.y)] = self
