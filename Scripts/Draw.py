import pygame
from World import *


class Draw(World):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode(self.RESOLUTION)
        self.surface = pygame.Surface(self.RESOLUTION, pygame.SRCALPHA)
        self.FPS = 10
        self.clock = pygame.time.Clock()

    def map_value(self, x, x_min, x_max, y_min, y_max):
        return y_min + ((x - x_min) * (y_max - y_min)) / (x_max - x_min)

    def draw_entity(self):
        # Energy checks for the entity are run here as the draw function runs every frame
        keys = list(self.predator_set.keys())
        for pos in keys:
            if pos in self.predator_set.keys():
                predator = self.predator_set[pos]
                predator.Energy -= predator.exists
                if predator.Energy > predator.Max_Energy:
                    predator.Energy = predator.Max_Energy
                if predator.Energy <= 0:
                    del self.predator_set[pos]
                    continue
                trans = self.map_value(predator.Energy, 1, predator.Max_Energy, 50, 255)
                pygame.draw.circle(
                    self.surface,
                    (255, 0, 0, int(trans)),
                    (
                        pos[0] * self.cell_size + self.cell_size // 2,
                        pos[1] * self.cell_size + self.cell_size // 2,
                    ),
                    self.cell_size // 2,
                )
        key = list(self.prey_set.keys())
        for pos in key:
            prey = self.prey_set[pos]
            prey.Energy -= prey.exists
            if prey.Energy > prey.Max_Energy:
                prey.Energy = prey.Max_Energy
            if prey.Energy <= 0:
                del self.prey_set[pos]
                continue

            trans = self.map_value(prey.Energy, 1, prey.Max_Energy, 50, 255)
            pygame.draw.circle(
                self.surface,
                (0, 0, 255, trans),
                (
                    pos[0] * self.cell_size + self.cell_size // 2,
                    pos[1] * self.cell_size + self.cell_size // 2,
                ),
                self.cell_size // 2,
            )

    def loop(self):
        self.screen.fill(pygame.Color("white"))
        self.surface.fill(pygame.Color("white"))
        self.clock.tick(self.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self.test_move()
        self.draw_entity()
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()


test = Draw()
test.populate()
while True:
    test.loop()
