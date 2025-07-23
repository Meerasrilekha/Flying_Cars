# simulation_engine.py
from .flying_car import FlyingCar
import random

class SwarmSimulator:
    def __init__(self, num_cars, start_point, end_point, weather):
        self.cars = [
            FlyingCar(
                id=i,
                position=[
                    start_point[0] + random.uniform(-10, 10),
                    start_point[1] + random.uniform(-10, 10),
                    start_point[2] + random.uniform(-5, 5)
                ],
                destination=end_point,
                weather=weather
            )
            for i in range(num_cars)
        ]

    def step(self):
        for car in self.cars:
            car.update_velocity(self.cars)
        for car in self.cars:
            car.update_position()

    def get_positions(self):
        return [car.get_position() for car in self.cars]
