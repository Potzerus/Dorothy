from discord.ext import commands

import discord


class Panopticon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tokens = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!updog":
            if message.author.id in [122739797646245899, 125660719323676672]:
                global tokens
                tokens += 1
                await self.bot.get_guild(303307934774067210).get_channel(842931370695196682).send(
                    "Restart Initiated")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.id != 673737213959208980:
            return

        if after.status != discord.Status.offline:
            return

        global tokens
        if tokens > 0:
            tokens -= 1
            return

        await self.bot.get_guild(303307934774067210).get_channel(842931370695196682).send(
            "Bot just went offline <@!122739797646245899>,<@!125660719323676672>")
