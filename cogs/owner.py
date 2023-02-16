import imp
import nextcord
from nextcord import Embed, Member, SlashOption, Interaction, slash_command
from nextcord.ext import commands
from nextcord.ext.commands import Cog, command
import random
from random import randint
import resources.functions as func
import asyncio
import os
from dataclasses import dataclass, field
from lib import *
from resources.data import *
from resources.functions import *
from resources.ecofunc import *
from lib import console
import aiosqlite



class Owner(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  
  testServerId = 937841015648292934
  
  @nextcord.slash_command(name="maintenance", description=f"Maintenance commands")
  async def Maintenance(self, interaction:Interaction):
   pass

  @Maintenance.subcommand(name="restart", description=f"Restart bot")
  async def restart(self, interaction:Interaction):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("you ain't on the list of people who can do that sort of shit"); return

    embed = nextcord.Embed(description="Restarting...", color=nextcord.Color.green())    
    await interaction.send(embed=embed, delete_after=10)
    await self.bot.close()
    await os.system("python3 main.py")
    
  @Maintenance.subcommand(name="changestatus", description=f"Change bot status") 
  async def changestatus(self, interaction:Interaction, status: str=SlashOption(name="status", description="Status to change bot to", choices=["online", "idle", "dnd"]), activity: str=SlashOption(name="activity", description="Activity to change bot to", choices=["Streaming", 'Playing', "None", "Default", "slash_commands"]), activity_name: str=SlashOption(name="activity_name", description="Activity name to change bot to", required=False)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant change my status. tf?"); return
    if status == "online":
      if activity == "Streaming":
        await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=activity_name, url="https://www.twitch.tv/aurorapg"))
        await interaction.send("Changed status to online and activity to Streaming", ephemeral=True)
      elif activity == "Playing":
        await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game(name=activity_name))
        await interaction.send("Changed status to online and activity to Playing", ephemeral=True)
      elif activity == "None":
        await self.bot.change_presence(status=nextcord.Status.online)
        await interaction.send("Changed status to online and activity to None", ephemeral=True)
      elif activity == "Default":
        await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name=f"currently in {len(self.bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))
        await interaction.send("Changed status to `Online` and activity to `Default Status`", ephemeral=True)
      elif activity == "slash_commands":
        await self.bot.def2
        await interaction.send("Changed status to `Online` and activity to `Slash Commands`", ephemeral=True)
    elif status == "idle":
        if activity == "Streaming":
          await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Streaming(name=activity_name, url="https://www.twitch.tv/aurorapg"))
          await interaction.send("Changed status to idle and activity to Streaming", ephemeral=True)
        elif activity == "Playing":
          await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game(name=activity_name))
          await interaction.send("Changed status to idle and activity to Playing", ephemeral=True)
        elif activity == "None":
          await self.bot.change_presence(status=nextcord.Status.idle)
          await interaction.send("Changed status to idle and activity to None", ephemeral=True)
        elif activity == "Default":
          await self.bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Streaming(name=f"currently in {len(self.bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))
          await interaction.send("Changed status to `Idle` and activity to `Default Status`", ephemeral=True)
        elif activity == "slash_commands":
          await self.bot.idledef2
          await interaction.send("Changed status to `Idle` and activity to `Slash Commands`", ephemeral=True)
    elif status == "dnd":
      if activity == "Streaming":
        await self.bot.change_presence(status=nextcord.Status.do_not_disturb, activity=nextcord.Streaming(name=activity_name, url="https://www.twitch.tv/aurorapg"))
        await interaction.send("Changed status to dnd and activity to Streaming", ephemeral=True)  
      elif activity == "Playing":
        await self.bot.change_presence(status=nextcord.Status.do_not_disturb, activity=nextcord.Game(name=activity_name))
        await interaction.send("Changed status to dnd and activity to Playing", ephemeral=True) 
      elif activity == "None":
        await self.bot.change_presence(status=nextcord.Status.do_not_disturb)
        await interaction.send("Changed status to dnd and activity to None", ephemeral=True)
      elif activity == "Default":
        await self.bot.change_presence(status=nextcord.Status.do_not_disturb, activity=nextcord.Streaming(name=f"currently in {len(self.bot.guilds)} servers", url="https://twitch.tv/aurorarpg"))
        await interaction.send("Changed status to `DND` and activity to `Default Status`", ephemeral=True)
      elif activity == "slash_commands":
        await self.bot.dnddef2
        await interaction.send("Changed status to `DND` and activity to `Slash Commands`", ephemeral=True)

  @Maintenance.subcommand(name="leaveguild", description=f"Leave a guild")
  async def leaveguild(self, interaction:Interaction, guild_id: str=SlashOption(name="guild_id", description="Guild ID to leave", required=True)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
    guild = self.bot.get_guild(int(guild_id))
    await guild.leave()
    await interaction.send(f"left {guild.name}")

  @Maintenance.subcommand(name="guilds", description="Gives you a list of all the guilds the bot is in")
  async def guilds(self, interaction:Interaction):
    guilds = []
    for guild in self.bot.guilds:
      guilds.append(f"{guild.name} ({guild.id})")
    guilds = "\n".join(guilds)
    embed = nextcord.Embed(title="Guilds", description=f"{guilds}", color=nextcord.Color.random())
    func.B_SetEmbedAuthor(embed, interaction.user, True)
    await interaction.send(embed=embed, ephemeral=True)

  @Maintenance.subcommand(name="guildnum", description="Gives you the number of guilds the bot is in")
  async def guildnum(self, interaction:Interaction):
    guildnum = len(self.bot.guilds)
    embed = nextcord.Embed(title="Guilds", description=f"{guildnum}", color=nextcord.Color.random())
    func.B_SetEmbedAuthor(embed, interaction.user, True)
    await interaction.send(embed=embed, ephemeral=True)

  @Maintenance.subcommand(name="reload", description="Reloads a cog")
  async def reload(self, interaction:Interaction, cog: str=SlashOption(name="cog", description="Cog to reload", required=True)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
    try:
      self.bot.unload_extension(f"cogs.{cog}")
      self.bot.load_extension(f"cogs.{cog}")
      embed = nextcord.Embed(title="Reloaded", description=f"`cogs.{cog}` was reloaded", color=nextcord.Color.green())
      await interaction.send(embed=embed)
      print(f"Reloaded cogs.{cog}")
    except Exception as e:
      error = nextcord.Embed(title=f"Encountered an Error whilst reloading `cogs.{cog}`", description=f"{e}", color=nextcord.Color.red())
      await interaction.send(embed=error)
  # @Maintenance.subcommand(name="reloadall", description="Reloads all cogs")
  # async def reloadall(self, interaction:Interaction):
  #   if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
  #   for cog in self.bot.cogs:
  #     try:
  #       self.bot.unload_extension(f"cogs.{cog}")
  #       self.bot.load_extension(f"cogs.{cog}")
  #       print(f"Reloaded all cogs")
  #     except Exception as e:
  #       error = nextcord.Embed(title=f"Encountered an Error whilst reloading `cogs.{cog}`", description=f"{e}", color=nextcord.Color.red())
  #       await interaction.send(embed=error)
  #   embed = nextcord.Embed(title="Reloaded", description="All cogs were reloaded", color=nextcord.Color.green())
  #   await interaction.send(embed=embed)
  @Maintenance.subcommand(name="unload", description="Unloads a cog")
  async def unload(self, interaction:Interaction, cog: str=SlashOption(name="cog", description="Cog to unload", required=True)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
    if cog == "owner": await interaction.send(f"Think about what you just tried to do {interaction.user.mention}."); return
    try:
      self.bot.unload_extension(f"cogs.{cog}")
      embed = nextcord.Embed(title="Unloaded", description=f"`cogs.{cog}` was unloaded", color=nextcord.Color.green())
      await interaction.send(embed=embed)
      print(f"Unloaded cogs.{cog}")
    except Exception as e:
      error = nextcord.Embed(title=f"Encountered an Error whilst unloading `cogs.{cog}`", description=f"{e}", color=nextcord.Color.red())
      await interaction.send(embed=error)
  @Maintenance.subcommand(name="load", description="Loads a cog")
  async def load(self, interaction:Interaction, cog: str=SlashOption(name="cog", description="Cog to load", required=True)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
    try:
      self.bot.load_extension(f"cogs.{cog}")
      embed = nextcord.Embed(title="Loaded", description=f"`cogs.{cog}` was loaded", color=nextcord.Color.green())
      await interaction.send(embed=embed)
      print(f"Loaded cogs.{cog}")
    except Exception as e:
      error = nextcord.Embed(title=f"Encountered an Error whilst loading `cogs.{cog}`", description=f"{e}", color=nextcord.Color.red())
      await interaction.send(embed=error)
  @slash_command(name='broadcast', description='Broadcasts a message to all guilds the bot is in')
  async def broadcast(self, interaction:Interaction, message: str=SlashOption(name="message", description="Message to broadcast", required=True), embed: bool=SlashOption(name="embed", description="Whether to send the message as an embed or not", required=False)):
    if func.B_IsMemberOwner(self, interaction.user) == False: await interaction.send("no you cant do that. tf?"); return
    for guild in self.bot.guilds:
      try:
          bembed = nextcord.Embed(title="Broadcast", description=f"{message}", color=nextcord.Color.random())
          bembed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
          if embed == True: await guild.system_channel.send(embed=bembed)
          else: await guild.system_channel.send(message)
      except:
        pass
    await interaction.send("Broadcasted message to all guilds")

  @commands.command(description="Logs a message to the console and shows log history")
  async def log(self, ctx, *, message=None):
    if func.B_IsMemberOwner(self, ctx.author) == False: await ctx.send("no you cant do that. tf?"); return
    if message == None:
      embed = nextcord.Embed(title="Logs", description="", color=nextcord.Color.random())
      for line in console.history:
        embed.description += f"`{line}\n`"
      await ctx.send(embed=embed)
    else:
      console.printf(message)
      embed = Embed(description="Logged message", color=nextcord.Color.green())
      await ctx.send(embed=embed)

  @commands.command(name="spam", description="Spams a user in all guilds the bot is in")
  async def spam_ping(self, ctx, member: nextcord.Member):
    if func.B_IsMemberOwner(self, ctx.author) == False: await ctx.send("who are you? :thinking:"); return
    pinge = self.bot.get_user(member.id)
    msg = [f"what does dis button do? {pinge.mention}", f"you did this to yourself {pinge.mention}", f"that mass ping was so uncalled for {pinge.mention}", f"Bingus >>> Clark {pinge.mention}", f"why do you have to be a better coder than me {pinge.mention}", f"men {pinge.mention}", f"find your wings {pinge.mention}", f"`what are you going to recode the ping all command?` {pinge.mention}", f"you love to play games {pinge.mention}"]
    for guild in self.bot.guilds:
      if pinge in guild.members:
        for channel in guild.channels:
          try:
            await channel.send(random.choice(msg))
          except:
            pass
    print("pinged!")
    
  @command(description="Maintenance mode toggle")
  async def wip(self, ctx: commands.Context, message=None):
    self.maintenance = json.load(open('resources/data/wip.json', 'r'))
    if message == "status":
      if "True" in self.maintenance:
        embed = Embed(title="Maintenance mode", description=f"{self.bot.user.name} is in maintenance mode", color=nextcord.Color.red())
        await ctx.reply(embed=embed)
      elif "False" in self.maintenance:
        embed = Embed(title="Maintenance mode", description=f"{self.bot.user.name} is not in maintenance mode", color=nextcord.Color.green())
        await ctx.reply(embed=embed)
      return
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    if "True" in self.maintenance:
      self.maintenance.pop('True')
      self.maintenance['False'] = "Open bot"
      json.dump(self.maintenance, open('resources/data/wip.json', 'w'))
      embed = Embed(title="Aaaaand we're back", description=f"{self.bot.user.name} is out of maintenance mode", color=nextcord.Color.green())
      await ctx.reply(embed=embed)
    elif "False" in self.maintenance:
      self.maintenance.pop('False')
      self.maintenance['True'] = "bongo now in maintenance mode"
      json.dump(self.maintenance, open('resources/data/wip.json', 'w'))
      embed = Embed(title="We'll be back soon folks (hopefully)", description=f"{self.bot.user.name} now in maintenance mode", color=nextcord.Color.red())
      await ctx.reply(embed=embed)
  
  @command(description="Loads all users to the database")
  async def load_all(self, ctx):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    for member in self.bot.users:
      async with self.db.cursor() as cursor:
          users = len(self.bot.users)
          await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (member.id,))
          data = await cursor.fetchone()
          if data is None:
              await create_balance(self, member)
              #print the number of the user in the list
              if member.bot == True:
                return
              for i in range(users):
                if member.id == self.bot.users[i].id:
                  console.info(f"Added {member.name}#{member.discriminator} to database [{i+1} / {users}]")
    await self.db.commit()
    await ctx.send(f"Loaded all users to database")
  
  @command(description="Wipe a user out of existence (to the database atleast)")
  async def wipe(self, ctx, member: nextcord.Member):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    async with self.db.cursor() as cursor:
      await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (member.id,))
      data = await cursor.fetchone()
      if data is None:
        await ctx.send("User not found in database")
        return
      else:
        await cursor.execute("DELETE FROM bank WHERE user = ?", (member.id,))
        em = Embed(description=f"Wiped <@{member.id}> from the database", color=nextcord.Color.green())
        await ctx.send(embed=em)
    await self.db.commit()
  
  @command(name="Bank Limit Increase [bli]", description="Increase the bank limit of a user", aliases=["bli"])
  async def bank_limit_increase(self, ctx, amount: int, member: nextcord.Member=None):
    if member == None:
      member = ctx.author
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    await update_maxbank(self, member, amount)
    maxbank = await get_maxbank(self, member)
    em = Embed(description=f"Set <@{member.id}>'s bank limit to {maxbank}", color=nextcord.Color.green())
    await ctx.send(embed=em)
    await self.db.commit()

  @command(name="Bank Limit Decrease [bld]", description="Decrease the bank limit of a user", aliases=["bld"])
  async def bank_limit_decrease(self, ctx, amount: int, member: nextcord.Member=None):
    if member == None:
      member = ctx.author
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    await update_maxbank(self, member, -amount)
    maxbank = await get_maxbank(self, member)
    em = Embed(description=f"Set <@{member.id}>'s bank limit {maxbank}", color=nextcord.Color.green())
    await ctx.send(embed=em)
    await self.db.commit()

  @command(aliases=["spawn"], description="Spawn money into your or someone else's wallet")
  async def spawn_cash(self, ctx: commands.Context, amount:int, user: nextcord.Member = None):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False:
      await ctx.send('smh, trying to inflate the economy')
      return
    if amount is None:
      await ctx.send("Please specify an amount")
      return
    if user is None:
      user = ctx.author
    await update_balance(self, user, amount)
    await ctx.send(f"Added {amount} to {user.name}'s balance")
  
  @command(description="raises all bank limits to a certain amount", aliases=["rabl"])
  async def raise_all_bank_limits(self, ctx, amount: int):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    for member in self.bot.users:
      print("pass")
      await update_maxbank(self, member, amount)
      print("passing the update bank limit")
      console.info(f"Set {member.name}#{member.discriminator}'s bank limit to {amount}")
    await ctx.send(f"Set all bank limits to {amount}")
    


  

    
def setup(bot):
    bot.add_cog(Owner(bot))
 