import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog
# from util.pray_utils import *


class PrayCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = json.loads(open("Pray.json", mode="r").read())

    def save(self):
        open("Pray.json", mode="w+").write(json.dumps(self.players))

    def has_char(self, user_id):
        return user_id in self.players

    def get_char(self, user_id):
        return self.players.get(user_id, None)

    def gen_char(self, user_id):
        char = None # Character(user_id)
        self.players[user_id] = char
        return char

    def get_or_gen_char(self, user_id):
        char = self.get_char(user_id)
        if not char:
            char = self.gen_char(user_id)
        return char

    # TODO: add mechanism for contributing to a power tree
    @commands.command()
    async def worship(self, ctx):
        pass

    @commands.group(invoke_without_command=True)
    async def character(self, ctx):
        await ctx.send(str(self.players[ctx.author.id]))

    @character.command(name="start")
    async def character_add(self, ctx):
        if not self.has_char(ctx.author.id):
            await ctx.send("You already have a character")
            return

    @commands.command()
    async def attack(self, ctx, target: discord.Member):
        if not self.has_char(ctx.author.id):
            await ctx.send("You don't have a character!")
            return
        if not self.has_char(target.id):
            await ctx.send("Target doesn't have a character!")
            return

    @commands.command()
    async def status(self, ctx):
        """
        Retrieve your own status
        """
        player = self.get_or_gen_char(ctx.author.id)
        embed = discord.Embed(title="%s Status" % player.name)
        embed.description = f"Health: {player.health}/{player.max_health}\n" \
                            f"Level: {player.level}/{player.max_level}\n" \
                            f""

        def display_strings(field_name):

            entries = [entry for entry in getattr(player, field_name.lower())]

            if entries:
                if hasattr(entries[0], "name"):
                    entries = [entry.name for entry in entries]
                entries = ", ".join(entries)
                embed.add_field(name=field_name.replace("_", " "), value=entries[:1024])

        display_strings("Effects")
        display_strings("Titles")

        # embed.add_field(name="_", value="_")

        await ctx.send(embed=embed)
