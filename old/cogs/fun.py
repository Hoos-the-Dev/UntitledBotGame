import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from urllib import response
from nextcord import Member
from nextcord.ext import commands
import asyncio
import requests
import random
import aiohttp

class Fun(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  testserverid = 937841015648292934  
  
  @commands.command()
  @commands.guild_only()  
  async def dm(self, ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
      await ctx.reply(f"You need to give me a message to send to {user}. But you should've known that already. dumbass")
    else:
      embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
      embed.add_field(name="Sent by", value=ctx.author)
      await user.send(embed=embed)
      await ctx.channel.purge(limit=1)
      await ctx.send(f'Delivered to {user}', delete_after=6)
  
  @dm.error
  async def dm_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply("You need to put a message to send. but you should've known that already dumbass.")
  
  
  @dm.error
  async def validuser_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply("You need to say a valid user to dm. but i thought that was obvious.")
          
  @commands.command()
  @commands.guild_only()
  async def anondm(self, ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
      await ctx.reply(f"You need to give me a message to send to {user}. But you should've known that already. dumbass")
    else:
      embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
      embed.add_field(name="Sent by", value="Bingus")
      await user.send(embed=embed)
      await ctx.channel.purge(limit=1)
      await ctx.send(f'Delivered to {user}', delete_after=6)

  @anondm.error
  async def dm_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply("You need to put a message to send. but that should've been a given.")
  
  
  @anondm.error
  async def validuser_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply("You need to say a valid user to dm. but i assumed that you knew that already.")

  @commands.command()
  async def feedfish(self, ctx):
    embed = nextcord.Embed(title="Yummy :fish:", description="You fed bingus some fish and Bingus starts to pur.")
    embed.set_footer(text="Thank you for the fish. ❤️")
    await ctx.reply(embed=embed)
    print("Yum")

  @commands.command()
  async def animeme(self, ctx):
      async with aiohttp.ClientSession() as cd:
          async with cd.get("https://www.reddit.com/r/animememes.json") as r:
              animememes = await r.json()
              embed = nextcord.Embed(title="here..", description="idk why u wanted this but ok", color=nextcord.Color.random())
              embed.set_image(url=animememes["data"]["children"][random.randint(0, 30)]["data"]["url"])
              embed.set_footer(text="fucking weeb")
              await ctx.reply(embed=embed)

  @commands.command()
  async def Rel(self, ctx):
      async with aiohttp.ClientSession() as cd:
          async with cd.get("https://www.reddit.com/user/Relevred.json") as r:
              animememes = await r.json()
              embed = nextcord.Embed(title="Here ya go", description="take this. might be interesting", color=nextcord.Color.random())
              embed.set_image(url=animememes["data"]["children"][random.randint(0, 30)]["data"]["url"])
              embed.set_footer(text="taken straight from the Relevred reddit")
              await ctx.reply(embed=embed)
    
def setup(bot):
    bot.add_cog(Fun(bot))
