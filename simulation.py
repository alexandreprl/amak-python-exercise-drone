from amak import PygameScheduler

from entities import DroneAgent
from system import DroneExerciseEnvironment, DroneExerciseMAS, GRID_WIDTH, GRID_HEIGHT

environment = DroneExerciseEnvironment(room=1)
mas = DroneExerciseMAS(environment)

for i in range(50):
    x = 0
    y = 0
    DroneAgent(mas, (x, y))

if __name__ == "__main__":
    PygameScheduler(mas, environment, GRID_WIDTH * 10, GRID_HEIGHT * 10, 120)
