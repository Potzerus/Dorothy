import discord


class Entity:
    def __init__(self, name, x=-1, y=-1, controllable=False):
        self.name = name
        self.x, self.y = x, y
        self.controllable = controllable

    def tick(self):
        pass

    def embed(self):
        return discord.Embed(title="No Implementation found for %s" % self.name)
