import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix=">")
data = json.loads(open("Points.json").read())
channel = 354019501865435137


def get_balance(id):
    id = str(id)
    if id not in data:
        data[id] = 0
    return data[id]


def change_balance(id, amount):
    get_balance(id)
    id = str(id)
    data[id] += amount


def get_leaderboard():
    leaderboard = dict(data)
    return sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)


def check_channel(ctx):
    return ctx.channel.id == channel


def save():
    with open("Points.json", "w") as da_file:
        da_file.write(json.dumps(data))


@bot.event
async def on_ready():
    global appli
    appli = await bot.application_info()
    print("Logged in! bot invite: https://discordapp.com/api/oauth2/authorize?client_id=" +
          str(appli.id) + "&permissions=0&scope=bot")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CheckFailure):
        return

    await ctx.send(error)


@bot.group(invoke_without_command=True)
@commands.check(check_channel)
async def points(ctx):
    """I usually have people pay for cracking me open like that"""
    await ctx.send("You have %d Science Points" % get_balance(ctx.author.id))


@points.command()
@commands.check(check_channel)
async def give(ctx, other: discord.Member, amount: int = 0):
    if amount == 0:
        await ctx.send("You really want to give nothing? How heartless")
        return
    if amount < 0:
        await ctx.send("You know stealing is wrong right?(and wouldn't be fun if i added it like that)")
        return
    if ctx.author == other:
        await ctx.send("You can't give yourself points silly")
        return
    if get_balance(ctx.author.id) < amount:
        await ctx.send("You don't have that much to give!")
        return
    change_balance(ctx.author.id, amount * -1)
    change_balance(other.id, amount)
    await ctx.send("Transaction successful!")
    save()


@commands.is_owner()
@points.command()
async def add(ctx, target: discord.Member, amount: int = 0):
    change_balance(target.id, amount)
    await ctx.send("Balance changed by %d!" % amount)
    save()


@points.command()
@commands.check(check_channel)
async def top(ctx):
    output = ""
    for thing in get_leaderboard():
        user = bot.get_user(int(thing[0]))
        display = ""
        if not hasattr(user, "nick"):
            display = user.display_name
        else:
            display = user.nick
        output += "%s : %d\n" % (display, thing[1])
    await ctx.send(output)


@commands.is_owner()
@bot.command()
@commands.check(check_channel)
async def repeat(ctx):
    stuff = ctx.message.content[8:]
    if stuff[0] == "\\":
        stuff = stuff[1:]
    await ctx.send(stuff)


bot.run(open("Token.txt").read())
