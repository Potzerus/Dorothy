import json
import _csv
import csv

data = json.loads(open("Oda.json").read())
reader = csv.reader(open("Oda.csv").read())
data = None

def save():
    with open("Oda.json", "+w") as da_file:
        return da_file.write(json.dumps(data))


# Getters

def get(name, default=None):
    if default is not None:
        data.setdefault(name, default)
    if name in data:
        return data[name]
    else:
        return None


def get_attribute(_id, attr, default=None):
    char = get(_id)
    if default is not None:
        char.setdefault(attr, default)




# Setters


# Misc
