from discord.ext import commands
from discord.ext.commands import Cog
import discord


class TestCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        msg = await (await self.bot.fetch_channel(784830212248436748)).fetch_message(841695007085166642)
        await msg.edit(content="boba tea")