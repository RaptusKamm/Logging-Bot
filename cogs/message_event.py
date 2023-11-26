import discord
from discord.ext import commands
import os
from datetime import datetime
import configparser
from cogs.channel_events import Settings
import pytz

c_parser = configparser.ConfigParser()  #configparser object
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/channel_config.ini") #Lesen der ini-Datei mit Token

intents = discord.Intents.default() #Intents um Member Informationen abzurufen
intents.members = True

bot = commands.Bot(intents=intents) #Bot object

class message_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(c_parser.get('Channel', 'id'))
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(
        title="Log - Message",
        description=f"A message was deleted!",
        color=discord.Color.from_rgb(102, 0, 0)
        )
        deleted_at = datetime.now(pytz.timezone('Europe/Berlin'))

        embed.add_field(name=f"Message from: ", value= f"{message.author}", inline=True)
        embed.add_field(name=f"Deleted on: ",  value= f"{deleted_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
        embed.add_field(name=f"Content of message: ", value= f"{message.content}", inline=False)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message_edit(self, old_msg, new_msg):
        embed = discord.Embed(
        title="Log - Message",
        description=f"A message has been changed!",
        color=discord.Color.from_rgb(204, 204, 0)
        )
        edited_at = datetime.now(pytz.timezone('Europe/Berlin'))

        embed.add_field(name=f"Message from: ", value= f"{new_msg.author}", inline=True)
        embed.add_field(name=f"Changed on: ", value= f"{edited_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
        embed.add_field(name=f"Content of message before: ", value= f"{old_msg.content}", inline=False)
        embed.add_field(name=f"Content of message after: ", value= f"{new_msg.content}", inline=False)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        if new_msg.content == old_msg.content:
            pass
        else:
            Settings.channel = self.bot.get_channel(Settings.get_channel_id())
            await Settings.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(message_events(bot))