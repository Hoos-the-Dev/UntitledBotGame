import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Fun(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  testserverid = 937841015648292934  
  
  @commands.command()
  @commands.guild_only()  
  async def dm(self, ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
      await ctx.reply(f"You need to give me a message to send to {user}. But you should've known that already. dumbass")
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


    
def setup(bot):
    bot.add_cog(Fun(bot))
