import discord
from discord.ext import commands
import json

channel_id = 354019501865435137


def check_channel(ctx):
    return ctx.channel.id == channel_id


class Chunii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.data = json.loads(open("Points.json").read())
        self.channel = None
        self.join_channel_id = 122051404582879233
        self.join_channel = None
        self.join_message = "https://imgur.com/dDl8jdb {.name}#{.discriminator} joined!"
        self.stuff = {}


    def get_balance(self, id):
        id = str(id)
        if id not in self.data:
            self.data[id] = 0
        return self.data[id]

    def change_balance(self, id, amount):
        self.get_balance(id)
        id = str(id)
        self.data[id] += amount

    def get_leaderboard(self):
        leaderboard = dict(self.data)
        return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)


    def save(self):
        with open("../Points.json", "w") as da_file:
            da_file.write(json.dumps(self.data))

    @commands.Cog.listener()
    async def on_ready(self):
        if not isinstance(self.join_channel, discord.abc.Snowflake):
            self.join_channel = await self.bot.fetch_channel(self.join_channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 122051404582879233:
            await self.join_channel.send(self.join_message.format(member, member))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.stuff and message.content == "NEW HOUR":
            await message.add_reaction(self.stuff[message.author.id])

    @commands.group(invoke_without_command=True)
    @commands.check(check_channel)
    async def points(self, ctx):
        """I usually have people pay for cracking me open like that"""
        await ctx.send("You have %d Science Points" % self.get_balance(ctx.author.id))

    @points.command()
    @commands.check(check_channel)
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

    @points.command(name="add")
    @commands.is_owner()
    async def points_add(self, ctx, target: discord.Member, amount: int = 0):
        self.change_balance(target.id, amount)
        await ctx.send("Balance changed by %d!" % amount)
        self.save()

    @points.command()
    @commands.check(check_channel)
    async def top(self, ctx, amount: int = 10, mode: str = "default"):
        if mode not in ["default", "all"]:
            mode = "default"
        output = ""
        leaderboard = self.get_leaderboard()
        for thing in leaderboard[:min(len(leaderboard), amount)]:
            user = self.bot.get_user(int(thing[0]))
            display = ""
            if not hasattr(user, "display_name"):
                if mode == "default":
                    continue
                if mode == "all":
                    display = "User left the server"
            elif not hasattr(user, "nick"):
                display = user.display_name
            else:
                display = user.nick
            output += "%s : %d\n" % (display, thing[1])
        await ctx.send(output or "No Entries, try a different amount")
