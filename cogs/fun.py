from email.mime import application, image

from pip import main
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from urllib import response
from nextcord import Member
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext.commands import command, Cog
import asyncio
import requests
import random
from random import randint
import humanfriendly
import aiohttp
from urllib3 import Retry
from resources.snipe import *
import resources.functions as func
from resources.ecofunc import *
import aiosqlite 
from lib import console


async def B_GetMemberPermissions(self, member, channel):
    permissions = channel.permissions_for(member)
    return permissions

class Fun(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  testserverid = 937841015648292934  
  @nextcord.slash_command(name = "parrot", description = "Repeats what you say (for the most part :/)")
  async def parrot(self, interaction:Interaction, message: str = SlashOption(name = "message", description = "Sentence to repeat", required=True)):
    reply = {"im gay": "already knew that but ok",
    "im stupid": "Do you really think I'm that stupid?",
    "smd": "theres nothing to suck...",
    "kys": "keep yourself safe :smiling_face_with_3_hearts:",
    "wanna fuck": "bro im a bot for crying outloud",
    "gordon ramsay": "idiot sandwich"}
    mesg = func.B_DeleteApostrophes(message)
    msg = reply.get(mesg.lower(), message)


    await interaction.send(msg)


  @nextcord.slash_command(name = "ltg", description = 'Send GIF to hear a faint "You should kill yourself NOW!" with reverb')
  async def ltg(self, interaction:Interaction):
    await interaction.send("https://tenor.com/view/ltg-low-tier-god-yskysn-ltg-thunder-thunder-gif-23523876")

  @nextcord.slash_command(name = "grammarnazi", description = "Correct user's small grammatical errors with style")
  async def grammarnazi(self, interaction:Interaction, option: str = SlashOption(name="type", description="Type of grammatical error", choices=["Your", "You're", "Yr'oue", "There", "They're", "Their"])):
    if option == "Your": await interaction.send("https://tenor.com/view/your-youre-spies-in-disguise-your-spies-gif-20405823")
    elif option == "You're": await interaction.send("https://tenor.com/view/youre-your-spies-spies-in-disguise-youre-spies-gif-20405819")
    elif option == "Yr'oue": await interaction.send("https://tenor.com/view/youre-your-gif-22328611")
    elif option == "There": await interaction.send("https://tenor.com/view/there-spies-in-disguise-gif-gif-24309165")
    elif option == "They're": await interaction.send("https://tenor.com/view/theyre-spies-in-disguise-their-there-spies-gif-23521253")
    elif option == "Their": await interaction.send("https://tenor.com/view/spies-in-disguise-spies-their-there-grammar-gif-22659580")

  @nextcord.slash_command(name = "ltg2", description = '"What are you here for? To worship me? KILL YOURSELF!!!!!" -LowTierGod (what a prophet)')
  async def ltg2(self, interaction:Interaction):
   await interaction.send("https://tenor.com/view/ltg-low-tier-god-meme-gif-23851809")

  @nextcord.slash_command(name = "mail", description = 'Mail a fam, not a flam')
  async def mail(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "recipent", description = "user", required=True), text: str = SlashOption(name = "text", description = "The contents of the message", required=True), anonymous: str = SlashOption(name = "anonymous", description = "Whether or not the mail composer appears as you, or Bingus", choices=["Yes", "No"], required=True), subject: str = SlashOption(name = "subject", description = "Subject of mail, if any", required=False)):
    if self.bot.user.id == member.id: await interaction.send("What did we accomplish here?", ephemral=True); return
    
    if subject == None: subject = "(no subject)"
    botname = str.lower(self.bot.user.name)
    username = str.lower(interaction.user.name)
    servername = str.lower(interaction.user.guild.name)
    servname = func.B_DeleteSpaces(servername)
    composer = f"{func.B_DeleteSpaces(username)}@bing.us"
    embed = nextcord.Embed(title="You've got new mail! :incoming_envelope:", color=nextcord.Color.random())
    if anonymous == "Yes": 
      botname = func.B_StringMask(botname, "prototype", "the");  botname = func.B_StringMask(botname, "bing", "ding")
      composer = f"{func.B_DeleteSpaces(botname)}@bing.us"
      embed.color = nextcord.Color.blue()
    else:
      # servername = func.B_StringMask(servername, "apartment on 22nd floor", "transit22"); servername = func.B_StringMask(servername, "asylum", "delivery")
      # servers = ["the22ndfloor", "transit22", "mentalward", "insaneimports", "haunted22", "hauntedtransit", "r34.hanime.tv", "theasylum"]
      # domains = ["com", "gg", "net", "org"]
      # url = random.choice(servers)
      # com = random.choice(domains)
      embed.add_field(name="Address", value=f"mail.{servname}.gg")
      if interaction.user.id == member.id: 
        composer = "me"

    embed.add_field(name="From", value=composer)
    embed.add_field(name=subject, value=text)
    await member.send(embed=embed)
    await interaction.send("Message sent.", ephemeral=True)
    #wait for response
    def check(m):
      return m.author.id == member.id and m.channel.id == member.dm_channel.id
    try:
      msg = await self.bot.wait_for("message", check=check)
      await interaction.send(f"Message received: {msg.content}", ephemeral=True)
    except:
      await member.send("Message timed out.", ephemeral=True)

  @mail.error
  async def mail_error(self, interaction:Interaction, member: nextcord.Member = SlashOption(name = "recipent", description = "user", required=True), text: str = SlashOption(name = "text", description = "The contents of the message", required=True), anonymous: str = SlashOption(name = "anonymous", description = "Whether or not the mail composer appears as you, or Bingus", choices=["Yes", "No"], required=True), subject: str = SlashOption(name = "subject", description = "Subject of mail, if any", required=False)):
    await interaction.send("This user is not accepting mail.", ephemeral=True)

  @commands.Cog.listener()
  async def on_message_delete(self, message):

    if message.author.bot == True: return
    if message.channel.id in Snipe:
      del_snipe(message.channel.id)
      add_snipe(message.author.id, message.content, message.channel.id)
    else:
      add_snipe(message.author.id, message.content, message.channel.id)

    

    await asyncio.sleep(60) # Took too long to execute the command, better luck next time
    try:
      del_snipe(message.channel.id)
    except:
      pass
  
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.author.bot == True: return
    if before.channel.id in Snipe:
      del_edit_snipe(after.channel.id)
      edit_snipe_add(after.author.id, before.content, after.content, after.channel.id)
    else:
      edit_snipe_add(after.author.id, before.content, after.content, after.channel.id)

    await asyncio.sleep(60) # Took too long to execute the command, better luck next time
    try:
      del_edit_snipe(after.channel.id)
    except:
      pass
  @nextcord.slash_command(name="snipe", description=f"Resend deleted or edited message")
  async def snipe(self, interaction:Interaction, type: str = SlashOption(name="on_message", description="To see a previously deleted or edited message", choices=["Delete", "Edit"], required=True)):
    if type == "edit":
      try:
        og_msg = get_og_message(interaction.channel.id)
        new_msg = get_new_message(interaction.channel.id)
      except KeyError:
        await interaction.send("um i got nothing", ephemeral=True)
        return
      auth = get_edit_author(interaction.channel.id)
      author = self.bot.get_user(auth)
      embed = nextcord.Embed(color=nextcord.Color.random())
      embed.add_field(name="Before:", value=og_msg)
      embed.add_field(name='After:', value=new_msg)
      embed.set_author(name=author.name, icon_url=author.avatar)
      await interaction.send(embed=embed)
      return
    try:
      snipe_message = get_message(interaction.channel.id)
    except KeyError:
      resp = ["nothing to see fam. better luck next time", "👨‍🦯", "i got nothing ¯\_(ツ)_/¯", "you late", "that message gone. oh well", ":/"]
      await interaction.send(random.choice(resp), ephemeral=True)
      return
    auth = get_author(interaction.channel.id)
    author = self.bot.get_user(auth)
    embed = nextcord.Embed(description=snipe_message, color=nextcord.Color.random())
    embed.set_author(name=author.name, icon_url=author.avatar)
    await interaction.send(embed=embed)

  @commands.command(name="snipe", description="Resend deleted or edited message")
  async def snipe2(self, ctx, mode=None):
    if mode == "edit":
      try:
        og_msg = get_og_message(ctx.channel.id)
        new_msg = get_new_message(ctx.channel.id)
      except KeyError:
        await ctx.reply("um i got nothing")
        return
      auth = get_edit_author(ctx.channel.id)
      author = self.bot.get_user(auth)
      embed = nextcord.Embed(color=nextcord.Color.random())
      embed.add_field(name="Before:", value=og_msg)
      embed.add_field(name='After:', value=new_msg)
      embed.set_author(name=author.name, icon_url=author.avatar)
      await ctx.send(embed=embed)
      return
    try:
      snipe_message = get_message(ctx.channel.id)
    except KeyError:
      resp = ["nothing to see fam. better luck next time", "👨‍🦯", "i got nothing ¯\_(ツ)_/¯", "you late", "that message gone. oh well", ":/"]
      await ctx.reply(random.choice(resp))
      return
    auth = get_author(ctx.channel.id)
    author = self.bot.get_user(auth)
    embed = nextcord.Embed(description=snipe_message, color=nextcord.Color.random())
    embed.set_author(name=author.name, icon_url=author.avatar)
    await ctx.send(embed=embed)
  

  
  #@snipe.error
  #async def snipe_error(self, interaction:Interaction, on_message: str = SlashOption(name="on_message", description="To see a previously deleted or edited message", choices=["Delete", "Edit"], required=True)):
  #  await interaction.send("Unknown error occurred; snipe failed.", ephemeral=True)
        
  @nextcord.slash_command(name="avatar", description=f"View user's avatar")
  async def avatar(self, interaction:Interaction, guild_avatar: str = SlashOption(name='guild_avatar', description="Send the user's server profile picture, if provided", choices=["True", "False"], required=True), member: nextcord.Member = SlashOption(name="user", description="The user avatar to send, if not your own", required=False)):
    if member == None: member = interaction.user
    embed = nextcord.Embed(color=nextcord.Color.random())
    func.B_SetEmbedAuthor(embed, interaction.user)
    if guild_avatar == "True":
      if member.guild_avatar == None: await interaction.send("That user does not have a server avatar.", ephemeral=True); return
      embed.set_image(url=member.guild_avatar)
    else:
      embed.set_image(url=member.avatar)
    await interaction.send(embed=embed)

  @nextcord.slash_command(name="info", description="Get user's info")
  async def info(self, interaction:Interaction, member: nextcord.Member = SlashOption(name="user", description="The user's info to get", required=True)):
    roles = "\n".join([role.mention for role in member.roles])
    if roles == "@everyone": #DONT WORK ON THE BOT RN 
      roles = None
    elif "@everyone" in roles:
      roles = func.B_StringMask(roles, "@everyone", "")

    embed = nextcord.Embed(description=member.mention, color=nextcord.Color.random())
    func.B_SetEmbedAuthor(embed, member)

    if member.display_name != member.name:
      embed.add_field(name="Username", value=member.name)
    
    if member.roles:
      embed.add_field(name="Roles", value=roles)

    if member != self.bot.user:
      if func.B_IsMemberOwner(self, member) == True:
        embed.add_field(name="Owner", value="Yes")
      else:
        embed.add_field(name="Owner", value="No")
    if func.B_CheckHorniJail(self, member) == True:
      embed.add_field(name="Horny Jail Status:", value="Yes")
    else:
      embed.add_field(name="Horny Jail Status:", value="No")


    status = nextcord.Status
    activity = member.activity
    if status:
      if activity == None: 
        activity = "*no activity found*"
      if activity == nextcord.ActivityType.streaming:
        activity = f":purple_circle: Streaming {activity.name} watch [here]({activity.url})"
      elif activity == nextcord.ActivityType.listening:
        activity = f":headphones: Listening to {activity.name})"
      elif activity == nextcord.ActivityType.watching:
        activity = f":eye: Watching {activity.name}"
      

      if member.status == status.dnd:
        embed.add_field(name="Status - :red_circle:", value=activity)
      elif member.status == status.idle:
        embed.add_field(name="Status - :crescent_moon:", value=activity)
      elif member.status == status.online:
        embed.add_field(name="Status - :green_circle:", value=activity)
    else:
      embed.add_field(name="Status - :black_circle:", value="``offline``")

    #add an embed for the permissions the user has
    if B_GetMemberPermissions(self, member) != None:
      embed.add_field(name="Permissions", value="`None`")
    else:
      embed.add_field(name="Permissions", value=f"`{B_GetMemberPermissions}`")

    

    embed.add_field(name="Joined", value=f"{member.joined_at.strftime('%m/%d/%Y')}\n")
    embed.add_field(name="Account Created", value=f"{member.created_at.strftime('%m/%d/%Y')}\n")
    embed.set_thumbnail(url=member.avatar)
    await interaction.send(embed=embed)

  @nextcord.slash_command(name="ping", description="Ping the bot")
  async def ping(self, interaction:Interaction):
    embed = nextcord.Embed(title=":ping_pong: Pong")
    embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
    embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar)
    await interaction.send(embed=embed)

  @nextcord.slash_command(name="animeme", description="Gives you a random anime meme from reddit")
  async def animeme(self, interaction:Interaction):
      async with aiohttp.ClientSession() as cd:
          async with cd.get("https://www.reddit.com/r/animememes.json") as r:
              animememes = await r.json()
              embed = nextcord.Embed(title="here..", description="idk why u wanted this but ok", color=nextcord.Color.random())
              embed.set_image(url=animememes["data"]["children"][random.randint(0, 30)]["data"]["url"])
              footer_text = [f"Requested by **{interaction.user}**", "Powered by Reddit", "50% chance of being loli", "that girl is 8, fuck the canon", "fucking weeb", "$10 that its a actual good meme, dm me"]
              embed.set_footer(text="fucking weeb")
              await interaction.send(embed=embed)
  
  @nextcord.slash_command(name="meme", description="Gives you a random meme from reddit")
  async def meme(self, interaction:Interaction):
      async with aiohttp.ClientSession() as cd:
          async with cd.get("https://www.reddit.com/r/memes.json") as r:
              memes = await r.json()
              embed = nextcord.Embed(title="Here ya go", color=nextcord.Color.random())
              embed.set_image(url=memes["data"]["children"][random.randint(0, 30)]["data"]["url"])
              footer_text = ["is this what you do with your free time?", "you bored rn?", "ima be real this is all from reddit", "go outside", "it might be a good meme, idk", "go back to jerking off"]
              embed.set_footer(text=random.choice(footer_text))
              await interaction.send(embed=embed)

  @nextcord.slash_command(name="feed", description="Feed Bingus")
  async def feed_bot(self, interaction:Interaction, food: str = SlashOption(name="food", description="The food to feed", choices=["Cod", "Salmon", "Canned Food", "Kibble", "Catnip"], required=True)):    
    embed = nextcord.Embed(title="Yummy 🐟", description=f"You fed Bingus some {food.lower()}, he starts to pur...", color=nextcord.Color.random())
    if food == "Cod" or food == "Salmon":
      embed.title = "Yummy 🐟"
    elif food == "Canned Food":
      embed.title = "Mmmmmmm 🥫"
    elif food == "Kibble":
      embed.title = "shit is dry but good 😺"
    elif food == "Catnip":
      embed = nextcord.Embed(title="ohhhhhhhh shiiit <a:cat_dies:976803192367116309>", description=f"You gave {self.bot.user.name} {food.lower()}, he falls out and rolls over, rubbing up against you. Bro's high as shit, my boy....", color=nextcord.Color.red())
    func.B_SetEmbedAuthor(embed, interaction.user, True)
    embed.set_footer(text=f"Thank you for the {food.lower()}, {interaction.user.name}! ❤️")
    await interaction.send(embed=embed)

  @nextcord.slash_command(name="version", description="Gives you the current version of the bot")
  async def version(self, interaction:Interaction):
    embed = nextcord.Embed(title="Version", description=f"{self.bot.version}", color=nextcord.Color.random())
    embed.set_thumbnail(url=self.bot.user.avatar)
    func.B_SetEmbedAuthor(embed, interaction.user, False)
    embed.set_footer(text=f"Thank you for using {self.bot.user.name}. ❤️")
    await interaction.send(embed=embed)
  
  
  # ===I NEED TO DO THIS LATER===

  # @nextcord.slash_command(name="hornyjail", description="put someone in hornijail")
  # async def hornijail(self, interaction:Interaction, member: nextcord.Member):
  #   if func.B_CheckHorniJail(self, member) == True: await interaction.send("That user is already in Horni Jail"); return
  #   if func.B_CheckHorniJail(self, interaction.user) == True: await interaction.send("but you're in horny jail yourself"); return
  #   else:
  #     time = random.randint(1, 365)
  #     time = str(time)
  #     time = time+"d"
  #     if time == 365:
  #       embed = nextcord.Embed(title="Horni Jail", description=f"{member.mention} has been put in Horni Jail", color=nextcord.Color.red())
  #       embed.add_field(name="Sentence", value="**Yikes!** you got max sentence and have been put in for `1 year`")
  #       await interaction.send(embed=embed)
  #       func.B_AddHorniJail(self, member)
  #     func.B_AddHorniJail(self, member)
  #     embed = nextcord.Embed(title="Horni Jail", description=f"{member.name} has been put in Horni Jail", color=nextcord.Color.red())
  #     embed.add_field(name="Sentence", value=f"{time} days")
  #     time = humanfriendly.parse_timespan(time)
  #     embed.set_thumbnail(url=member.avatar)
  #     await interaction.send(embed=embed)
    
  @nextcord.slash_command(name="coinflip", description="Flips a coin")
  async def coinflip(self, interaction:Interaction):
    coinflip = ["tails", "heads"]
    result = random.choice(coinflip)
    await interaction.send(result)

  @nextcord.slash_command(name="roll", description="Rolls a dice")
  async def roll(self, interaction:Interaction):
    dice = random.randint(1, 6)
    await interaction.send(dice)
  
  @nextcord.slash_command(name="8ball", description="Ask the magic 8ball a question")
  async def eightball(self, interaction:Interaction, question: str = SlashOption(name="question", description="The question to ask", required=True)):
    eightball = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful" , "personally i wouldnt bet on it"]
    result = random.choice(eightball)
    embed = nextcord.Embed(title="Magic 8ball 🎱", description=f'"{question}"')
    embed.add_field(name="Answer", value=result)
    func.B_SetEmbedAuthor(embed, interaction.user, False)
    await interaction.send(embed=embed)
  

  @nextcord.slash_command(name="gayrate", description="see how gay you or someone else is (no homo)")
  async def gayrate(self, interaction:Interaction, member: nextcord.User=SlashOption(name="user", description="whos gay rate you're checking", required=True)):
    youoris = ""
    if member.id == interaction.user.id: youoris = ", you are"
    else: youoris = " is"
    if member.id == 365250952480948234: await interaction.send(f"{member.name}{youoris} {randint(89, 100)}% gay"); return
    await interaction.send(f"{member.name}{youoris} {randint(0, 100)}% gay")

  @command(name="dice")
  async def dice(self, ctx: commands.Context, mode, number:int, number2:int, wager:str=None, user:nextcord.Member=None):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    wallet, bank, maxbank = await get_balance(self, ctx.author)
    uwallet, ubank, umaxbank = await get_balance(self, user)
    if wager == 0:
      wager = None
    if mode == "1v1":
      if number == number2:
        await ctx.send("rigged.")
        return
      rng = random.randint(number, number2)
      rng2 = random.randint(number, number2)
      em = nextcord.Embed(title="Dice 🎲", description=f"the dice game will start once {user.mention} accepts")
      msg = await ctx.send(embed=em)
      await msg.add_reaction("👍")
      await msg.add_reaction("👎")
      usr=user
      try:
        def check(reaction, user):
          return user == usr and str(reaction.emoji) in ["👍", "👎"]
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
      except asyncio.TimeoutError:
        embed = nextcord.Embed(title="yikes", description=f"{usr.mention} didnt respond in time", color=nextcord.Color.red())
        await msg.edit(embed=embed)
        return
      if str(reaction.emoji) == "👎":
        embed = nextcord.Embed(title="yikes", description=f"{usr.mention} declined your request", color=nextcord.Color.red())
        await msg.edit(embed=embed)
        return
      if str(reaction.emoji) == "👍":
        em = nextcord.Embed(title="Dice 🎲", description="the dice game will commence soon", color=nextcord.Color.random())
        msg = await ctx.send(embed=em)
        await asyncio.sleep(3)
        em.description = f"the dice game has began"
        em.add_field(name=ctx.author.name, value=f"???")
        em.add_field(name=user.name, value=f"???")
        await msg.edit(embed=em)
        await asyncio.sleep(2)
        em = nextcord.Embed(title="Dice 🎲", description="the dice game has began", color=nextcord.Color.random())
        em.add_field(name=ctx.author.name, value=f"rolls a **{rng}**")
        em.add_field(name=user.name, value=f"???")
        await msg.edit(embed=em)
        await asyncio.sleep(4)
        em = nextcord.Embed(title="Dice 🎲", description="the dice game has began", color=nextcord.Color.random())
        em.add_field(name=ctx.author.name, value=f"rolls a **{rng}**")
        em.add_field(name=user.name, value=f"rolls a **{rng2}**")
        await msg.edit(embed=em)

        if rng > rng2:
          await ctx.send(f"{ctx.author.name} won the dice game")
        elif rng2 > rng:
          await ctx.send(f"{user.name} won the dice game")
        else:
          await ctx.send("it was a tie")
        
        if wager == None:
          return
        if "b" in wager:
          wager = int(wager.replace("b", ""))
          wager = wager * 1000000000
        elif "m" in wager:
          wager = int(wager.replace("m", ""))
          wager = wager * 1000000
        elif "k" in wager:
          wager = int(wager.replace("k", ""))
          wager = wager * 1000
        else:
          try: wager = int(wager)
          except: await ctx.send("invalid wager"); return
        if wager < 0:
          await ctx.send("wager cannot be negative, wager has been voided")
          return
        if int(wallet) < wager:
          await ctx.send("you dont have enough balance to bet that much. no wager, no money")
          return
        if int(uwallet) < wager:
          await ctx.send("they dont have enough money to bet that much. Don't siphon from the poor")
          return
        if rng > rng2:
          await update_balance(self, ctx.author, wager)
          await update_balance(self, user, -wager)
          await ctx.send(f"{ctx.author.name} won {wager}")
        elif rng2 > rng:
          await update_balance(self, user, wager)
          await update_balance(self, ctx.author, -wager)
          await ctx.send(f"{user.name} won {wager}")
        else:
          await ctx.send("it was a tie")

    elif mode == "solo":
      if number == number2:
        await ctx.send("rigged.")
        return
      rng = random.randint(number, number2)
      rng2 = random.randint(number, number2)
      em = nextcord.Embed(title="Dice 🎲", description="the dice game will commence soon", color=nextcord.Color.random())
      msg = await ctx.send(embed=em)
      await asyncio.sleep(3)
      em.description = f"the dice game has began"
      em.add_field(name=ctx.author.name, value=f"???")
      em.add_field(name="CPU", value=f"???")
      await msg.edit(embed=em)
      await asyncio.sleep(2)
      em = nextcord.Embed(title="Dice 🎲", description="the dice game has began", color=nextcord.Color.random())
      em.add_field(name=ctx.author.name, value=f"rolls a **{rng}**")
      em.add_field(name="CPU", value=f"???")
      await msg.edit(embed=em)
      await asyncio.sleep(4)
      em = nextcord.Embed(title="Dice 🎲", description="the dice game has began", color=nextcord.Color.random())
      em.add_field(name=ctx.author.name, value=f"rolls a **{rng}**")
      em.add_field(name="CPU", value=f"rolls a **{rng2}**")
      await msg.edit(embed=em)

      if wager == None:
        return
      if "b" in wager:
        wager = int(wager.replace("b", ""))
        wager = wager * 1000000000
      elif "m" in wager:
        wager = int(wager.replace("m", ""))
        wager = wager * 1000000
      elif "k" in wager:
        wager = int(wager.replace("k", ""))
        wager = wager * 1000
      else:
        try: wager = int(wager)
        except: await ctx.send("invalid wager"); return
      if wager < 0:
        await ctx.send("wager cannot be negative")
        return
      if int(await get_balance(self, ctx.author.id)) < wager:
        await ctx.send("you dont have enough balance to bet that much, no loss but also no money made")
        return
      if rng > number2/2:
        update_balance(self, ctx.author, wager)
        await ctx.send(f"{ctx.author.name} won {wager}")
      else:
        update_balance(self, ctx.author, -wager)
        await ctx.send(f"{ctx.author.name} lost {wager}")
  


    
    

def setup(bot):
    bot.add_cog(Fun(bot))   