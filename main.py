#Bot by Derrick and Aiire


from sys import prefix
from urllib import response
import nextcord
from nextcord import Embed, Member, SlashOption
from nextcord.ext import commands, ipc
from nextcord.ext.commands import Bot, has_permissions, MissingPermissions
import asyncio
import requests
import json
import os
from nextcord import Interaction 
import aiohttp
import aiosqlite
from lib import console
import time
import random
from resources.iio import *



owners = {
   "Aiire" : 262417442209398784,
   "Derrick" : 164061868741099520
}

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            "help": "Shows help about the bot, a command, or a category",
            "aliases": ["h", "commands", "?"]
        })

    async def send_bot_help(self, mapping):
        embed = nextcord.Embed(title="Help", description="Here are all of my commands!", color=0x00ff00)
        for cog, commands in mapping.items():
            command_signatures = [f"`{c.name}`" for c in commands]
            if command_signatures:  
              cog_name = getattr(cog, "qualified_name", "No Category")
              if cog_name == "No Category":
                cog_name = "General"
              if cog_name == "Owner":
                if self.context.author.id in owners.values():
                  Dembed = Embed(title="Owner Commands", description="since you own the bot, your help command is special", color=0x00ff00)
                  for command in commands:
                    Dembed.add_field(name=command.name, value=command.description, inline=False)
                  Dembed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
                  await self.context.author.send(embed=Dembed)
                  await self.context.reply("Check your DMs! aswell")
                else:
                  pass
              if cog_name != "Owner":
                embed.add_field(name=cog_name, value=" ".join(command_signatures), inline=False)
              else:
                pass
        embed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = nextcord.Embed(title=cog.qualified_name, description=cog.description, color=0x00ff00)
        commands = cog.get_commands()
        for command in commands:
            embed.add_field(name=command.name, value=command.description, inline=False)
        embed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
        if cog.qualified_name == "Owner":
          if self.context.author.id in owners.values():
            await self.context.author.send(embed=embed)
            return
          else:
            await self.context.reply("you ain't got the answers sway")
            return
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = nextcord.Embed(title=command.name, description=command.description, color=0x00ff00)
        embed.add_field(name="Usage", value=f"`{command.name} {command.signature}`")
        embed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
        await self.get_destination().send(embed=embed)


console.info("Starting up...")
console.info("Loading cogs...")


# get prefix from config.db
async def get_prefix(guild_id):
    db = await aiosqlite.connect("config.db")
    cursor = await db.cursor()
    await cursor.execute("SELECT prefix FROM config WHERE guild_id = ?", (guild_id,))
    prefix = await cursor.fetchone()
    await cursor.close()
    await db.close()
    return prefix[0]


class DaBot(commands.Bot):
  version: str
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.ipc = ipc.Server(self,secret_key="secret")
  
  async def invoke(self, ctx: commands.Context):
    maintenance = json.load(open("resources/data/wip.json"))
    if ctx.command is None:
      return
    if ctx.command.name == "help":
      return await super().invoke(ctx)
    if ctx.command.name == "wip":
      return await super().invoke(ctx)
    if 'True' in maintenance:
      if ctx.author.id in owners.values():
        return await super().invoke(ctx)
      if ctx.author.id == bot.user.id:
        return await super().invoke(ctx)
      else:
        embed = Embed(title="I'm unavailable rn tbh", description="The bot is currently undergoing maintenance. Please try again later.", color=nextcord.Color.red())
        await ctx.send(embed=embed)
        return
    else:
     return await super().invoke(ctx)

  async def on_ready(self):
    console.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
    console.info(f"ID: {bot.user.id}")
    console.info(f"Prefix: {bot.command_prefix}")
    console.info(f"Loaded cogs: {len(bot.cogs)}")
    console.info(f"Loaded commands: {len(bot.commands)}")
    console.info("Ready!")
    console.info("                                                         ")
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=f"currently in {len(bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))
    print(f"Successfully logged in as {bot.user.name}, and Currently in {len(bot.guilds)} servers")

  async def on_ipc_ready(self):
    print("IPC Server is ready")

  async def on_ipc_error(self, endpoint ,error):
    print(endpoint, "raised", error)

bot = DaBot(command_prefix=["--","—"], case_insensitive=True, intents = nextcord.Intents.all(), help_command=HelpCommand())
bot.version = "2.5 / 3"

intents = nextcord.Intents.all()
intents.members = True

from resources.apikey import Tokens


bot.def2 = bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=f"Now using / commands!", url="https://twitch.tv/aurorarpg"))
bot.idledef2 = bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Streaming(name=f"Now using / commands!", url="https://twitch.tv/aurorarpg"))
bot.dnddef2 = bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Streaming(name=f"Now using / commands!", url="https://twitch.tv/aurorarpg"))

