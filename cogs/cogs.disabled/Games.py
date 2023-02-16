import nextcord
from nextcord.ext import commands
from nextcord import ApplicationInvokeError, Interaction
import asyncio
import random

class Games(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  
  @commands.command()
  async def rps(self, ctx):
    await ctx.send("Rock, Paper, Scissors")
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["rock", "paper", "scissors"]
    user_choice = await self.bot.wait_for("message", check=check)
    bot_choice = random.choice(["rock", "paper", "scissors"])
    await ctx.send(f"I choose {bot_choice}")
    if user_choice.content == bot_choice:
      await ctx.send("It's a tie!")
    elif user_choice.content == "rock" and bot_choice == "paper":
      await ctx.send("I win!")
    elif user_choice.content == "rock" and bot_choice == "scissors":
      await ctx.send("You win!")
    elif user_choice.content == "paper" and bot_choice == "rock":
      await ctx.send("You win!")
    elif user_choice.content == "paper" and bot_choice == "scissors":
      await ctx.send("I win!")
    elif user_choice.content == "scissors" and bot_choice == "rock":
      await ctx.send("I win!")
    elif user_choice.content == "scissors" and bot_choice == "paper":
      await ctx.send("You win!")
    else:
      await ctx.send("Invalid choice")
    
    
  @commands.command()
  async def guess(self, ctx):
    await ctx.send("Guess a number between 1 and 10")
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
    user_guess = await self.bot.wait_for("message", check=check)
    bot_guess = random.randint(1, 10)
    await ctx.send(f"I choose {bot_guess}")
    if int(user_guess.content) == bot_guess:
      await ctx.send("It's a tie!")
    elif int(user_guess.content) > bot_guess:
      await ctx.send("You win!")
    elif int(user_guess.content) < bot_guess:
      await ctx.send("I win!")
    else:
      await ctx.send("Invalid choice")

  
  @commands.command(aliases=["ttt"])
  async def tictactoe(self, ctx, user: nextcord.Member):
    embed = nextcord.Embed(title="Tic Tac Toe", description=f"{ctx.author.mention} vs {user.mention}", color=nextcord.Color.random())
    embed.add_field(name="Board", value="1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9")
    embed.add_field(name="Instructions", value="Type the number of the square you want to place your piece in")
    embed.add_field(name="Turn", value=f"{ctx.author.mention}")
    message = await ctx.send(embed=embed)
    #use buttons
    def check(i):
      return i.author == ctx.author and i.channel == ctx.channel and i.message == message
    while True:
      try:
        interaction = await self.bot.wait_for("interaction", check=check)
      except asyncio.TimeoutError:
        await ctx.send("You took too long to respond")
        break
      if interaction.data.custom_id == "1":
        await interaction.respond(content="1")
      elif interaction.data.custom_id == "2":
        await interaction.respond(content="2")
      elif interaction.data.custom_id == "3":
        await interaction.respond(content="3")
      elif interaction.data.custom_id == "4":
        await interaction.respond(content="4")
      elif interaction.data.custom_id == "5":
        await interaction.respond(content="5")
      elif interaction.data.custom_id == "6":
        await interaction.respond(content="6")
      elif interaction.data.custom_id == "7":
        await interaction.respond(content="7")
      elif interaction.data.custom_id == "8":
        await interaction.respond(content="8")
      elif interaction.data.custom_id == "9":
        await interaction.respond(content="9")
      else:
        await interaction.respond(content="Invalid choice")
  

  @commands.command(aliases=["sma"])
  async def servermuteall(self, ctx):
    if not ctx.author.guild_permissions.mute_members:
      await ctx.send("no")
      return
    vc = ctx.author.voice
    for member in vc.channel.members:
      await member.edit(mute=True)
    await ctx.send("Muted all members in the voice channel, i assume for among us")
  
  @commands.command(aliases=["uma"])
  async def serverunmuteall(self, ctx):
    if not ctx.author.guild_permissions.mute_members:
      await ctx.reply("no")
      return
    vc = ctx.author.voice
    for member in vc.channel.members:
      await member.edit(mute=False)
    await ctx.reply("Unmuted all members in the voice channel")

      
def setup(bot):
    bot.add_cog(Games(bot))
