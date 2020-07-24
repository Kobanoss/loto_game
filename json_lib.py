import json


def read_json(name):
    with open(name, "r+") as file:
        data = json.load(file)
        return data


def add_to_json(name, key, value):
    buffer_data = read_json(name)
    buffer_data[key] = value
    with open("stat.json", "w+") as file:
        json.dump(buffer_data, file)


def sort_json(name):
    new_buffer_data = {}
    buffer_data = read_json(name)
    for key in sorted(buffer_data.keys())[::-1]:
        new_buffer_data[key] = buffer_data[key]
    with open(name, "w+") as file:
        json.dump(new_buffer_data, file)


def print_json(name):
    buffer_data = read_json(name)
    data = ''
    for key, value in buffer_data.items():
        data += str(key) + ' - ' + str(value) + '\n'
    return data
