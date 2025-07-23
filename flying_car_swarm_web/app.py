from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

class FlyingCar:
    def __init__(self, id, position, destination):
        self.id = id
        self.position = np.array(position, dtype=float)
        self.destination = np.array(destination, dtype=float)
        self.velocity = np.random.uniform(-1, 1, 3)
        self.max_speed = 2.0
        self.safe_distance = 10.0
        self.neighbor_distance = 30.0
        self.weather = "clear"

    def set_weather(self, condition):
        self.weather = condition
        if condition == "rain":
            self.max_speed = 1.2
            self.safe_distance = 12.0
        elif condition == "fog":
            self.max_speed = 0.8
            self.neighbor_distance = 15.0
        else:
            self.max_speed = 2.0
            self.safe_distance = 10.0
            self.neighbor_distance = 30.0

    def update_velocity(self, cars):
        separation = np.zeros(3)
        alignment = np.zeros(3)
        cohesion = np.zeros(3)
        goal = (self.destination - self.position) * 0.01
        count = 0

        for car in cars:
            if car.id == self.id:
                continue
            diff = car.position - self.position
            dist = np.linalg.norm(diff)

            if dist < self.neighbor_distance:
                if dist < self.safe_distance and dist != 0:
                    separation -= diff / dist
                alignment += car.velocity
                cohesion += car.position
                count += 1

        if count > 0:
            alignment /= count
            alignment = (alignment - self.velocity) * 0.05
            cohesion /= count
            cohesion = (cohesion - self.position) * 0.01

        if self.weather == "wind":
            wind = np.random.normal(0, 0.3, size=3)
        else:
            wind = np.zeros(3)

        self.velocity += separation + alignment + cohesion + goal + wind
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

    def update_position(self):
        self.position += self.velocity


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    weather = data.get("weather", "clear")
    starts = data.get("starts", [])
    ends = data.get("ends", [])

    cars = []
    for i, (start, end) in enumerate(zip(starts, ends)):
        # Apply spacing offset to reduce visual overlap
        offset = i * 50
        start = [float(c) + offset for c in start]
        end = [float(c) for c in end]
        car = FlyingCar(i, start, end)
        car.set_weather(weather)
        cars.append(car)

    all_positions = []
    for _ in range(200):  # simulate 200 frames
        for car in cars:
            car.update_velocity(cars)
        for car in cars:
            car.update_position()
        all_positions.append([car.position.tolist() for car in cars])

    return jsonify(all_positions)


if __name__ == '__main__':
    app.run(debug=True)
