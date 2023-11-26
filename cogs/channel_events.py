import discord
from discord.ext import commands
import os
import configparser
from datetime import datetime
import pytz

intents = discord.Intents.all() #Intents um Member Informationen abzurufen
intents.members = True

bot = commands.Bot(intents=intents) #Bot object

c_parser = configparser.ConfigParser()  #configparser object
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/channel_config.ini") #Lesen der ini-Datei mit Token

class Settings:
    channel_id = int(c_parser.get('Channel', 'id'))

    @staticmethod
    def get_channel_id():
        return int(c_parser.get('Channel', 'id'))
    
    @staticmethod
    def set_channel_id(id):
        channel_id = id
        c_parser.set('Channel', 'id', str(id))
        with open(os.path.dirname(os.path.realpath(__file__))+"/channel_config.ini", 'w') as configfile:
            c_parser.write(configfile)

class channel_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(c_parser.get('Channel', 'id'))

        


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(
        title="Log - Channel created",
        description=f"A new channel was created",
        color=discord.Color.from_rgb(0, 204, 0)
        )

        embed.add_field(name=f"Name: ", value= f"{channel.name}", inline=True)
        embed.add_field(name=f"Category: ", value= f"{channel.category}", inline=True)

        created_at = datetime.now(pytz.timezone('Europe/Berlin'))
        embed.add_field(name=f"Time: ", value= f"{created_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(
        title="Log - Channel deleted",
        description=f"A channel was deleted",
        color=discord.Color.from_rgb(255 , 0, 0)
        )

        embed.add_field(name=f"Name: ", value= f"{channel.name}", inline=True)
        embed.add_field(name=f"Category: ", value= f"{channel.category}", inline=True)

        deleted_at = datetime.now(pytz.timezone('Europe/Berlin'))
        embed.add_field(name=f"Time: ", value= f"{deleted_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=True)
        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)

    @commands.slash_command(name="select_channel", description="Select the text channel to send all logs to.")
    async def select_logging(self, ctx, channel: discord.TextChannel):
        self.channel_id = channel.id
        Settings.set_channel_id(self.channel_id)
        
        await ctx.respond(f"Logging channel was set to {channel.name} - The channel was diretly updated.")


def setup(bot):
    bot.add_cog(channel_event(bot))
