from util.Entities import Entity
import json
import discord

part_dict = json.loads(open("Parts.json").read())
resources = json.loads(open("Resources.json").read())


class Drone(Entity):
    default_stats = {
        "mass": 0,
        "vision range": 0,
        "move time": 0,
    }

    def __init__(self, name, x, y, parts, owner, cargo=None):
        super().__init__(name, x, y)
        self.parts = parts
        self.owner = owner
        self.types = []
        self.stats = dict(Drone.default_stats)
        for name in parts:
            for stat, value in part_dict[name].items():
                if stat == "type":
                    if value in self.types:
                        raise ("Duplicate Type %s" % value)
                    else:
                        self.types.append(value)
                elif stat not in self.stats:
                    self.stats[stat] = value
                else:
                    self.stats[stat] += value
        self.cargo = cargo or {}
        self.mass = self.stats["mass"]
        self.task = None
        self.task_time = 0
        self.task_name = None
        self.instructions = []

    def tick(self):
        if self.task is None:
            if not self.instructions:
                return None
            self.task, self.task_time, self.task_name = self.instructions.pop(0)
        self.task_time -= 1
        if self.task_time <= 0:
            self.task()
            self.task = None
            name = self.task_name
            self.task_name = None
            return name

    def calc_cargo_mass(self):
        total = 0
        for resource, amount in self.cargo.items():
            total += resources[resource]["density"] * amount
        return total

    # def __str__(self):
    #     return "{.name}, owned by <@{.owner}>".format(self, self)

    def __repr__(self):
        return "{.name}\nTask: {.task_name}\nStats: {.stats}".format(self, self, self)

    def add_instruction(self, task, time: int, name: str = "Unnamed Task"):
        self.instructions.append((task, time, name))

    def embed(self):
        _embed = discord.Embed(title=self.name)
        _embed.description = str(self.stats)
        return _embed
