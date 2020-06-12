import random, json

agent_number = 8

car_types = pow(3, agent_number)

car_vector = []

for i in range(0, car_types):
    if random.random() > 0.75:
        car_vector.append(random.choice(range(1, 10)))
    else:
        car_vector.append(0)

with open("config/generate_vector.json", "w") as write_file:
    json.dump(car_vector, write_file)