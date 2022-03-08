import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Fun(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  testserverid = 937841015648292934
  
  @nextcord.slash_command(name ="dm", description = "DM other users with the bot", guild_ids=[testserverid])
  async def dm(self, interaction: Interaction, ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
        await interaction.response.send_message('You need to put a message')
    else:
        embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
        embed.add_field(name="Sent by", value=ctx.author)
        await user.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Delivered to {user}', delete_after=6)
        
  @nextcord.slash_command(name ="test", description = "testing slash commands", guild_ids=[testserverid])
  async def test(self, interaction: Interaction):
    await interaction.response.send_message('Je mappelle Bot')
  
  @commands.command()
  async def anondm(self, ctx, user: nextcord.User, *, message=None, amount=1):
    if message == None:
        await ctx.send('You need to put a message')
    else:
        embed = nextcord.Embed(title="You got mail :incoming_envelope:", description=message)
        embed.add_field(name="Sent by", value="Bingus")
        await user.send(embed=embed)
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Delivered to {user}', delete_after=6)

    @commands.command()
    async def feedfish(self, ctx):
      embed = nextcord.Embed(title="Yummy :fish:", description="You fed bingus some fish and Bingus starts to pur.")
      await ctx.reply(embed=embed)
      print("Yum")


    
def setup(bot):
    bot.add_cog(Fun(bot))
