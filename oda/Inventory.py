from oda import Data
from oda.User import User

"""
The inventory consists of two elements, item storage and resource storage
resources are non-unique and stored in a dictionary with the name:amount format

items are unique and complex classes stored in a list
"""
class Inventory:

    # Getter Functions

    @classmethod
    def get(cls,_id):
        user = User.get(_id)
        if not user.inventory:
            user.inventory = Inventory()



    def get_resource(_id, name):
        inv = get(_id)
        if name not in inv:
            amount = 0
        else:
            amount = inv[name]
        return amount


    # Modify Functions

    def give_resource(_id, name, amount=1):
        inv = get(_id)
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
        return give_resource(_id,name,-amount)



