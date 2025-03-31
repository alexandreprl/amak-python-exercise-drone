import pygame
from amak import MAS
import random

GRID_WIDTH = 100
GRID_HEIGHT = 50
MAX_CRITICALITY = 10000

class DroneExerciseMAS(MAS):
    def __init__(self, environment):
        super().__init__(environment)


class DroneExerciseEnvironment:
    def __init__(self, room=1):
        self.events = []
        w, h = GRID_WIDTH, GRID_HEIGHT
        self.dragging = False
        self.grid = [[[] for x in range(w)] for y in range(h)]
        self.cells_criticalities = [[random.randint(0, MAX_CRITICALITY) for x in range(w)] for y in range(h)]

    def cycle(self):
        events = self.events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
        if self.dragging:
            x, y =  pygame.mouse.get_pos()
            x //= 10
            y //= 10
            for i in range(max(0, x - 5), min(GRID_WIDTH, x + 5)):
                for j in range(max(0, y - 5), min(GRID_HEIGHT, y + 5)):
                    if (i - x) ** 2 + (j - y) ** 2 <= 5 ** 2:
                        self.cells_criticalities[j][i] += 100


        self.cells_criticalities = [[min(cell + 1, MAX_CRITICALITY) for cell in row] for row in
                                    self.cells_criticalities]

        for x in range(GRID_WIDTH // 2 - 5, GRID_WIDTH // 2 + 5):
            for y in range(GRID_HEIGHT // 2 - 5, GRID_HEIGHT // 2 + 5):
                self.cells_criticalities[y][x] = min(self.cells_criticalities[y][x] + 100, MAX_CRITICALITY)

    def render(self, display_surface):
        display_surface.fill((255, 255, 255))

        # draw green to red squares from cells_criticalities between 0 and 100
        green = (0, 255, 0)
        red = (255, 0, 0)

        for x in range(0, len(self.cells_criticalities[0])):
            for y in range(0, len(self.cells_criticalities)):
                criticality = self.cells_criticalities[y][x]
                color = (int((red[0] - green[0]) * criticality / MAX_CRITICALITY + green[0]),
                         int((red[1] - green[1]) * criticality / MAX_CRITICALITY + green[1]),
                         int((red[2] - green[2]) * criticality / MAX_CRITICALITY + green[2]))
                display_surface.fill(color, (x * 10, y * 10, 10, 10))

    def remove_entity(self, entity):
        if not self.is_on_grid_position_valid(entity.on_grid_position):
            return
        self.grid[entity.on_grid_position[1]][entity.on_grid_position[0]].remove(entity)

    def reset_cell_criticality(self, position):
        if not self.is_on_grid_position_valid(position):
            return
        self.cells_criticalities[position[1]][position[0]] = 0

    # Helper methods
    def is_on_grid_position_valid(self, position):
        if position is None:
            return False
        x, y = position
        return 0 <= position[0] < len(self.grid[0]) and 0 <= position[1] < len(self.grid)

    def is_on_grid_position_empty(self, position):
        if not self.is_on_grid_position_valid(position):
            return False
        return not self.grid[position[1]][position[0]]

    def retrieve_cell_positions_with_highest_criticality(self, on_grid_position, radius):
        x, y = on_grid_position
        max_criticality = 0
        max_position = [(x, y)]
        # if multiple position with same criticality return a random one
        for i in range(max(0, x - radius), min(GRID_WIDTH, x + radius)):
            for j in range(max(0, y - radius), min(GRID_HEIGHT, y + radius)):
                if self.cells_criticalities[j][i] > max_criticality:
                    max_criticality = self.cells_criticalities[j][i]
                    max_position = [(i, j)]
                elif self.cells_criticalities[j][i] == max_criticality:
                    max_position.append((i, j))

        return max_position

    def retrieve_closest_drone_position(self, drone, radius):
        x, y = drone.on_grid_position
        min_distance = float('inf')
        closest_position = None
        for i in range(max(0, x - radius), min(GRID_WIDTH, x + radius)):
            for j in range(max(0, y - radius), min(GRID_HEIGHT, y + radius)):
                if (i, j) != (x, y) and self.grid[j][i]:
                    distance = abs(i - x) + abs(j - y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_position = (i, j)
        return closest_position

