import json

from discord.ext import commands
from discord.ext.commands import Cog
import discord


def is_oda(ctx):
    return ctx.author.id == 273988946264981506


class OdaCord(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.data = json.loads(open("Oda.json").read())

    def get_data(self, name, default=None):
        if default is not None:
            self.data.setdefault(name, default)
        return self.data[name]

    def get_balance(self, id):
        id = str(id)
        self.data.setdefault(id, dict())
        self.data[id].setdefault("odacoins", 0)
        return self.data[id]["odacoins"]

    def save(self):
        with open("Oda.json", "+w") as da_file:
            return da_file.write(json.dumps(self.data))

    def change_balance(self, id, amount):
        self.get_balance(id)
        id = str(id)
        self.data[id]["odacoins"] += amount
        self.save()

    def set_balance(self, id, amount):
        self.get_balance(id)
        id = str(id)
        self.data[id]["odacoins"] = amount
        self.save()

    def get_leaderboard(self):
        leaderboard = dict(self.data)
        return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    async def cog_check(self, ctx):
        if ctx.guild is not None and ctx.guild.id == 747340433398693959:
            return True
        else:
            return False

    @commands.group(aliases=["oc", "odacoin"], invoke_without_command=True)
    async def odacoins(self, ctx, target: discord.Member = None):
        if not target:
            target = ctx.author
        balance = self.get_balance(target.id)
        if target.id == 273988946264981506:
            balance = "∞"
        await ctx.send("{.name} has {} odacoins".format(target, balance))

    @odacoins.command(name="set")
    @commands.check(is_oda)
    async def coins_set(self, ctx, target: discord.Member = None, amount: int = 0):
        if target is None:
            target = ctx.author
        self.set_balance(target.id, amount)
        await ctx.send("Balance set to %d!" % amount)

    @odacoins.command(name="give", aliases=["add"])
    async def coins_give(self, ctx, other: discord.Member, amount: int = 0):
        if amount == 0:
            await ctx.send("You really do be out here giving nothing huh")
            return
        if amount < 0:
            await ctx.send("You know stealing is wrong right?")
            return
        if self.get_balance(ctx.author.id) < amount and ctx.author.id != 273988946264981506:
            await ctx.send("You don't have that much to give!")
            return
        self.change_balance(ctx.author.id, amount * -1)
        self.change_balance(other.id, amount)
        await ctx.send("Transaction successful!")

    @odacoins.command(name="take", aliases=["remove", "rem"])
    @commands.check(is_oda)
    async def coins_take(self, ctx, other: discord.Member, amount: int = 0):
        self.change_balance(other.id, amount * -1)
        self.change_balance(ctx.author.id, amount)
        await ctx.send("Took %d odacoins" % amount)

    @commands.group(invoke_without_command=True)
    async def bet(self, ctx, option=None):
        """Does nothing right now, one sec"""
        pass

    @bet.command(name="create")
    @commands.check(is_oda)
    async def bet_create(self, ctx, *options):
        bets = self.data["bets"]
        if len(bets) != 0:
            await ctx.send("A bet is still running")
        for option in options:
            pass

    @bet.command(name="end")
    @commands.check(is_oda)
    async def bet_end(self, ctx, winner: int):
        pass

    @commands.group(name="buy", invoke_without_command=True)
    async def buy(self, ctx):
        pass

    @buy.command(name="kekenickname", aliases=["kn", "kekenick"])
    async def keke_nickname(self, ctx, *, new_name: str):
        if self.get_balance(ctx.author.id) < 15 and ctx.author.id != 273988946264981506:
            await ctx.send("You don't have enough earnings!")
            return
        self.change_balance(ctx.author.id, -15)
        odacord = self.bot.get_guild(747340433398693959)
        keke = odacord.get_member(206203994786234368)
        await keke.edit(reason="%s bought it with Odacoins" % ctx.author.name, nick=new_name)
        await ctx.send("Transaction successful!")

    @commands.group(aliases=["bounties"], invoke_without_command=True)
    async def bounty(self, ctx):
        embed = discord.Embed(title="Current Bounties")
        bounties = self.get_data("bounties", [])
        for bounty in bounties:
            embed.add_field(name="%s: %s %s" % (bounty["name"], str(bounty["reward"]), "odacoins"), value=bounty[
                "description"], inline=False)
            if len(bounties) == 0:
                embed.description = "No Bounties!"

        await ctx.send(embed=embed)

    @bounty.command(name="create", aliases=["make", "issue"])
    @commands.check(is_oda)
    async def bounty_create(self, ctx, name: str, reward: int, *, description: str = "-"):
        """
        >bounty create Vibe 10 Have a good day or smthn idk
        >bounty create "Destroy Monke" 20 Perform the ultimate sacrifice, destroy monke once and for all
        """
        bounty = {
            "name": name,
            "reward": reward,
            "description": description
        }
        bounties = self.get_data("bounties", [])
        bounties.append(bounty)
        self.save()
        await ctx.send("Bounty Created!")

    @bounty.command(name="remove", aliases=["delete", "clear"])
    @commands.check(is_oda)
    async def bounty_remove(self, ctx, *, name: str):
        bounties = self.get_data("bounties", [])
        for i in range(len(bounties)):
            if bounties[i]["name"].lower() == name.lower():
                bounties.remove(bounties[i])
                await ctx.send("Successfully cleared Bounty")
                self.save()
                return
        await ctx.send("No Bounty with that name found")
