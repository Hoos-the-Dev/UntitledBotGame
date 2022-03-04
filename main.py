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

bot = commands.Bot(command_prefix="-test ")

intents = nextcord.Intents.default()
intents.members = True

token = os.environ['token']
from apikey import BOTTOKEN

@bot.event
async def on_ready():
    await bot.change_presence(status=nextcord.Status.do_not_disturb,
                              activity=nextcord.Streaming(
                                  name='Security Cam footage',
                                  url='https://twitch.tv/aurorarqg'))
    print("i am Running on " + bot.user.name)


### Fun commands


@bot.command()
async def dm(ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
        await ctx.send('You need to put a message')
    else:
        embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
        embed.add_field(name="Sent by", value=ctx.author)
        await user.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Delivered to {user}', delete_after=6)
        
@bot.command()
async def anondm(ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
        await ctx.send('You need to put a message')
    else:
        embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
        embed.add_field(name="Sent by", value="Bingus")
        await user.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Delivered to {user}', delete_after=6)

@bot.command()
async def ping(ctx):
    await ctx.reply(":ping_pong: pong")
    print("user has pinged")


@bot.command()
async def ptsd(ctx):
    await ctx.reply("https://tenor.com/view/owl-surprised-gif-11760566")
    await ctx.send("ive seen what gio sends")
    print("the trauma")
 



@bot.command()
async def jaden(ctx):
    await ctx.reply("jaden")
    await ctx.send("please speak up")
    print("he be quiet")


@bot.command()
async def nsfw(ctx):
    await ctx.reply(":japanese_goblin: Hoo does not approve.")
    print("user tried to be a sussy baka")


@bot.command(pass_context=True)
async def bing(ctx):
    await ctx.reply("bong")
    print("user has binged")


@bot.command()
async def serverinfo(ctx):
    await ctx.reply("still no embed but heres the servers info")
    await ctx.reply(name="Name", value=ctx.message.server.name, inline=True)
    await ctx.reply(name="ID", value=ctx.message.server.id, inline=True)
    await ctx.reply(name="Roles",
                    value=len(ctx.message.server.roles),
                    inline=True)
    await ctx.reply(name="Members", value=len(ctx.message.server.members))


@bot.command(pass_context=True)
async def Hoo(ctx):
    await ctx.reply("Hoos that?")

initial_extensions = []

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
      initial_extensions.append("cogs." + filename[:-3])

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
      bot.load_extension(extension)



      
bot.run(BOTTOKEN)
