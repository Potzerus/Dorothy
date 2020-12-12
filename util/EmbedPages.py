import discord
import asyncio


async def paginate(ctx, embeds):
    message = await ctx.send(embed=embeds[0])
    arrows = ["⬅", "➡"]
    for emote in arrows:
        await message.add_reaction(emote)
    index = 0

    def check(reaction, user):
        if str(reaction.emoji) not in arrows:
            return False
        return ctx.message.id == reaction.message.id and ctx.author.id == user.id

    try:
        while True:
            reaction, user = await ctx.bot.wait_for("reaction_add", check, timeout=60)
            if str(reaction.emoji) == "⬅":
                index = max(0, index - 1)
            if str(reaction.emoji) == "➡":
                index = min(index + 1, len(embeds) - 1)
            await message.edit(embed=embeds[index])
    except asyncio.TimeoutError:
        await ctx.send("Timed out!")
