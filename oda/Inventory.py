from oda import Data


# Getter Functions

def get(_id):
    return Data.get_attribute(_id, "inventory", [])


def get_resource(_id, name):
    inv = get(_id)
    if name not in inv:
        amount = 0
    else:
        amount = inv[name]
    return amount


# Modify Functions

def give_resource(_id, name, amount=1):
    inv = get_inventory(_id)
    inv.setdefault(name, 0)
    inv[name] += amount
    if inv[name] < 0:
        inv[name] -= amount
        return False
    if inv[name] == 0:
        inv.pop(name)
    Data.save()
    return True


def take_resource(_id, name, amount):
    give_resource(_id,name,-amount)



