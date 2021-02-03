import discord
from discord.ext import commands
import datetime

class body(commands.Cog):
    """Basic body of the bot""" 

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Pings the bot", description="Pings the bot, bot replies with pong. Useful for checking if bot is alive")
    async def ping(self, ctx):
        await ctx.send('pong :ping_pong:')

    @commands.command(brief="Shows server information", description="Shows the server information")
    async def serverinfo(self, ctx):
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

    @commands.command(brief="Shows user information", description="Shows user information. If a user is not provided in the args, message author is assumed.")
    async def userinfo(self, ctx, user: discord.Member = None):
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

def setup(bot):
    bot.add_cog(body(bot))