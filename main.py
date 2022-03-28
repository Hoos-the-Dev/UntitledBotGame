#Apartment by Aurora Rpg

from urllib import response
import nextcord
from nextcord import Member
from nextcord.ext import commands
from nextcord.ext.commands import Bot, has_permissions, MissingPermissions
import asyncio
import requests
import json
import os
from nextcord import Interaction
import aiohttp

bot = commands.Bot(command_prefix="-", case_insensitive=True)

intents = nextcord.Intents.default()
intents.members = True

from apikey import BOTTOKEN

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.do_not_disturb,
                              activity=nextcord.Streaming(
                                  name='Security Cam footage',
                                  url='https://twitch.tv/aurorarqg'))
    print("i am Running on " + bot.user.name)

@bot.command()
async def ping(ctx):
  embed = nextcord.Embed(title=":ping_pong: Pong", description=f"this took {round(bot.latency*1000)}ms to send")
  await ctx.reply(embed=embed)
  print("user has pinged")

initial_extensions = []

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
      initial_extensions.append("cogs." + filename[:-3])

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
      bot.load_extension(extension)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    embed = nextcord.Embed(title="???", description="The Command that you just tried to do doesnt even exist... Use -help for a list of commands that actually work instead of shit that doesnt.")
    await ctx.reply(embed=embed)

      
bot.run(BOTTOKEN)
