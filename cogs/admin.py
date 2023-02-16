from urllib import response
import nextcord
from nextcord import Embed, Member, SlashOption, Interaction
from nextcord.ext import commands, application_checks
from nextcord.ext.commands import Bot, has_permissions, MissingPermissions, command, Cog
import asyncio
import requests
import random
import humanfriendly
import datetime
from random import randint
import sqlite3
from resources.functions import *
from dataclasses import *
from lib import *
import json
import resources.functions as func

poll_file =  JSONData(file="polls.json", path="resources/data")
raffle_file = JSONData(file="raffles.json", path="resources/data")

@dataclass
class Poll:
    question: str
    options: list[str]
    votes: dict[int, list[nextcord.User]] = field(default_factory=dict)
    active: bool = True

    def __post_init__(self):
        self.id = random.randint(10000, 99999)
        if self.options is None:
            return

        self.options = [option.strip() for option in self.options]
        for i, option in enumerate(self.options):
            self.votes[i] = []
    
    def vote(self, user: nextcord.User, option: int|str) -> bool:
        if not self.active:
            return False

        option = self.index(option)
        if option is None:
            return False

        if user in self.votes[option]:
            return False

        self.votes[option].append(user)
        return True

    def results(self) -> int:
        if self.active is False:
            return -1
        
        results: dict[int, int] = {}
        for option, votes in self.votes.items():
            results[option] = len(votes)

        self.active = False
        return max(results, key=results.get)
    
    def index(self, option: int|str) -> int|str|None:
        if isinstance(option, int):
            if option < len(self.options):
                return self.options[option]
            
            return None
        
        if option in self.options:
            return self.options.index(option)
        
        return None

    def __int__(self) -> int:
        return self.id

