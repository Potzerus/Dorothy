from discord.ext import commands
from util import *


class DroneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.map = Map(open("DefaultMap").read())
        self.controllables = {}
        entity_list = []
        for entity in entity_list:
            if hasattr(entity, "owner"):
                self.add_drone(entity, entity.owner)
        self.selector = {}
        self.assign_selectors()

    def add_drone(self, drone, owner_id):
        self.map.entities.append(drone)
        if owner_id not in self.controllables:
            self.controllables[owner_id] = []
        self.controllables[owner_id].append(drone)

    def assign_selectors(self):
        for owner_id, entities in self.controllables.items():
            if owner_id not in self.selector and len(entities) > 0:
                self.selector[owner_id] = 0

    async def check_controllables(self, ctx):
        if ctx.author_id not in self.controllables:
            await ctx.send("You do not have controllable drones!")
            return False
        return True
    @commands.group(invoke_without_command=True)
    async def drone(self, ctx):
        if ctx.author.id not in self.controllables:
            await ctx.send("You do not have controllable drones!")
            return
        drone = self.controllables[ctx.author.id][self.selector[ctx.author.id]]
        await ctx.send(embed=drone.embed())

    @drone.command(name="list")
    async def drone_list(self, ctx):
        if ctx.author.id not in self.controllables:
            await ctx.send("You do not have controllable drones!")
            return
        embeds = [i.embed() for i in self.controllables[ctx.author.id]]
        await paginate(ctx, embeds)

    @drone.command(name="create")
    @commands.is_owner()
    async def drone_create(self, ctx, name, *parts):
        drone = Drone(name, 2, 2, parts, ctx.author.id)
        self.add_drone(drone, ctx.author.id)

        self.assign_selectors()

    @drone.command(name="remove")
    @commands.is_owner()
    async def drone_remove(self, ctx, name):
        pass
