import json

data = json.loads(open("Oda.json").read())


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


def get_person(_id):
    _id = str(_id)
    return get(_id, dict())


def get_attribute(_id, name, default=None):
    person = get_person(_id)
    if default is not None:
        person.setdefault(name, default)
    return person[name]


# Setters

def set_attribute(_id, name, value):
    person = get_person(_id)
    person[name] = value
    save()

# Misc
