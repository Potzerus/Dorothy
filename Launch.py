import asyncio

import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix=">")
data = json.loads(open("Points.json").read())
channel_id = 354019501865435137
channel = None
join_channel_id = 122051404582879233
join_channel = None
join_message = "https://imgur.com/dDl8jdb {.name}#{.discriminator} joined!"
stuff = {}
response_json = json.loads(open("responses.json").read())


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
    return ctx.channel.id == channel_id


def save():
    with open("Points.json", "w") as da_file:
        da_file.write(json.dumps(data))
    with open("responses.json", "w") as da_file:
        da_file.write(json.dumps(response_json))


@bot.event
async def on_ready():
    global appli
    appli = await bot.application_info()
    print("Logged in! bot invite: https://discordapp.com/api/oauth2/authorize?client_id=" +
          str(appli.id) + "&permissions=0&scope=bot")
    global join_channel
    if not isinstance(join_channel, discord.abc.Snowflake):
        join_channel = await bot.fetch_channel(join_channel_id)


@bot.event
async def on_member_join(member):
    if member.guild.id == 122051404582879233:
        await join_channel.send(join_message.format(member, member))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CheckFailure):
        return

    await ctx.send(error)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id in stuff and message.content == "NEW HOUR":
        await message.add_reaction(stuff[message.author.id])
    if not message.author.bot:
        for k, v in response_json.items():
            if k in message.content.lower():
                await message.channel.send(v)
                break


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


@points.command(name="add")
@commands.is_owner()
async def points_add(ctx, target: discord.Member, amount: int = 0):
    change_balance(target.id, amount)
    await ctx.send("Balance changed by %d!" % amount)
    save()


@points.command()
@commands.check(check_channel)
async def top(ctx, amount: int = 10, mode: str = "default"):
    if mode not in ["default", "all"]:
        mode = "default"
    output = ""
    leaderboard = get_leaderboard()
    for thing in leaderboard[:min(len(leaderboard), amount)]:
        user = bot.get_user(int(thing[0]))
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


@bot.command()
@commands.is_owner()
async def react(ctx, id: int):
    await ctx.send("Which reaction?")
    try:
        reaction, auth = await bot.wait_for("reaction_add", check=lambda x, y: ctx.author.id == y.id, timeout=60)
        stuff[id] = reaction
        await ctx.send("Acknowledged")
    except asyncio.TimeoutError:
        await ctx.send("Timed out")


@bot.command()
@commands.is_owner()
async def repeat(ctx):
    stuff = ctx.join_message.content[8:]
    if stuff[0] == "\\":
        stuff = stuff[1:]
    await ctx.send(stuff)


@bot.group(invoke_without_command=True)
@commands.is_owner()
async def responses(ctx):
    output = ""
    for k, v in response_json.items():
        output += "%s: %s\n\n" % (k, v)
    await ctx.send(output or "No responses set")


@responses.command(name="add")
@commands.is_owner()
async def responses_add(ctx, key: str, *, response: str):
    response_json[key] = response
    await ctx.send("Add operation successful")
    save()


@responses.command(name="remove")
@commands.is_owner()
async def responses_remove(ctx, *, key: str):
    response_json.pop(key)
    await ctx.send("Remove operation successful")
    save()


@bot.command()
@commands.is_owner()
async def set_join_message(ctx, *, arg: str):
    global join_message
    join_message = arg
    await ctx.send("New join join_message is {}".format(arg))


@bot.command(name="eval")
@commands.is_owner()
async def _eval(ctx, *, args: str):
    await ctx.send(eval(args))


bot.run(open("Token.txt").read())
