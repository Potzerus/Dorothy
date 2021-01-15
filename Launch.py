import asyncio

import cogs
from discord.ext import commands
import json

bot = commands.Bot(command_prefix=">")

reactions = {}
response_json = json.loads(open("responses.json").read())
join_message = ""
load_cogs = [
    # cogs.Drones,
    # cogs.Chunii,
    cogs.OdaCord
]
for cog in load_cogs:
    bot.add_cog(cog(bot))


def save():
    with open("responses.json", "w") as da_file:
        da_file.write(json.dumps(response_json))


def odacheck():
    async def predicate(ctx):
        return ctx.guild.id == 747340433398693959

    return commands.check(predicate)


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


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if not message.author.bot:
        for k, v in response_json.get(str(message.guild.id), {}).items():
            if k in message.content.lower():
                await message.channel.send(v)
                break


@bot.command()
@commands.is_owner()
async def react(ctx, id: int):
    await ctx.send("Which reaction?")
    try:
        reaction, auth = await bot.wait_for("reaction_add", check=lambda x, y: ctx.author.id == y.id, timeout=60)
        reactions[id] = reaction
        await ctx.send("Acknowledged")
    except asyncio.TimeoutError:
        await ctx.send("Timed out")


@bot.command()
@commands.is_owner()
async def repeat(ctx, *, stuff: str):
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
@commands.check_any(commands.has_permissions(manage_channels=True), odacheck())
async def responses_add(ctx, key: str, *, response: str):
    response_json.setdefault(str(ctx.guild.id), {})[key] = response
    await ctx.send("Add operation successful")
    save()


@responses.command(name="remove")
@commands.check_any(commands.has_permissions(manage_channels=True), odacheck())
async def responses_remove(ctx, *, key: str):
    response_json[str(ctx.guild.id)].pop(key)
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


@bot.command(name="leave")
@commands.is_owner()
async def _leave(ctx, server_id):
    target = await ctx.bot.fetch_guild(server_id)
    await target.leave()


bot.run(open("Token.txt").read())
