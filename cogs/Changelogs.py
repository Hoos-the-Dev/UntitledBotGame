import discord
from discord.ext import commands

class Changelogs(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def changelogs(self, ctx):
    ###Edit changelogs to fit the changes
    embed = discord.Embed(title="Changelogs v0.1.0 :newspaper:", description='The first edition of changelogs. The bot has been updated, here we go!')
    embed.set_author(name='Derrick')
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/759623404989972482/944494477735772180/derrick.png")
    embed.add_field(name="Rework of staff commands", value="Staff commands have been re done to support embeding instead of plain generic text. This will also be coming to some other commands aswell", inline=True)
    embed.add_field(name="Addition of Changelogs", value="the addition of the changelogs themselves", inline=True)
    embed.add_field(name="Thats it?", value="Yeah we didnt have much changed to the bot for this changelog but this is the end of the changes. thank you for reading")
    await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Changelogs(bot))
