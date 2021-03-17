from discord.ext import commands
from discord.ext.commands import Cog
import discord


class PrayCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.encounters = []

    def has_char(self, user_id):
        return user_id in self.players

    # TODO:[after 1.0] replace this with an actual id system
    def encounter_id(self, user1_id, user2_id):
        return str(user1_id) + str(user2_id) if user1_id < user2_id else str(user2_id) + str(user1_id)

    @commands.command()
    async def worship(self, ctx):
        pass

    @commands.group(invoke_without_command=True)
    async def character(self, ctx):
        await ctx.send(str(self.players[ctx.author.id]))

    @character.command(name="create")
    async def character_add(self, ctx):
        if not self.has_char(ctx.author.id):
            await ctx.send("You already have a character")
            return

        self.players[ctx.author.id] = {
            "name": ctx.author.name,
            "max_health": 20,
            "health": 20,
            "inventory": [],
            "level": 1,
            "maxlevel": 20,
            "titles": [],
        }

    @commands.command(name="duel")
    async def initiate_encounter(self, ctx, target: discord.Member):
        initiator = ctx.author.id
        targeted = target.id
        if not self.has_char(initiator):
            await ctx.send("You don't have a character!")
            return
        if initiator == targeted:
            await ctx.send("You can't fight yourself!")
            return
        if not self.has_char(targeted):
            await ctx.send("Target doesn't have a character!")
            return
        e_id = self.encounter_id(initiator, targeted)
        # replace this with a check pulling up encounters and seeing if the characters are in any
        for encounter in self.encounters:
            if initiator in encounter["participants"]:
                await ctx.send("You are already in combat!")
                return
            if targeted in encounter["participants"]:
                await ctx.send("This character is already in combat!")
                return

        encounter = {
            "participants": [initiator, targeted],
            "turn_tracker": 0,
            "turn_available": [True, True],
            "id": e_id,
        }

    @commands.command()
    async def attack(self, ctx, target: discord.Member):
        if not self.has_char(ctx.author.id):
            await ctx.send("You don't have a character!")
            return
        if not self.has_char(target.id):
            await ctx.send("Target doesn't have a character!")
            return
