import discord
from discord.ext import commands
import datetime
from asyncio import sleep

def token():
    tokenFile=open("token","r")
    return tokenFile.read()

bot = commands.Bot(command_prefix='>', description="A bot by nfq#1781")

@bot.command(brief="Pings the bot", description="Pings the bot, bot replies with pong. Useful for checking if bot is alive")
async def ping(ctx):
    await ctx.send('pong :ping_pong:')

@bot.command(brief="Shows server information", description="Shows the server information")
async def serverinfo(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(title="Error!", description=f"*{ctx.command}* command cannot be used in a DM", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=f"{ctx.guild.name}", description="", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at:%Y-%m-%d}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}".capitalize())
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    await ctx.send(embed=embed)

@bot.command(brief="Shows user information", description="Shows user information. If a user is not provided in the args, message author is assumed.")
async def userinfo(ctx, user: discord.Member = None):
    if not user:
        user = ctx.author

    embed = discord.Embed(title=f"{user}", description="", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="User server nick", value=f"{user.nick}")
    embed.add_field(name="User created at", value=f"{user.created_at:%Y-%m-%d}")
    embed.add_field(name="User joined server at", value=f"{user.joined_at:%Y-%m-%d}")
    embed.add_field(name="User top role", value=f"{user.top_role}")
    embed.add_field(name="User ID", value=f"{user.id}")
    embed.set_thumbnail(url=f"{user.avatar_url}")

    await ctx.send(embed=embed)

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="myself get coded"))
    print(f"--------\nLogged in as {bot.user.name} (ID:{str(bot.user.id)}') | Connected to {len(bot.users)} users")
    print("--------")
    print(f"Current Discord.py Version: {discord.__version__}")

@bot.listen()
async def on_message(message):
    return

bot.run(token())