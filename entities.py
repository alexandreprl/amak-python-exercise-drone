from random import choice, random

from amak import RenderableAgent


def grid_to_display_position(on_grid_position):
    return 5 + on_grid_position[0] * 10, 5 + on_grid_position[1] * 10


class DroneAgent(RenderableAgent):
    def __init__(self, mas, on_grid_position):
        self.on_grid_position = on_grid_position
        super().__init__(mas, grid_to_display_position(self.on_grid_position), "black")
        self.set_on_grid_position(on_grid_position)

    def set_on_grid_position(self, on_grid_position):
        g = self.amas.environment.grid[self.on_grid_position[1]][self.on_grid_position[0]]
        if self in g:
            g.remove(self)
        self.on_grid_position = on_grid_position
        self.set_position(grid_to_display_position(on_grid_position))
        self.amas.environment.grid[self.on_grid_position[1]][self.on_grid_position[0]].append(self)

    def take_picture(self):
        self.amas.environment.reset_cell_criticality(self.on_grid_position)

    # Methods to implement
    def on_perceive(self):
        pass

    def on_decide_and_act(self):
        self.take_picture()
        # Exercise: Implement the Drone decision and action
        self.move_randomly()

    # Helper methods
    def move_toward_position(self, target_position):
        if target_position is None:
            return
        x, y = self.on_grid_position
        tx, ty = target_position
        if x < tx:
            self.set_on_grid_position((x + 1, y))
        elif x > tx:
            self.set_on_grid_position((x - 1, y))
        elif y < ty:
            self.set_on_grid_position((x, y + 1))
        elif y > ty:
            self.set_on_grid_position((x, y - 1))

    def move_randomly(self):
        new_position = None
        max_attempt = 10
        while (max_attempt > 0 and not self.amas.environment.is_on_grid_position_valid(new_position)) and not self.amas.environment.is_on_grid_position_empty(new_position):
            direction = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            new_position = (self.on_grid_position[0] + direction[0], self.on_grid_position[1] + direction[1])
            max_attempt -= 1
        if max_attempt > 0:
            self.set_on_grid_position(new_position)