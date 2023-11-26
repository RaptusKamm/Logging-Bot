import discord
from discord.ext import commands
import os
from datetime import datetime
import configparser
from cogs.channel_events import Settings
import pytz

c_parser = configparser.ConfigParser()  #configparser object
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/channel_config.ini") #Lesen der ini-Datei mit Token

class ban_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_timestamp = {}
        self.channel_id = int(c_parser.get('Channel', 'id'))
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        embed = discord.Embed(
        title="Log - Ban",
        description=f"A member was banned!",
        color=discord.Color.from_rgb(153, 0, 0)
        )

        embed.add_field(name=f"Name: ", value= f"{member.name}", inline=True)

        
        ban_entry = await guild.fetch_ban(discord.Object(id=int(member.id))) # Holt sich das Member-Objekt anhand der ID
        embed.add_field(name=f"Reason: ", value= f"{ban_entry.reason}", inline=True) # Durch das Member-Objekt ban reason abfrage

        self.ban_timestamp[member.id] = datetime.now(pytz.timezone('Europe/Berlin'))
        ban_time = self.ban_timestamp[member.id]
        embed.add_field(name=f"Time: ", value= f"Banned at {ban_time.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        embed = discord.Embed(
        title="Log - Unban",
        description=f"A member was unbanned!",
        color=discord.Color.from_rgb(0, 153, 0)
        )

        embed.add_field(name=f"Name: ", value= f"{member.name}", inline=True)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(ban_event(bot))