# flying_car.py
import numpy as np

class FlyingCar:
    def __init__(self, id, position, destination, weather='clear'):
        self.id = id
        self.position = np.array(position, dtype=float)
        self.destination = np.array(destination, dtype=float)
        self.velocity = np.random.rand(3) * 2 - 1
        self.max_speed = 2.0
        self.safe_distance = 5.0
        self.neighbor_distance = 20.0
        self.weather = weather

    def update_weather_params(self):
        if self.weather == "rain":
            self.max_speed = 1.2
            self.safe_distance = 8.0
        elif self.weather == "wind":
            self.velocity += np.random.normal(0, 0.5, size=3)
        elif self.weather == "fog":
            self.max_speed = 0.8
            self.neighbor_distance = 10.0
        else:
            self.max_speed = 2.0
            self.safe_distance = 5.0
            self.neighbor_distance = 20.0

    def get_position(self):
        return self.position.tolist()

    def update_velocity(self, cars):
        self.update_weather_params()

        separation = np.zeros(3)
        alignment = np.zeros(3)
        cohesion = np.zeros(3)
        goal_attraction = (self.destination - self.position) * 0.01
        count = 0

        for car in cars:
            if car.id != self.id:
                distance_vector = car.position - self.position
                distance = np.linalg.norm(distance_vector)

                if distance < self.neighbor_distance:
                    if distance < self.safe_distance and distance != 0:
                        separation -= distance_vector / distance
                    alignment += car.velocity
                    cohesion += car.position
                    count += 1

        if count > 0:
            alignment /= count
            alignment = (alignment - self.velocity) * 0.05
            cohesion /= count
            cohesion = (cohesion - self.position) * 0.01

        self.velocity += separation + alignment + cohesion + goal_attraction
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

    def update_position(self):
        self.position += self.velocity
