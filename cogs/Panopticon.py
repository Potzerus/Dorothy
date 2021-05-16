from discord.ext import commands

import discord
import datetime


class Panopticon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.intent = False
        self.time = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!updog":
            if message.author.id in [122739797646245899, 125660719323676672]:
                if self.bot.get_user(673737213959208980).Status == discord.Status.online:
                    self.tokens += 1
                await self.bot.get_guild(303307934774067210).get_channel(842931370695196682).send(
                    "Restart Initiated")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.id != 673737213959208980:
            return

        if after.Status != discord.Status.offline:
            return

        if self.intent:
            self.intent = False
            return

        await self.bot.get_guild(303307934774067210).get_channel(842931370695196682).send(
            "Bot just went offline <@!122739797646245899>,<@!125660719323676672>")

    @commands.group()
    async def intent(self, ctx):
        await ctx.send(self.intent)

    @intent.command()
    async def off(self, ctx):
        self.intent = False
        await ctx.send(self.intent)

    @intent.command()
    async def on(self, ctx):
        self.intent = True
        await ctx.send(self.intent)
