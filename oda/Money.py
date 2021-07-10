from oda import Data, User


def get_balance(_id):
    return User.get_attribute(_id, "odacoins", 0)


def set_balance(_id, amount):
    User.set_attribute(_id, "odacoins", amount)
    Data.save()


def change_balance(_id, amount):
    bal = get_balance(_id)
    bal = bal + amount
    set_balance(_id, bal)
