import nextcord
from nextcord.ext import commands

class Math(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def add(self, ctx, num1: int, num2: int):
    await ctx.reply(num1 + num2)


  @commands.command()
  async def subtract(self, ctx, num1: int, num2: int):
    await ctx.reply(num1 - num2)


  @commands.command()
  async def multiply(self, ctx, num1: int, num2: int):
    await ctx.reply(num1 * num2)


  @commands.command()
  async def divide(self, ctx, num1: int, num2: int):
    await ctx.reply(num1 / num2)

def setup(bot):
    bot.add_cog(Math(bot))
 