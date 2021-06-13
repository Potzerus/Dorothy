from oda import Data


def get_balance(_id):
    return Data.get_attribute(_id, "odacoins", 0)


def set_balance(_id, amount):
    Data.set_attribute(_id, "odacoins", amount)
    Data.save()


def change_balance(_id, amount):
    bal = get_balance(_id)
    bal = bal + amount
    set_balance(_id, bal)
