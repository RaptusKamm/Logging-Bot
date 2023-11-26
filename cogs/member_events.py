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

class member_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(c_parser.get('Channel', 'id'))
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
        title="Log - Join",
        description=f"A member joined the server!",
        color=discord.Color.from_rgb(0, 0, 153)
        )

        joined_at = datetime.now(pytz.timezone('Europe/Berlin'))
        acc_create = member.created_at

        embed.set_author(name= member.name, icon_url= member.display_avatar)
        embed.add_field(name=f"Name: ", value= f"{member.name} (ID: {member.id})", inline=False)
        embed.add_field(name=f"Time : ", value= f"{joined_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=False)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        embed.set_footer(text=f"Account created at: {acc_create.strftime('%d.%m.%Y %H:%M:%S')}")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
        title="Log - Left",
        description=f"A member left the server!",
        color=discord.Color.from_rgb(0, 128, 255)
        )

        left_at = datetime.now(pytz.timezone('Europe/Berlin'))
        acc_create = member.created_at

        embed.set_author(name= member.name, icon_url= member.display_avatar)
        embed.add_field(name=f"Name: ", value= f"{member.name} (ID: {member.id})", inline=False)
        embed.add_field(name=f"Time : ", value= f"{left_at.strftime('%d-%m-%Y %H:%M:%S')}", inline=False)

        embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
        embed.set_footer(text=f"Account created at: {acc_create.strftime('%d.%m.%Y %H:%M:%S')}")
        
        Settings.channel = self.bot.get_channel(Settings.get_channel_id())
        await Settings.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, old_inf, new_inf):
        nick_old = old_inf.nick
        nick_new = new_inf.nick
        name_old = old_inf.name
        name_new = new_inf.name
        
        embed = discord.Embed(
        title="Log - Nickname",
        description=f"A member changes his nickname!",
        color=discord.Color.from_rgb(0, 255, 128)
        )

        change = datetime.now(pytz.timezone('Europe/Berlin'))
        channel = self.bot.get_channel(self.channel_id)


        if name_new != name_old:
            embed.set_author(name= name_new, icon_url= new_inf.display_avatar)
            embed.add_field(name=f"Changed from: ", value= f"**{name_old}** to **{name_new}** (ID: {new_inf.id})", inline=False)

            embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
            embed.set_footer(text=f"Change completed on: {change.strftime('%d.%m.%Y %H:%M:%S')}")
            Settings.channel = self.bot.get_channel(Settings.get_channel_id())
            await Settings.channel.send(embed=embed)

        elif nick_new != nick_old:
            embed.set_author(name= nick_new, icon_url= new_inf.display_avatar)
            embed.add_field(name=f"Changed from: ", value= f"**{nick_old}** to **{nick_new}** (ID: {new_inf.id})", inline=False)

            embed.set_thumbnail(url="https://i.ibb.co/wykgrgV/logo-color.png")
            embed.set_footer(text=f"Change completed on: {change.strftime('%d.%m.%Y %H:%M:%S')}")
            Settings.channel = self.bot.get_channel(Settings.get_channel_id())
            await Settings.channel.send(embed=embed)
        ############################################################### Prüfen wegen username
        
        
def setup(bot):
    bot.add_cog(member_events(bot))