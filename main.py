#Apartment by Aurora Rpg

from urllib import response
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
import asyncio
import requests
import json
import os

bot = commands.Bot(command_prefix="-test ")

intents = discord.Intents.default()
intents.members = True

my_secret = os.environ['token']

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb,
                              activity=discord.Streaming(
                                  name='Security Cam footage',
                                  url='https://twitch.tv/aurorarqg'))
    print("i am Running on " + bot.user.name)


### Fun commands


@bot.command(pass_context=True)
async def dm(ctx, user: discord.User, *, message=None):
    if message == None:
        await ctx.send('You need to put a message')
    else:
        await user.send(message)
        await ctx.channel.purge(1)
        await ctx.send('DM Sent')
        await ctx.author.send(
            "this is purely a test to see if it can dm i guess" + str(user))


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.reply(":ping_pong: pong")
    print("user has pinged")


@bot.command(pass_context=True)
async def ptsd(ctx):
    await ctx.reply("https://tenor.com/view/owl-surprised-gif-11760566")
    await ctx.send("ive seen what gio sends")
    print("the trauma")


@bot.command(pass_context=True)
async def jaden(ctx):
    await ctx.reply("jaden")
    await ctx.send("please speak up")
    print("he be quiet")


@bot.command(pass_context=True)
async def nsfw(ctx):
    await ctx.reply(":japanese_goblin: Hoo does not approve.")
    print("user tried to be a sussy baka")


@bot.command(pass_context=True)
async def bing(ctx):
    await ctx.reply("bong")
    print("user has binged")


@bot.command(pass_context=True)
async def mine(ctx):
    await ctx.reply("you so Fuckin Precious When you smile")
    await ctx.reply("              okay                        ")
    await ctx.reply("ahh")
    await ctx.reply("Hit it From The Back And Drive You wild")
    await ctx.reply("Okay")
    await ctx.reply("Girl i lose my Self Up in those Eyes")


@bot.command(pass_context=True)
async def serverinfo(ctx):
    await ctx.reply("still no embed but heres the servers info")
    await ctx.reply(name="Name", value=ctx.message.server.name, inline=True)
    await ctx.reply(name="ID", value=ctx.message.server.id, inline=True)
    await ctx.reply(name="Roles",
                    value=len(ctx.message.server.roles),
                    inline=True)
    await ctx.reply(name="Members", value=len(ctx.message.server.members))


@bot.command(pass_context=True)
async def slopeintercrept(ctx, num1: int, num2: int, num3: int, num4: int):
    await ctx.reply(num1=num2(num3) + num4)


@bot.command(pass_context=True)
async def addwjaden(ctx):
    await ctx.reply("jaden cant be added to anything. not even relationships")


@bot.command(pass_context=True)
async def Hoo(ctx):
    await ctx.reply("Hoos that?")

@bot.command()
async def on_message(message):
    if "hi" in message.content:
     print("hrei")

initial_extensions = []

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
      initial_extensions.append("cogs." + filename[:-3])

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
      bot.load_extension(extension)



      
bot.run(token)
