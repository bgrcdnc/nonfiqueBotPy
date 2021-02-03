import discord
from discord.ext import commands

class examTable(commands.Cog):
    """A neat exam reminder I plan to develop"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Testing")
    async def addexam(self, ctx, year, name, date, time):
        return

def setup(bot):
    bot.add_cog(examTable(bot))