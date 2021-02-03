import discord
from discord.ext import commands
from tokenhdl import tokenHandler

bot = commands.Bot(command_prefix='>', description="A bot by nfq#1781")

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    print(f"--------\nLogged in as {bot.user.name} (ID:{str(bot.user.id)}') | Connected to {len(bot.users)} users")
    print("--------")
    print(f"Current Discord.py Version: {discord.__version__}")

@bot.listen()
async def on_message(message):
    return

bot.load_extension("cogs.examTable")
bot.load_extension("cogs.botBody")
bot.run(tokenHandler.readtoken())