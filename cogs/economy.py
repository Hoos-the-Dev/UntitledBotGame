import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from urllib import response
from nextcord import Member, Embed, Color
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext.commands import command, Cog, cooldown, BucketType
import asyncio
import requests
import random
from random import randint
import humanfriendly
import aiohttp
from urllib3 import Retry
from resources.functions import *
from resources.iio import *
from lib import console
import aiosqlite
from resources.ecofunc import * 
from resources.marriage import *


class Economy(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @Cog.listener()
  async def on_ready(self):
    self.db = await aiosqlite.connect("resources/data/bank.db")
    await self.db.execute("CREATE TABLE IF NOT EXISTS bank (wallet INTEGER, bank INTEGER, maxbank INTEGER, user INTEGER)")
    items = []
    for i in json.load(open("resources/data/items.json")):
      items.append(i)
    await self.db.execute("CREATE TABLE IF NOT EXISTS inv (banknote INTERGER, apple INTERGER, computer INTERGET, Catnip INTERGER, user INTERGER)")
    await self.db.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, id TEXT, description TEXT, price INTERGER)")
    await self.db.commit()
    console.info("Bank database connected")

  

  @command(aliases=["bal"], description="Check your balance")
  async def balance(self, ctx: commands.Context, member: nextcord.Member = None):
    if member is None:
      member = ctx.author
    wallet, bank, maxbank = await get_balance(self, member)
    embed = nextcord.Embed(title=f"{member.name}'s balance", color=nextcord.Color.green())
    embed.add_field(name="Wallet", value=f"${wallet}", inline=True)
    embed.add_field(name="Bank", value=f"${bank}/${maxbank}", inline=True)
    await ctx.reply(embed=embed)

  @command(aliases=["wd"], description="Withdraw money from your bank")
  async def withdraw(self, ctx: commands.Context, amount):
    wallet, bank, maxbank = await get_balance(self, ctx.author)
    if amount is None:
      await ctx.send("Please specify an amount")
      return
    if amount == "all" or amount == "max":
      await update_balance(self, ctx.author, bank)
      await update_bank(self, ctx.author, -bank)
      embed = Embed(description=f"Withdrew ${bank} from your bank", color=Color.yellow())
      await ctx.send(embed=embed)
      return
    if amount == "half":
      amount = bank / 2
      await update_balance(self, ctx.author, amount)
      await update_bank(self, ctx.author, -amount)
      embed = Embed(description=f"Withdrew ${amount} from your bank", color=Color.yellow())
      await ctx.send(embed=embed)
      return
    if "b" in amount:
      amount = amount.replace("b", "")
      try: amount = int(amount) * 1000000000
      except: await ctx.reply("does that look valid to you?")
    if "m" in amount:
      amount = amount.replace("m", "")
      try: amount = int(amount) * 1000000
      except: await ctx.reply("does that look valid to you?")
    if "k" in amount:
      amount = amount.replace("k", "")
      try: amount = int(amount) * 1000
      except: await ctx.reply("does that look valid to you?")
    try: amount = int(amount)
    except: await ctx.reply("NUMBERS, I NEED NUMBERS")
    if amount > bank:
      await ctx.send("You don't have that much money in your bank")
      return
    await update_bank(self, ctx.author, -amount)
    await update_balance(self, ctx.author, amount)
    embed = Embed(description=f"Withdrew ${amount} from your bank", color=Color.yellow())
    await ctx.send(embed=embed)

  @command(aliases=["dep"], description="Deposit money into your bank")
  async def deposit(self, ctx: commands.Context, amount):
    if amount is None:
      await ctx.send("Please specify an amount")
      return 
    wallet, bank, maxbank = await get_balance(self, ctx.author)
    if amount == "all" or amount == "max":
      if int(wallet) == 0:
        embed = Embed(description=f"Deposited ${wallet} into your bank", color=Color.red())
        await ctx.send(embed=embed)
        return
      if bank > maxbank:
        await ctx.reply("Your bank is full")
        return
      if wallet > maxbank:
        #deposit until bank is full
        await update_bank(self, ctx.author, maxbank)
        await update_balance(self, ctx.author, -maxbank)
        if bank > maxbank:
          amount = bank - maxbank
          await update_bank(self, ctx.author, -amount)
          await update_balance(self, ctx.author, amount)
          return
        embed = Embed(description=f"Deposited ${maxbank} into your bank", color=Color.green())
        await ctx.send(embed=embed)
        return
        
      await update_bank(self, ctx.author, wallet)
      await update_balance(self, ctx.author, -wallet)
      embed = Embed(description=f"Deposited ${wallet} into your bank", color=Color.green())
      await ctx.send(embed=embed)
      return
    if "b" in amount:
      amount = amount.replace("b", "")
      try: amount = int(amount) * 1000000000
      except: await ctx.reply("does that look valid to you?")
    if "m" in amount:
      amount = amount.replace("m", "")
      try: amount = int(amount) * 1000000
      except: await ctx.reply("does that look valid to you?")
    if "k" in amount:
      amount = amount.replace("k", "")
      try: amount = int(amount) * 1000
      except: await ctx.reply("does that look valid to you?")  

    try: amount = int(amount)
    except: await ctx.reply("NUMBERS, I NEED NUMBERS")
    if amount > wallet:
      await ctx.send("You don't have that much money in your wallet")
      return
    if amount > maxbank:
      await ctx.send(f"You have a bank limit of ${maxbank}... do the math")
      return
    if bank >= maxbank:
      await ctx.send("Your bank is full")
      return
      
    await update_balance(self, ctx.author, -amount)
    await update_bank(self, ctx.author, amount)
    embed = Embed(description=f"Deposited ${amount} into your bank", color=Color.green())
    await ctx.send(embed=embed)
  
  @command(description="Pay someone money")
  async def pay(self, ctx: commands.Context, member: nextcord.Member, amount):
    if amount is None:
      await ctx.send("Please specify an amount")
      return
    if member is None:
      await ctx.send("Please specify a member")
      return
    if member == ctx.author:
      await ctx.reply("You can't pay yourself")
      return
    if amount == "all" or amount == "max":
      wallet, bank, maxbank = await get_balance(self, ctx.author)
      await transfer(self, ctx.author, member, wallet)
      embed = Embed(description=f"You paid {member.name} ${wallet}", color=Color.green())
      await ctx.reply(embed=embed)
      return
    if amount == "half":
      wallet, bank, maxbank = await get_balance(self, ctx.author)
      await transfer(self, ctx.author, member, wallet/2)
      embed = Embed(description=f"You paid {member.name} ${wallet/2}", color=Color.green())
      await ctx.reply(embed=embed)
      return
    if "b" in amount:
      amount = amount.replace("b", "")
      try: amount = int(amount) * 1000000000
      except: await ctx.reply("does that look valid to you?")
    if "m" in amount:
      amount = amount.replace("m", "")
      try: amount = int(amount) * 1000000
      except: await ctx.reply("does that look valid to you?")
    if "k" in amount:
      amount = amount.replace("k", "")
      try: amount = int(amount) * 1000
      except: await ctx.reply("does that look valid to you?")
    try: amount = int(amount)
    except: await ctx.reply("NUMBERS, I NEED NUMBERS")
    wallet, bank, maxbank = await get_balance(self, ctx.author)
    if amount > wallet:
      await ctx.send("You don't have that much money in your wallet")
      return
    await transfer(self, ctx.author, member, amount)
    embed = Embed(description=f"You paid {member.name} ${amount}", color=Color.green())
    await ctx.reply(embed=embed)
  
  @command(name="Rob", description="Run someones pockets")
  @cooldown(2, 30, BucketType.user)
  async def rob(self, ctx: commands.Context, member: nextcord.Member):
    semi_rare_chance = await B_RandomChance(25)
    rng_af = await B_RandomChance(0.5)
    if member is None:
      await ctx.reply("Please specify a member")
      return
    if member == ctx.author:
      await ctx.reply("You can't rob yourself")
      return
    wallet, bank, maxbank = await get_balance(self, member)
    op_wallet, op_bank, op_maxbank = await get_balance(self, ctx.author)
    if op_wallet < 2:
      await ctx.reply("i would let you rob someone but theres gotta be some consequences if you get caught")
      return
    if wallet <= 100:
      await ctx.reply("They got sheckles my guy... why are you robbing them? thats sad")
      return
    if semi_rare_chance == True:
      give_max = int(op_wallet / 2)
      amount = randint(1, give_max)
      embed = nextcord.Embed(title="smh", description=f"You got caught and had to pay ${amount}", color=nextcord.Color.red())
      await transfer(self, ctx.author, member, amount)
      await ctx.reply(embed=embed)
      return
    if rng_af == True:
      await transfer(self, member, ctx.author, wallet)
      embed = nextcord.Embed(title="DAMN", description=f"YOU RAN AWAY WITH THEIR WHOLE WALLET AND POCKETED ${wallet}", color=nextcord.Color.gold())
      await ctx.reply(embed=embed)
      return
    give_max = int(wallet / 2)
    amount = randint(1, int(give_max))
    await transfer(self, member, ctx.author, amount)
    embed = Embed(description=f"You robbed {member.name} and got ${amount}", color=Color.green())
    await ctx.reply(embed=embed)
  
  @command()
  @cooldown(3, 20, BucketType.user)
  async def beg(self, ctx: commands.Context):
    wallet, bank, maxbank = await get_balance(self, ctx.author)
    semi_rare_chance = await B_RandomChance(25)
    rng_af = await B_RandomChance(0.5)
    amount = randint(1, 100)
    rng = randint(1, 100)
    fail_titles = ["oof", "yikes", "ouch", "thats wild", "fail", "oooo....", "eels"]
    fail_message = ["leave me alone...", "i want a restraining order", "ew poor people", "hands and knees bucko", "cry me a river", "i dont have any money *while wearing gucci flip flops*", "creep", "...... *hes got airpods in*", "just get a job", "i dont support hobos", "you just gonna use the money on drugs", "bum"]
    success_titles = ["nice", "wow", "yay", "yuh", "yeehaw"]
    success_msg = ["Sure, I can help you out.",  "Of course, I'm happy to give a hand.",  "Yeah, I can spare some money for you.",  "Sure thing, let me see what I can do.",  "I'd be glad to help. What do you need?",  "Yeah, I don't mind lending a hand.",  "Absolutely, I'll do what I can.",  "Sure, I'll try my best to assist you.",  "Of course, I'll do what I can to help.",  "Definitely, let's see what we can do together."]
    citizen_firstnames = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph", "Thomas", "Christopher", "Daniel", "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin", "Jason", "Matthew", "Gary", "Timothy", "Jose", "Larry", "Jeffrey", "Frank", "Scott", "Eric", "Stephen", "Andrew", "Raymond", "Gregory", "Joshua", "Jerry", "Dennis", "Walter", "Patrick", "Peter", "Harold", "Douglas", "Henry", "Carl", "Arthur", "Ryan", "Roger", "Joe", "Juan", "Jack", "Albert", "Jonathan", "Justin", "Terry", "Gerald", "Keith", "Samuel", "Willie", "Ralph", "Lawrence", "Nicholas", "Roy", "Benjamin", "Bruce", "Brandon", "Adam", "Harry", "Fred", "Wayne", "Billy", "Steve", "Louis", "Jeremy", "Aaron", "Randy", "Howard", "Eugene", "Carlos", "Russell", "Bobby", "Victor", "Martin", "Ernest", "Phillip", "Todd", "Jesse", "Craig", "Alan", "Shawn", "Clarence", "Sean", "Philip", "Chris", "Johnny", "Earl", "Jimmy", "Antonio", "Danny", "Bryan", "Tony", "Luis", "Mike", "Stanley", "Leonard", "Nathan", "Dale", "Manuel", "Rodney", "Curtis", "Norman", "Allen", "Marvin", "Vincent", "Glenn", "Jeffery", "Travis", "Jeff", "Chad", "Jacob", "Lee", "Melvin", "Alfred", "Kyle", "Francis", "Bradley", "Jesus", "Herbert", "Frederick", "Ray", "Joel", "Edwin", "Don", "Eddie", "Ricky", "Troy", "Randall", "Barry", "Alexander", "Bernard", "Mario", "Leroy"]
    citizen_lastnames = ["Heredia","Tate", "Smith", "Jones", "Williams", "Taylor", "Brown", "Wilson", "Johnson", "Davis", "Miller", "White", "Clark", "Hall", "Thomas", "Thompson", "Moore", "Hill", "Walker", "Anderson", "Wright", "Martin", "Wood", "Allen", "Robinson", "Lewis", "Scott", "Green", "King", "Baker", "James", "Russell", "Harris", "Lee", "Jackson", "Phillips", "Edwards", "Turner", "Parker", "Cook", "McDonald", "Bell", "Evans", "Morris", "Mitchell", "Adams", "Campbell", "Carter", "Roberts", "Graham", "Stewart", "Reid", "Murphy", "Bailey", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons"]
    name = random.choice(citizen_firstnames) + " " + random.choice(citizen_lastnames)
    if wallet >= 100000:
      embed = Embed(title="You are too rich to be begging", description="go home.", color=Color.red())
      embed.set_footer(text=f"you are out of your goddamn mind.")
      await ctx.send(embed=embed)
      return
    if randint(1, 2000) == randint(1, 2000):
    # if await B_RandomChance(25):
      embed = Embed(title="MRBEASSST", description=f"MrBeast gave you $100,000", color=Color.gold())

      responses = [
  "Sure, why not? Here's $100,000.",
  "No problem, happy to help. Make good use of it.",
  "It's always great to be able to give back. Enjoy the money!",
  "I believe in spreading kindness and generosity. Here you go.",
  "Money can't buy happiness, but it can make life a little easier. Take this $100,000 and use it wisely.",
  "I'm in a giving mood today. Enjoy this $100,000!",
  "We all could use a little extra help sometimes. Here's $100,000 to make things a little easier.",
  "Pay it forward, that's what I always say. Enjoy the $100,000!",
  "I'm glad I can make a difference in someone's life",
  "Life is too short to not spread happiness. Take this $100,000 and do something great with it."
]

      embed.add_field(name=" ", value=f'"{random.choice(responses)}" -MrBeast')
      embed.set_footer(text=f"+ $100,000", icon_url=ctx.author.avatar)
      await ctx.send(embed=embed)
      await update_balance(self, ctx.author, 100000)
      return

    if randint(1, 10000) == randint(1, 10000):
      embed = Embed(title="MR MUSK?", description=f"Elon Musk gave you $1,000,000", color=Color.gold())
      elon_responses = [
  "Sure, why not? Here's $1,000,000.",
  "No problem, happy to help. Make good use of it.",
  "i paid 40 billion dollars for twitter, i can afford to give you 1 million dollars",
  "does this count as charity work"
  "can i put this on my taxes?"
  "buy a tesla with it"
  "you poor thing"
  "i'm glad i can make a difference in someone's life"
  "i'm in a giving mood today. enjoy this $1,000,000!"
  "life is too short to not spread happiness. take this $1,000,000 and do something great with it."]
      embed.add_field(name=" ", value=f'"{random.choice(elon_responses)}" -Elon Musk')
      embed.set_footer(text=f"+ $1,000,000", icon_url=ctx.author.avatar)
    
    if await B_RandomChance(5):
      embed = Embed(title="You found a wallet", description=f"You found a wallet with $100 in it", color=Color.dark_gold())
      embed.set_footer(text=f"+ $100", icon_url=ctx.author.avatar)
      await ctx.send(embed=embed)
      await update_balance(self, ctx.author, 100)
      return
    
    if randint(1, 25) == randint(1,26): amount = randint(1000, 10000)
    if await B_RandomChance(0.5): amount = randint(100, 1000)

    if await B_RandomChance(35)  == True:
      embed = Embed(title=random.choice(success_titles), description=f'\n"{random.choice(success_msg)}" -{name}', color=Color.green())
      embed.set_footer(text=f"+ ${amount}", icon_url=ctx.author.avatar)
      await update_balance(self, ctx.author, amount)
      await ctx.send(embed=embed)
      return

    embed = Embed(title=random.choice(fail_titles), description=f'\n"{random.choice(fail_message)}" -{name}', color=Color.red())
    await ctx.send(embed=embed)

  @command(name="profile")
  async def profile(self, ctx, member: Member = None):
    self.marriage_db = await aiosqlite.connect("resources/data/marriage.db")
    member = member or ctx.author
    wallet, bank, maxbank = await get_balance(self, member)
    nw = int(bank) + int(wallet)

    if await get_marriage_partner(self, member) == False:
      marriage_partner = False
    else:
      marriage_partner = await get_marriage_partner(self, member)
      marriage_partner = await self.bot.fetch_user(marriage_partner)
    marriage_date = await get_marriage_since(self, member)
    embed = Embed(title=f"{member.name}'s profile", color=Color.blurple())
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="Wallet", value=f"${wallet}")
    embed.add_field(name="Bank", value=f"${bank}")
    embed.add_field(name="Total", value=f"${nw}")
    if marriage_partner == False:
      embed.add_field(name="Marital Status", value="Single")
    else:
      embed.add_field(name="Marital Status", value=f"Married to: {marriage_partner.mention}\nMarried since: {marriage_date}")
  
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)
  

  @command(name="leaderboard", aliases=["lb", "top", "top10"])
  async def leaderboard(self, ctx):
    developement = True
    try:
      # create a leaderboard based on the balance of each user in the server its being called in.
      # the leaderboard will be sorted from highest to lowest.
      # the leaderboard will be displayed in an embed.
      # the leaderboard will be limited to the top 10 users.
      # the leaderboard will be updated every 5 minutes.
      
      # create a connection to the database
      db = await aiosqlite.connect("resources/data/bank.db")
      cursor = await db.cursor()
      # get all the users in the server
      await cursor.execute("SELECT * FROM bank WHERE guild_id = ?", (ctx.guild.id,))
      # fetch all the results
      result = await cursor.fetchall()
      # result is a list of tuples, with the first element of each tuple being the user's ID
      # and the second element being the user's balance.
      # [(user_id, balance), (user_id, balance), ...]

      # sort the list by the user's balance, from highest to lowest
      result.sort(key=lambda x: x[1], reverse=True)

      # create the leaderboard embed
      embed = Embed(title="Leaderboard", description="The richest people in the server.", color=Color.blurple())
      # iterate through the list of tuples
      for x, y in enumerate(result):
        # get the user object for each user
        user = self.bot.get_user(y[0])
        # add a field for each user, showing their position in the leaderboard,
        # their name, and their balance
        embed.add_field(name=f"{x+1}. {user.name}", value=f"${y[1]}", inline=False)
        # only add the top 10 users to the leaderboard
        if x == 9:
          break

      # send the leaderboard embed
      await ctx.send(embed=embed)
    except Exception as e:
      if developement == True:
        if not B_IsMemberOwner(self, ctx.author):
          embed = Embed(title="Error", description="This command is still in developement folks", color=Color.red())
          await ctx.send(embed=embed)
      else:
        raise e

    

    

def setup(bot):
    bot.add_cog(Economy(bot)) 