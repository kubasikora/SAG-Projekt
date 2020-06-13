import random, json

agent_number = 8

car_types = pow(3, agent_number)

car_vector = []


indexes = random.sample(range(0, car_types), 9)

for i in range(0, car_types):
    if i in indexes:
        car_vector.append(random.choice(range(1, 9)))
        print(car_vector[i])
        print(i)
    else:
        car_vector.append(0)

'''
for i in range(0, car_types):
    if random.random() > 0.9:
        car_vector.append(random.choice(range(1, 10)))
    else:
        car_vector.append(0)
'''


with open("config/generate_vector5.json", "w") as write_file:
    json.dump(car_vector, write_file)