class Admin(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  giotoggle = {
  }


  @nextcord.slash_command(name = "kick", description = "Kick user")
  @application_checks.has_permissions(kick_members=True)
  async def kick(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "user", description = "The user to kick", required=True), reason: str = SlashOption(name="reason", description="The reason for kicking, if any", required=False)):
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "kick", 188); return
    if self.bot.user.id == member.id: await interaction.send("What exactly made you think this was gonna work?"); return
    if B_IsMemberOwner(self, member): await interaction.send("He seems like such a nice guy tho..."); return
    if member.bot: await interaction.send("no kicking bots.", ephemeral=True); return

    if interaction.user.id == member.id:
      await interaction.send("https://cdn.vox-cdn.com/thumbor/mFiywP9BUHDC8AIRBDYJvXdfQiA=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23265504/Spider_Man_meme.jpg")
    else:
      output = nextcord.Embed(title="Adios :boot:", description=f"{member.mention} got kicked from the server, what an idiot. :joy_cat:", color=nextcord.Color.red())
      if reason == None: reason = "No reason given"
      output.add_field(name="Reason", value=reason)
      appeal = nextcord.Embed(title="Way to go", description=f"You got kicked from **{interaction.guild.name}**, come back when you're not as obnoxious as last time. :unamused:", color=nextcord.Color.red())
      appeal.add_field(name="Kicker", value=interaction.user.mention)
      appeal.add_field(name="Reason", value=reason)

      await interaction.send(embed=output)  
      await member.send(embed=appeal)
      await member.kick(reason=reason)

  @nextcord.slash_command(name = "ban", description = "Ban user") 
  @application_checks.has_permissions(ban_members=True) 
  async def ban(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "user", description = "The user to ban", required=True), reason: str = SlashOption(name = "reason", description = "The reason for banning, if any", required=False)):
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "ban", 188); return
    if self.bot.user.id == member.id: await interaction.send("Boggles my MIND how you thought that'd work LMFAO."); return
    if member.bot: await interaction.send("how dare you try to ban one of my fellow bots! :rage:"); return
    
    if interaction.user.id == member.id:
      await interaction.send("https://cdn.vox-cdn.com/thumbor/mFiywP9BUHDC8AIRBDYJvXdfQiA=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23265504/Spider_Man_meme.jpg")
    else:
      if reason == None: reason = "No reason given"
      output = nextcord.Embed(title="So long, gay Bowser!", description=f"{member.mention}'s dumbass got banned from the server :clown:", color=nextcord.Color.red())
      output.add_field(name="Reason", value=reason)
      appeal = nextcord.Embed(title="Uh Oh...", description=f'You were banned from **{interaction.guild.name}**', color=nextcord.Color.red())
      appeal.add_field(name="Banned by", value=interaction.user.mention)
      appeal.add_field(name="Reason", value=reason)
      await interaction.send(embed=output)
      await member.send(embed=appeal)
      await member.ban(reason=reason)
  
  @nextcord.slash_command(name = "timeout", description = "Timeout user")
  @application_checks.has_permissions(manage_guild=True) 
  async def timeout(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "user", description = "The user to timeout", required=True), time: str = SlashOption(name = "duration", description = "How long they should be timed out for", required=True), reason: str = SlashOption(name = "reason", description = "The reason for timing them out, if any", required=False)):
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "timeout", 187); return
    if self.bot.user.id == member.id: await interaction.send("Boggles my MIND how you thought that'd work LMFAO."); return
    if reason == None: reason = "No reason given"

    if interaction.user.id == member.id:
      await interaction.send("https://cdn.vox-cdn.com/thumbor/mFiywP9BUHDC8AIRBDYJvXdfQiA=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23265504/Spider_Man_meme.jpg")
    else:
      if B_IsMemberOwner(self, member): await interaction.send("no."); return
      embed = nextcord.Embed(title=f"stfu", description=f"Great job, {member.mention}, you got timed out by {interaction.user.mention}, you fucking clown", color=nextcord.Color.red())
      embed.add_field(name="Reason", value=reason)
      if "d" in time:
        if "1d" in time:
          time = str(time.replace("d", " day"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("d", " days"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "h" in time:
        if "1h" in time:
          time = str(time.replace("h", " hour"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("h", " hours"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "m" in time:
        if "1m" in time:
          time = str(time.replace("m", " minute"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("m", " minutes"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "s" in time:
        if "1s" in time:
          time = str(time.replace("s", " second"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("s", " seconds"))
          embed.add_field(name="Duration", value=f"{time}")
      time = humanfriendly.parse_timespan(time)
      if time == 0: 
        embed = nextcord.Embed(title=f"Welcome Back {member.name}", description="You are no longer in time out", color=nextcord.Color.green())
        await member.edit(timeout=None)
        await interaction.send(member.mention, embed=embed)
        return
      else:
        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
      await interaction.send(member.mention, embed=embed)

  @nextcord.slash_command(name="purge", description="Delete messages") 
  @application_checks.has_permissions(manage_messages=True)
  async def purge(self, interaction:Interaction, amount: int = SlashOption(name="limit", description="The number of messages to delete")):
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "purge", 188); return
    if amount <= 1:
      if amount == 1:
       await interaction.send("Could you not delete one single message yourself?")
      else:
       await interaction.send(f"Explain to me how I can delete {amount} messages")
    elif amount >= 100:
      if amount >= 1000:
        await interaction.send("Fuck all that shit, just delete the channel at this point")
      else:
        await interaction.send(f"yeah no, I'm not deleting {amount} goddamn messages")
    else:
      embed = nextcord.Embed(title='Boom! :bomb: :firecracker:', description=f'Deleted {amount} messages')
      B_SetEmbedAuthor(embed, interaction.user)
      await interaction.channel.purge(limit=amount)
      await interaction.send(embed=embed, delete_after=5)

  @nextcord.slash_command(name="feedback", description="feedback")  
  async def feedback(self, interaction:Interaction, message: str):
    Derrick = interaction.guild.get_member(164061868741099520)
    Aiire = interaction.guild.get_member(262417442209398784)
    await interaction.send(f"Thanks for your feedback, {interaction.user.name}!", ephemeral=True)
    embed = nextcord.Embed(title="You've got Mail! :incoming_envelope:", description=f"{interaction.user.name} has sent feedback!", color=nextcord.Color.random())
    embed.add_field(name="Feedback", value=message)
    await Derrick.send(embed=embed)
    await Aiire.send(embed=embed)
 
  @nextcord.slash_command(name="blacklist", description=f"Blacklist or un-blacklist user from administrator commands") 
  async def blacklist(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "user", description = "The user to blacklist/un-blacklist", required=True), option: str = SlashOption(name="action", description="Remove or add to blacklist", choices=["Add", "Remove"], required=True), reason: str = SlashOption(name = "reason", description = "The reason for blacklisting, if any", required=False)):
    if option == "Add":
      if B_CheckBlacklist(self, interaction.user) == True: await interaction.send("Why should I? You're blacklisted, remember?"); return
      if not B_IsMemberOwner(self, interaction.user): await interaction.send("the lion, the witch, and the audacity of this bitch"); return
      if interaction.user.id == member.id: await interaction.send("https://cdn.vox-cdn.com/thumbor/mFiywP9BUHDC8AIRBDYJvXdfQiA=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23265504/Spider_Man_meme.jpg"); return
      if B_IsMemberOwner(self, member): await interaction.send("i don't really feel like it"); return
      if self.bot.user.id == member.id: await interaction.send("Uh, I'm not going to blacklist myself 🤨", ephemeral=True); return
      if member.bot: await interaction.send("leave my fellow bots alone."); return
      
      if B_CheckBlacklist(self, member) == True: await interaction.send("That user is already blacklisted.", ephemeral=True); return

      blacklist[member.id] = member.mention
      embed = nextcord.Embed(title="Blacklisted!", description=f"You've been put on the **{self.bot.user.name}** blacklist!", color=nextcord.Color.red())
      if not reason == None:
        embed.add_field(name="Reason", value=reason)

      await interaction.send(member.mention, embed=embed)
    else:
      if B_CheckBlacklist(self, interaction.user) == True: await interaction.send("I'll pass"); return
      if not B_IsMemberOwner(self, interaction.user): await interaction.send("Last I checked, you didn't program me."); return
      if len(blacklist) == 0: await interaction.send("No one is currently blacklisted, and we'd like to keep it that way...", ephemeral=True); return
      if self.bot.user.id == member.id: await interaction.send("why on earth would i be on the blacklist", ephemeral=True); 
      if interaction.user.id == member.id: await interaction.send("If you really want to know, no, you're not blacklisted", ephemeral=True); return
      if member.bot: await interaction.send("Bots can't be blacklisted in the first place..."); return
      if B_CheckBlacklist(self, member) == False: await interaction.send("That user is not blacklisted.", ephemeral=True); return

      del blacklist[member.id]
      embed = nextcord.Embed(title="Delisted!", description=f"You've been removed from the **{self.bot.user.name}** blacklist...", color=nextcord.Color.green())
      await interaction.send(member.mention, embed=embed)

  @nextcord.slash_command(name="clearblacklist", description=f"Clear admin command blacklist") 
  async def clearblacklist(self, interaction:Interaction):
    if len(blacklist) == 0: await interaction.send("No users are blacklisted, as it should be.", ephemeral=True); return
    if not B_IsMemberOwner(self, interaction.user): await interaction.send("excuse me but who are you exactly???"); return
    if B_CheckBlacklist(self, interaction.user) == True: await interaction.send(":joy: no!!!"); return
    
    blacklist.clear()
    embed = nextcord.Embed(title="Screw it! ✂️", description=f"{interaction.user.mention} just cleared the admin blacklist!", color=nextcord.Color.green())
    await interaction.send(embed=embed)
 
  @nextcord.slash_command(name="viewblacklist", description=f"List users on admin command blacklist") 
  async def viewblacklist(self, interaction:Interaction):
    if B_CheckBlacklist(self, interaction.user) == True: await interaction.send("Imagine being blacklisted L + ratio.", ephemeral=True); return
    if not B_IsMemberOwner(self, interaction.user): await interaction.send("Ever heard of minding your own business?", ephemeral=True); return
    if len(blacklist) == 0: await interaction.send("No one is currently blacklisted, and we'd like to keep it that way...", ephemeral=True); return

    embed = nextcord.Embed(title=f"The Blacklist ✏️📜", description=B_DictToList(blacklist), color=nextcord.Color.random())
    embed.set_footer(text=f"Total - {len(blacklist)}")
    await interaction.send(embed=embed, ephemeral=True)

  # Give or take roles
  @nextcord.slash_command(name="role", description=f"Modify user roles")
  @application_checks.has_permissions(manage_roles=True)
  async def role(self, interaction:Interaction, option: str = SlashOption(name="action", description="Remove or add role", choices=["Give", "Take"]), member: nextcord.Member = SlashOption(description="user"), role: nextcord.Role = SlashOption(description="Role")):
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "role", 186); return
    
    embed = nextcord.Embed()
    if option == "Give":
      if role in member.roles: await interaction.send("pretty sure this user already has that role", ephemeral=True); return

      embed = nextcord.Embed(title="Role get!", description=f"{member.mention} now has the role {role.mention}", color=nextcord.Color.green())
      await member.add_roles(role)
    elif option == "Take":
      if not role in member.roles: await interaction.send("Uhm, they don't even have that role...", ephemeral=True); return
      
      embed = nextcord.Embed(title="Role robbed!", description=f"{member.mention} no longer has the role {role.mention}", color=nextcord.Color.red())
      await member.remove_roles(role)
    await interaction.send(embed=embed)


  
  @commands.command()
  async def hackrole(self, ctx, role: nextcord.Role=None, member: nextcord.Member=None):
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    if role == None:
        await ctx.reply("hey... you forgot to put a role")
        return
    elif member == None:
        await ctx.reply("you forgot to say whos getting the role")
        return
    await member.add_roles(role)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"aight {member.mention}, you now have the role **{role}**")

  @commands.command()
  async def unrole(self, ctx, role: nextcord.Role=None, member: nextcord.Member=None):
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    if role == None:
        await ctx.reply("hey... you forgot to put a role")
        return
    elif member == None:
        await ctx.reply("you forgot to say whos getting the role")
        return
    await member.remove_roles(role)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{member.mention}, poof goes the {role}")


  @commands.command()
  async def togglegiotrashtalk(self, ctx, message):
    self.giotoggle = json.load(open('giotoggle.json', 'r'))
    if B_IsMemberOwner(self, ctx.author) == False: await ctx.send("hahahah good one bucko"); return
    if message == "off":
      if "False" in self.giotoggle: await ctx.reply("Trash Talking <@365250952480948234> is already off"); return
      self.giotoggle.pop('True')
      self.giotoggle['False'] = "Lame ass"
      json.dump(self.giotoggle, open('giotoggle.json', 'w'))
      await ctx.reply("Trash Talking <@365250952480948234> has been turned off")
    elif message == 'on':
      if "True" in self.giotoggle: await ctx.reply("Trash Talking <@365250952480948234> is already on"); return
      self.giotoggle.pop('False')
      self.giotoggle["True"] = 'bingus will trash talk Flam'
      json.dump(self.giotoggle, open('giotoggle.json', 'w'))
      await ctx.reply('yay i get to shit talk gio again!')
    else:
      await ctx.reply(f'"{message}" doesnt make sense. get it together')
      print('LOOK AT THIS BULLSHIT:')
      print(f'{message} - {ctx.author}')


  #make unban command that pulls and unbans user using autocomplete
  @nextcord.slash_command(name="unban", description="Unban a user")
  @application_checks.has_permissions(ban_members=True)
  async def unban(self, interaction:Interaction, user: str=SlashOption(description="User to unban", autocomplete=True), usr: int=SlashOption(description="User to unban", autocomplete=True)):
    usr = str
    if B_CheckBlacklist(self, interaction.user) == True: await B_BlacklistEmbed(self, interaction, "unban", 186); return

    for ban in await interaction.guild.bans().flatten():
      if ban.user.name == user:
        usr = await interaction.guild.fetch_ban(ban.user)
        await interaction.guild.unban(usr.user)
        await interaction.send(f"{user} has been unbanned", ephemeral=True)


        print(user)
        break
    
    user = await self.bot.fetch_user(user)
  
      


        

    output = nextcord.Embed(title="Fingers crossed...", description=f"{user.mention} in now un-banned from this server, PRAY nothing goes wrong! :pray:", color=nextcord.Color.green())
    appeal = nextcord.Embed(title="Welcome back", description=f'You were previously banned from **{interaction.guild.name}**, but the ban hammer has been lifted and you may join back if you please!', color=nextcord.Color.green())
    await interaction.send(embed=output)
    try:
      await user.send(embed=appeal)
    except:
      pass
    await interaction.guild.unban(user)

  @unban.on_autocomplete("user")
  async def unban_list(self, interaction:Interaction, user:str = SlashOption(name="banlist", description="List of banned users")):
   bans = interaction.guild.bans()
   user = [f"{member.user.name}#{member.user.discriminator}" async for member in bans]
   await interaction.response.send_autocomplete(user)
   

  polls = {}
  poll_message = {}

  @commands.command(name="poll")
  async def poll(self, ctx: commands.Context, question: str, *options: str):
      if len(options) < 2:
          await ctx.send("You need at least 2 options to start a poll.")
          return

      poll = Poll(question, options)
      self.polls[int(poll)] = poll

      embed = nextcord.Embed(title="Poll", description=poll.question, color=nextcord.Color.blurple())
      embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
      for i, option in enumerate(poll.options):
          embed.add_field(name=f"{i+1}: {option}", value="\u200b", inline=False)
      embed.set_footer(text=f"Poll ID: {poll.id}")
    
      message = await ctx.send(embed=embed)
      for i in range(len(poll.options)):
          await message.add_reaction(f"{i+1}\N{COMBINING ENCLOSING KEYCAP}")
      self.poll_message[poll.id] = message




  @commands.command(name="endpoll")
  async def endpoll(self, ctx: commands.Context, poll_id: int):
      if poll_id not in self.polls:
          await ctx.send("That poll does not exist.")
          return


      poll = self.polls[poll_id]
      message = self.poll_message[poll_id]
      embed = message.embeds[0]
      embed.color = nextcord.Color.red()
      embed.title = "Poll Ended"
      embed.set_footer(text=f"Poll ID: {poll_id}")
      await message.edit(embed=embed)
      nembed= Embed(title=poll.question, description="**Results**:")
      await ctx.send(embed=nembed)
      self.polls.pop(poll_id)
      self.poll_message.pop(poll_id)
    
  @commands.command(name="polls")
  async def poll_list(self, ctx: commands.Context):
      if not self.polls:
          await ctx.send("There are no polls at the moment.")
          return

      embed = nextcord.Embed(title="Polls", color=nextcord.Color.blurple())
      for poll_id, poll in self.polls.items():
          embed.add_field(name=f"Poll ID: {poll_id}", value=poll.question, inline=False)
      await ctx.send(embed=embed)

  @commands.command()
  async def banlist(self, ctx):
    bans = await ctx.guild.bans()
    embed = nextcord.Embed(title="Banned Users", description="List of banned users", color=nextcord.Color.random())
    for ban in bans:
      embed.add_field(name=ban.usera.name, value=ban.user.id, inline=False)
    await ctx.send(embed=embed)

  @commands.command()
  async def member_count(self, ctx):
    guild = ctx.guild
    bots = len([member for member in guild.members if member.bot])
    members = len(guild.members) - bots
    embed = nextcord.Embed(title="Members", description="Amount of members", color=nextcord.Color.random())
    embed.add_field(name="Members:", value=members, inline=False)
    embed.add_field(name="Bots:", value=bots, inline=False)
    embed.add_field(name="Total Members:", value=len(guild.members), inline=False)
    await ctx.send(embed=embed)
    
    
  @nextcord.slash_command(name="embed", description="Send your message as an embed")
  @application_checks.has_permissions(manage_messages=True)
  async def embed(self, interaction:Interaction, title, message: str = SlashOption(name="message", description="The message to send", required=True), color: str = SlashOption(name="color", description="The color of the embed", choices=["Red", "Green", "Blue", "Purple", "Random"], required=True)):
    if color == "Red":
      embedcolor = nextcord.Color.red()
    elif color == "Green":
      embedcolor = nextcord.Color.green()
    elif color == "Blue":
      embedcolor = nextcord.Color.blue()
    elif color == "Purple":
      embedcolor = nextcord.Color.purple()
    elif color == "Random":
      embedcolor = nextcord.Color.random()
    embed = nextcord.Embed(title=title, description=message, color=embedcolor)
    func.B_SetEmbedAuthor(embed, interaction.user, False)
    await interaction.send(embed=embed)
  
  @commands.command(name="embed")
  async def embed_com(self, ctx):
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send("What would you like the title of the embed to be?")
    title = await self.bot.wait_for("message", check=check)
    await ctx.send("What would you like the message of the embed to be?")
    message = await self.bot.wait_for("message", check=check)
    if message.content == "cancel":
      await ctx.send("Cancelled")
      return
    if title.content == "cancel":
      await ctx.send("Cancelled")
      return
    if title.content == "none":
      title.content = None
    if message.content == "cancel" and title.content == "cancel":
      await ctx.send("Cancelled")
      return
    await ctx.send("What color would you like the embed to be? (Red, Green, Blue, Purple, Random)")
    color = await self.bot.wait_for("message", check=check)
    embedcolor = None
    if color.content == "Red":
      embedcolor = nextcord.Color.red()
    elif color.content == "Green":
      embedcolor = nextcord.Color.green()
    elif color.content == "Blue":
      embedcolor = nextcord.Color.blue()
    elif color.content == "Purple":
      embedcolor = nextcord.Color.purple()
    elif color.content == "Random":
      embedcolor = nextcord.Color.random()
    embed = nextcord.Embed(title=title.content, description=message.content, color=embedcolor)
    func.B_SetEmbedAuthor(embed, ctx.author, False)
    await ctx.send(embed=embed)

  
  @commands.command(name="kick")
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: nextcord.Member, *, reason=None):
    if reason == None:
      reason = "No reason provided"
    if member == ctx.author:
      await ctx.send("You can't kick yourself")
      return
    if member == self.bot.user:
      await ctx.send("so like, wanna rethink that?")
      return
    DEmbed = nextcord.Embed(title="Kicked", description=f"You have been kicked from {ctx.guild.name} for {reason}", color=nextcord.Color.red())
    await member.send(embed=DEmbed)
    embed = nextcord.Embed(title="Kicked", description=f"{member.mention} has been kicked for **{reason}**", color=nextcord.Color.red())
    await member.kick(reason=reason)
    await ctx.send(embed=embed)
  
  @commands.command(name="ban")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: nextcord.Member, *, reason=None):
    if reason == None:
      reason = "No reason provided"
    if member == ctx.author:
      await ctx.send("You can't ban yourself")
      return
    if member == self.bot.user:
      await ctx.send("im lost for words")
      return
    DEmbed = nextcord.Embed(title="Banned", description=f"You have been banned from {ctx.guild.name} for **{reason}**", color=nextcord.Color.red())
    await member.send(embed=DEmbed)
    embed = nextcord.Embed(title="Banned", description=f"{member.mention} has been banned for {reason}", color=nextcord.Color.red())
    await member.ban(reason=reason)
    await ctx.send(embed=embed)

  @commands.command(name="unban")
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
      user = ban_entry.user
      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        embed = nextcord.Embed(title="Unbanned", description=f"{user.mention} has been unbanned", color=nextcord.Color.green())
        await ctx.send(embed=embed)
        return

  @commands.command(name="purge")
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, amount: int):
    if amount > 100:
      await ctx.send("You can only purge up to 100 messages");return
    if amount < 1:
      await ctx.send("how the fuck am i doing that one chief");return
    if amount == 1:
      await ctx.send("im not doing that *lazy fuck*"); return
    if amount > 1000:
      await ctx.send("delete the channel at that point");return
    if amount > 10000:
      await ctx.send("again, delete the channel");return
    await ctx.channel.purge(limit=amount)
    embed = nextcord.Embed(title="Purged", description=f"{amount} messages have been purged", color=nextcord.Color.green())
    await ctx.send(embed=embed)
  
  @command(name = "Mute", description = "Mute a user", aliases = ["timeout"])
  @has_permissions(manage_messages=True)
  async def timeout(self, ctx, member: nextcord.Member, time: str, reason: str = None):
    if B_CheckBlacklist(self, ctx.user) == True: await B_BlacklistEmbed(self, ctx, "timeout", 187); return
    if self.bot.user.id == member.id: await ctx.send("Boggles my MIND how you thought that'd work LMFAO."); return
    if reason == None: reason = "No reason given"

    if ctx.user.id == member.id:
      await ctx.send("https://cdn.vox-cdn.com/thumbor/mFiywP9BUHDC8AIRBDYJvXdfQiA=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/23265504/Spider_Man_meme.jpg")
    else:
      if B_IsMemberOwner(self, member): await ctx.send("no."); return
      embed = nextcord.Embed(title=f"stfu", description=f"Great job, {member.mention}, you got timed out by {ctx.author.mention}, you fucking clown", color=nextcord.Color.red())
      embed.add_field(name="Reason", value=reason)
      if "d" in time:
        if "1d" in time:
          time = str(time.replace("d", " day"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("d", " days"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "h" in time:
        if "1h" in time:
          time = str(time.replace("h", " hour"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("h", " hours"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "m" in time:
        if "1m" in time:
          time = str(time.replace("m", " minute"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("m", " minutes"))
          embed.add_field(name="Duration", value=f"{time}")
      elif "s" in time:
        if "1s" in time:
          time = str(time.replace("s", " second"))
          embed.add_field(name="Duration", value=f"{time}")
        else:
          time = str(time.replace("s", " seconds"))
          embed.add_field(name="Duration", value=f"{time}")
      time = humanfriendly.parse_timespan(time)
      await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time))
      await ctx.send(member.mention, embed=embed)

  @command(name = "Unmute", description = "Unmute a user", aliases = ["untimeout"])
  @has_permissions(manage_messages=True)
  async def untimeout(self, ctx, member: nextcord.Member):
    embed = Embed(title="gg wp wb", description=f"{member.mention} has been unmuted by {ctx.author.mention}", color=nextcord.Color.green())
    await member.edit(timeout=None)
    await ctx.send(embed=embed)

  raffles = {}

  @command(name="raffle", description="start a raffle", aliases=["giveaway"])
  @has_permissions(manage_messages=True)
  async def raffle(self, ctx: commands.Context, time: str, *, prize: str):
    id = randint(10000, 100000)
    embed = nextcord.Embed(title="Raffle Ended", description=f"React with 🎉 to enter the raffle for", color=nextcord.Color.green())
    embed.add_field(name="Prize:", value=f"{prize}", inline=True)
    embed.add_field(name="Duration:", value=f"{time}", inline=True)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    self.raffles[id] = {"msg_id": msg.id,"time": time, "prize": prize, "host": ctx.author.id, "message_channel": ctx.channel.id}
    print(self.raffles)
    await asyncio.sleep(humanfriendly.parse_timespan(time))
    if id not in self.raffles: return
    new_msg = await ctx.channel.fetch_message(msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))
    winner = random.choice(users)
    msg = await ctx.channel.fetch_message(msg.id)
    await ctx.send(f"Congratulations {winner.mention}, you won {prize}!")
    embed = nextcord.Embed(title="Raffle Ended", description=f"React with 🎉 to enter the raffle for", color=nextcord.Color.red())
    embed.add_field(name="Prize:", value=f"{prize}", inline=True)
    embed.add_field(name="Duration:", value=f"{time}", inline=True)
    embed.add_field(name="Winner:", value=f"{winner.mention}", inline=True)
    nembed = nextcord.Embed(title="Raffle Ended", description=f"The raffle for **{prize}** has ended and the winner is \n\n{winner.mention}", color=nextcord.Color.random())
    await msg.edit(embed=embed)

  @command(name="endraffle", description="end a raffle", aliases=["endgiveaway"])
  @has_permissions(manage_messages=True)
  async def endraffle(self, ctx: commands.Context, message_id: int):
    if B_CheckBlacklist(self, ctx.author) == True: await B_BlacklistEmbed(self, ctx, "endraffle", 187); return
    raffle = self.raffles
    try:
      msg = await ctx.channel.fetch_message(raffle[message_id]["msg_id"])
    except:
      await ctx.send("Invalid message ID")
      return
    users = await msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))
    winner = random.choice(users)
    prize = raffle[message_id]["prize"]
    nembed = nextcord.Embed(title="Raffle Ended", description=f"React with 🎉 to enter the raffle for", color=nextcord.Color.red())
    nembed.add_field(name="Prize:", value=f"{prize}", inline=True)
    nembed.add_field(name="Duration:", value=f"{raffle[message_id]['time']}", inline=True)
    nembed.add_field(name="Winner:", value=f"{winner.mention}", inline=True)
    embed = nextcord.Embed(title="Raffle Ended", description=f"Congratulations {winner.mention}, you won {prize}!", color=nextcord.Color.random())
    embed.add_field(name="Duration", value=f"{raffle[message_id]['time']}")
    embed.set_footer(text=f"Hosted by {ctx.author.name} | ID: {message_id}")
    await msg.edit(winner.mention, embed=embed)
    await ctx.send
    del self.raffles[message_id]
  
  @command(name="reset", description="reset the channel, full blown restart")
  @has_permissions(manage_messages=True)
  async def reset(self, ctx: commands.Context):
    if B_CheckBlacklist(self, ctx.author) == True: await B_BlacklistEmbed(self, ctx, "reset", 187); return
    embed = Embed(title=":warning: Warning :warning:", description="Are you sure you want to reset the channel? This will delete the channel and create a new one in its absence.\n\nYou will have 5 seconds to decide if you want to go through with this", color=nextcord.Color.red())
    embed.set_footer(text="Are you sure you want to do this? This action cannot be undone.")
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    def check(reaction, user):
      return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]
    try:
      reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
    except asyncio.TimeoutError:
      await ctx.send("Timed out.")
    else:
      try:
        if str(reaction.emoji) == "✅":
          description = ctx.channel.topic
          channel_type = ctx.channel.type
          await ctx.guild.create_text_channel(ctx.channel.name)
          channel = ctx.guild.get_channel(ctx.channel.id)
          await channel.edit(topic=description)
          await channel.edit(type=channel_type)
          await channel.edit(position=ctx.channel.position)
          await ctx.channel.delete()

          await channel.send("its as if none of that ever happened")
      except Exception as e:
        await channel.send(f"Error: {e}")
      else:
        await ctx.send("Cancelled.")

  @command(name="Random Number Generator [RNG]", description="Generate a random number between 2 numbers", aliases=["rng"])
  async def rng(self, ctx: commands.Context, min: int, max: int):
    if B_CheckBlacklist(self, ctx.author) == True: await B_BlacklistEmbed(self, ctx, "rng", 187); return
    embed = Embed(title="Random Number Generator", description="Generating a random number between 2 numbers", color=nextcord.Color.random())
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    number = random.randint(min, max)
    embed = Embed(title="Random Number Generator", description=f"Your random number is {number}", color=nextcord.Color.dark_theme())
    await msg.edit(embed=embed)
        

  

    


def setup(bot):
    bot.add_cog(Admin(bot))
 
