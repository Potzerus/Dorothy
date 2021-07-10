import Data


class User:

    def __init__(self, owner_id: int):
        self._id = owner_id
        self.attributes = {}
        self.inventory = None
        self.wallet = 0

    @classmethod
    def get(self, _id: int):
        users: dict = Data.get("user", dict())
        if str(_id) not in users:
            users.setdefault(str(_id), User(_id))
            Data.save()
        return users[str(_id)]

    def __getitem__(self, name: str):
        return self.attributes[name]

    def __setitem__(self, name, value):
        self.attributes[name] = value
        Data.save()
