import json

from discord.ext import commands
from discord.ext.commands import Cog
import discord


def is_oda(ctx):
    return ctx.author.id == 273988946264981506


class OdaCord(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.data = json.loads(open("Odacoins.json").read())

    def get_balance(self, id):
        id = str(id)
        if id not in self.data:
            self.data[id] = 0
        return self.data[id]

    def save(self):
        with open("../Points.json", "w") as da_file:
            da_file.write(json.dumps(self.data))

    def change_balance(self, id, amount):
        self.get_balance(id)
        id = str(id)
        self.data[id] += amount

    def get_leaderboard(self):
        leaderboard = dict(self.data)
        return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    async def cog_check(self, ctx):
        if ctx.guild is not None and ctx.guild.id == 747340433398693959:
            return True
        else:
            return False

    @commands.group(aliases=["oc"])
    async def odacoins(self, ctx, target: discord.Member = None):
        if not target:
            target = ctx.author
        await ctx.send("{.name} has {} odacoins".format(target, self.get_balance(target.id)))

    @odacoins.command(name="add", aliases=["make"])
    @commands.check(is_oda)
    async def coins_add(self, ctx, target: discord.Member = None, amount: int = 0):
        if target is None:
            target = ctx.author
        self.change_balance(target.id, amount)
        await ctx.send("Balance changed by %d!" % amount)
        self.save()

    @odacoins.command()
    async def give(self, ctx, other: discord.Member, amount: int = 0):
        if amount == 0:
            await ctx.send("You really want to give nothing? How heartless")
            return
        if amount < 0:
            await ctx.send("You know stealing is wrong right?(and wouldn't be fun if i added it like that)")
            return
        if ctx.author == other:
            await ctx.send("You can't give yourself points silly")
            return
        if self.get_balance(ctx.author.id) < amount:
            await ctx.send("You don't have that much to give!")
            return
        self.change_balance(ctx.author.id, amount * -1)
        self.change_balance(other.id, amount)
        await ctx.send("Transaction successful!")
        self.save()