start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

@bot.event
async def on_slash_command_error(ctx, error):
    await ctx.send(f"An error occured: {error}")


@bot.event
async def on_interaction_error(interaction, error):
    await interaction.response.send_message(f"An error occured: {error}")



@bot.event
async def on_guild_join(guild: nextcord.Guild):
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=f"currently in {len(bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))
    embed = nextcord.Embed(title="Thank you for adding me to your server!")
    embed.add_field(name="How to use me", value="Simply type `/` and you will see a list of my commands in a menu.")
    embed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
    await guild.system_channel.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
  await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=f"currently in {len(bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))

@bot.ipc.route()
async def get_guild_count(data):
  return len(bot.guilds)

@bot.ipc.route()
async def get_guild_ids(data):
  final = []
  for guild in bot.guilds:
    final.append(guild.id)
  return final # returns the guild ids to the client

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        embed = nextcord.Embed(title="What the fuck did you just say?", description=f"{ctx.author.mention} The command you tried to use was not found. Please type `/` or '`{bot.command_prefix}help`' to see a list of my commands.")
        embed.set_footer(text=f"Dont embarass yourself again.", icon_url=bot.user.avatar)
        await ctx.send("That command does not exist!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I am missing permissions to use that command!")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = nextcord.Embed(title="Chill out!", description=f"{ctx.author.mention} You are on cooldown. Please wait `{error.retry_after:.2f}` seconds before trying again.", color=nextcord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
      embed = Embed(description="that member doesnt exist chief", color=nextcord.Color.red())
      await ctx.send(embed=embed)
    elif isinstance(error, commands.UserNotFound):
      embed = Embed(description="that user doesnt exist chief", color=nextcord.Color.red())
      await ctx.send(embed=embed)
    else:
        console.error(error)
        embed = nextcord.Embed(title="L ratio", description=f"{ctx.author.mention} An error occured while trying to run that command. Please try again later.")
        embed.set_footer(text=f"Error: {error}", icon_url=bot.user.avatar)
        await ctx.send(embed=embed)
        raise error

@bot.event
async def on_message_delete(message):
  if message.author == bot.user:
    return
  if message.guild is None:
    return
  if message.author.bot:
    return
  console.info(f"{message.author} deleted a message in {message.guild.name}.\nMessage: {message.content}")

@bot.event
async def on_message_edit(before, after):
  if before.author == bot.user: return
  if before.guild is None: return
  if before.author.bot: return
  if before.content == after.content: return
  console.info(f"{before.author} edited a message in {before.guild.name}.\nBefore: {before.content}\nAfter: {after.content}")




@bot.command()
async def serverinfo(ctx):
    embed = nextcord.Embed(title=f"Server Info for {ctx.guild.name}", description=f"We federal", color=0x00ff00)
    embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
    embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Created At", value=ctx.guild.created_at, inline=True)
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.set_footer(text=f"{bot.user.name} by Derrick And Aiire | {bot.version}", icon_url=bot.user.avatar)
    await ctx.send(embed=embed)     

@bot.slash_command(name="serverinfo", description="Shows info about the server")
async def slashserverinfo(interaction: Interaction):
    embed = nextcord.Embed(title=f"Server Info for {interaction.guild.name}", description=f"We federal", color=0x00ff00)
    embed.add_field(name="Owner", value=interaction.guild.owner, inline=True)
    embed.add_field(name="Members", value=interaction.guild.member_count, inline=True)
    embed.add_field(name="Roles", value=len(interaction.guild.roles), inline=True)
    embed.add_field(name="Channels", value=len(interaction.guild.channels), inline=True)
    embed.add_field(name="categories", value=len(interaction.guild.categories), inline=True)
    embed.set_footer(text=f"Server ID: {interaction.guild.id} | Created at: {interaction.guild.created_at}")
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
    await interaction.send(embed=embed)   

    

initial_extensions = []

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
      initial_extensions.append("cogs." + filename[:-3])

print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
      bot.load_extension(extension)
      console.info(f"Loaded {extension}")
    console.info("Loaded all cogs")

# @bot.event
# async def on_command_error(ctx, error):
  # if isinstance(error, commands.CommandNotFound):
    # embed = nextcord.Embed(title="???", description="The Command that you just tried to do doesnt even exist... Use -help for a list of commands that actually work instead of shit that doesnt.")
    # await ctx.reply(embed=embed)
bot.ipc.start()    
bot.run(Tokens.get('Spike'))


hello = "Hello World!"

match hello:
  case "Hello World!":
    print("Hello World!")
  case _:
    print("No match")