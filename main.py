import discord
from discord.ext import commands
import os
import configparser
from datetime import datetime

c_parser = configparser.ConfigParser()  #configparser object
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/config.ini") #Lesen der ini-Datei mit Token

intents = discord.Intents.all() #Intents um Member Informationen abzurufen
intents.members = True

bot = commands.Bot(intents=intents) #Bot object

for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/cogs"): # In einer for-Schleife werden alle cogs im Ordner cogs durchgegangen
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
  print("""
 _                                                      _       
| |                                                    | |      
| |     ___   __ _  __ _  ___ _ __   _ __ ___  __ _  __| |_   _ 
| |    / _ \ / _` |/ _` |/ _ \ '__| | '__/ _ \/ _` |/ _` | | | |
| |___| (_) | (_| | (_| |  __/ |    | | |  __/ (_| | (_| | |_| |
\_____/\___/ \__, |\__, |\___|_|    |_|  \___|\__,_|\__,_|\__, |
              __/ | __/ |                                  __/ |
             |___/ |___/                                  |___/ 
----------------------------------------------------------------
        """)

bot.run(c_parser.get('Bot', 'token'))
