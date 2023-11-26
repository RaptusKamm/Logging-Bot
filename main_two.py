import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    embed = discord.Embed(title="Log - Message", description=f"Message was send from {ctx.author}", color=discord.Color.dark_blue())
    
    await ctx.respond(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    embed = discord.Embed(
        title="Log - Channel created",
        description=f"A new channel was created",
        color=discord.Color.dark_blue()
    )

    embed.add_field(name=f"Name: ", value= f"{channel.name}", inline=True)
    embed.add_field(name=f"Category: ", value= f"{channel.category}", inline=True)

    created_at = channel.created_at
    embed.add_field(name=f"Time: ", value= f"{created_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
    embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
    
    channel = bot.get_channel(1009072788147015770)
    await channel.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    embed = discord.Embed(
        title="Log - Channel deleted",
        description=f"A channel was deleted",
        color=discord.Color.dark_blue()
    )

    embed.add_field(name=f"Name: ", value= f"{channel.name}", inline=True)
    embed.add_field(name=f"Category: ", value= f"{channel.category}", inline=True)

    created_at = channel.created_at
    embed.add_field(name=f"Time: ", value= f"{created_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
    embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
    
    channel = bot.get_channel(1009072788147015770)
    await channel.send(embed=embed)


bot.run('MTEyMDczMjczNzQ4NjIwOTExNQ.GnF5Ki.qfF-LC7D3_AGEmIlwcv9oIL_a5GrzJdHQYGoUU')