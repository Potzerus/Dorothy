import json

from discord.ext import commands
from discord.ext.commands import Cog
import discord

from oda import Data, Money, Item, Inventory

auth_ids = [
    273988946264981506,
    125660719323676672
]


def is_oda(ctx):
    return ctx.author.id == 273988946264981506


def is_authorized(ctx):
    return ctx.author.id in auth_ids


class OdaCord(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is not None and ctx.guild.id == 747340433398693959:
            return True
        else:
            return False

    @commands.group(aliases=["oc", "odacoin"], invoke_without_command=True)
    async def odacoins(self, ctx, target: discord.Member = None):
        if not target:
            target = ctx.author
        balance = Money.get_balance(target.id)
        if target.id == 273988946264981506:
            balance = "∞"
        await ctx.send("{.name} has {} odacoins".format(target, balance))

    @odacoins.command(name="set")
    @commands.check(is_oda)
    async def coins_set(self, ctx, target: discord.Member = None, amount: int = 0):
        if target is None:
            target = ctx.author
        Money.set_balance(target.id, amount)
        await ctx.send("Balance set to %d!" % amount)

    @odacoins.command(name="give", aliases=["add"])
    async def coins_give(self, ctx, other: discord.Member, amount: int = 0):
        if amount == 0:
            await ctx.send("You really do be out here giving nothing huh")
            return
        if amount < 0:
            await ctx.send("You know stealing is wrong right?")
            return
        if Money.get_balance(ctx.author.id) < amount and ctx.author.id != 273988946264981506:
            await ctx.send("You don't have that much to give!")
            return
        if not is_oda(ctx):
            Money.change_balance(ctx.author.id, amount * -1)
        Money.change_balance(other.id, amount)
        await ctx.send("Transaction successful!")

    @odacoins.command(name="take", aliases=["remove", "rem"])
    @commands.check(is_oda)
    async def coins_take(self, ctx, other: discord.Member, amount: int = 0):
        Money.change_balance(other.id, amount * -1)
        Money.change_balance(ctx.author.id, amount)
        await ctx.send("Took %d odacoins" % amount)

    @commands.group(name="buy", invoke_without_command=True)
    async def buy(self, ctx):
        pass

    @buy.command(name="kekenickname", aliases=["kn", "kekenick"])
    async def keke_nickname(self, ctx, *, new_name: str):
        if Money.get_balance(ctx.author.id) < 15 and ctx.author.id != 273988946264981506:
            await ctx.send("You don't have enough earnings!")
            return
        Money.change_balance(ctx.author.id, -15)
        odacord = self.bot.get_guild(747340433398693959)
        keke = odacord.get_member(206203994786234368)
        await keke.edit(reason="%s bought it with Odacoins" % ctx.author.name, nick=new_name)
        await ctx.send("Transaction successful!")

    @buy.command()
    async def ammo(self, ctx, amount: int = 1):
        price = Data.get("ammo-price", 100000000000000)
        if Money.get_balance(ctx.author.id) < price * amount and not is_oda(ctx):
            await ctx.send(f"You don't have enough earnings!\nYou need {price * amount}")
            return
        Money.change_balance(ctx.author.id, -price * amount)
        Inventory.give_resource(ctx.author.id, "Artillery-Ammo", amount)
        await ctx.send(f"Bought {amount} artillery ammo")

    @commands.group(aliases=["bounties"], invoke_without_command=True)
    async def bounty(self, ctx):
        embed = discord.Embed(title="Current Bounties")
        bounties = Data.get("bounties", [])
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
        bounties = Data.get("bounties", [])
        bounties.append(bounty)
        Data.save()
        await ctx.send("Bounty Created!")

    @bounty.command(name="remove", aliases=["delete", "clear"])
    @commands.check(is_oda)
    async def bounty_remove(self, ctx, *, name: str):
        bounties = Data.get("bounties", [])
        for i in range(len(bounties)):
            if bounties[i]["name"].lower() == name.lower():
                bounties.remove(bounties[i])
                await ctx.send("Successfully cleared Bounty")
                Data.save()
                return
        await ctx.send("No Bounty with that name found")

    @commands.command(aliases=["inv", "i"])
    async def inventory(self, ctx):

        inv = Inventory.get(ctx.author.id)
        output = discord.Embed(title="Inventory")
        output.description = ""
        for item, amount in inv.items():
            output.description = output.description + item
            if amount != 1:
                output.description = output.description + "x" + str(amount)
            output.description = output.description + "\n"

        if len(output.description) == 0:
            output.description = "Empty"
        await ctx.send(embed=output)

    @commands.group(invoke_without_command=True)
    async def status(self, ctx, target: discord.Member):
        status = Data.get_attribute(target.id, "status", [])
        await ctx.send(status)

    @status.command(name="apply")
    @commands.check(is_authorized)
    async def status_apply(self, ctx, condition: str, *, target: discord.Member):
        status = Data.get_attribute(target.id, "status", [])
        status.append(condition)
        Data.set_attribute(target.id, "status", status)
        await ctx.send("Application successful")

    @status.command(name="remove")
    @commands.check(is_authorized)
    async def status_remove(self, ctx, condition: str, *, target: discord.Member):
        status: list = Data.get_attribute(target.id, "status", [])
        status.remove(condition)
        Data.set_attribute(target.id,"status",status)
        await ctx.send("De-Application successful")

    @commands.group(invoke_without_command=True)
    async def artillery(self, ctx, target: discord.Member = None, shots: int = 1):
        if not Data.get_attribute(ctx.author.id, "artillery", False):
            await ctx.send("Clearly, you don't own any artillery")
            return
        if not target:
            ammo = "Artillery-Ammo"
            await ctx.send(f"Your artillery is ready to fire, you have {Inventory.get_resource(ctx.author.id, ammo)} shots!")

    @artillery.command()
    async def shoot(self, ctx):
        pass

    @commands.command()
    @commands.check(is_authorized)
    async def give(self, ctx, itemname, target: discord.Member = None, amount: int = 1):
        if target is None:
            target = ctx.author
        target = target.id
        if Inventory.give_resource(target, itemname, amount):
            await ctx.send("Success!")
            return
        else:
            await ctx.send("Epic Embed fail!")
            return
