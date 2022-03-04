import nextcord
from nextcord.ext import commands

class Plans(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def plans(self, ctx):
    ###Edit changelogs to fit the changes
    embed = nextcord.Embed(title="Bot Plans :scroll:", description='Derrick has a goal and wants to work on these things.')
    embed.set_author(name='Derrick')
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/759623404989972482/944494477735772180/derrick.png")
    embed.add_field(name="Migration to Nextcord", value="Discord.py has been discontinued for a bit now. pretty much hindering development in the future. Nextcord is up to date and supports new features discord has to offer. This brings us to...", inline=True)
    embed.add_field(name="Slash commands", value="implementing Slash commands is essential because after April of this year. Discord will no longer support prefixes. A bummer but i cant do much about that. Slash commands will be needed to opperate in the future. ", inline=True)
    embed.add_field(name="Buttons!", value="Buttons, you've seen them. They arent essential but its really barbaric not to have them sooo. yeah. Done properly can do what dyno does and assign role colors.", inline=True)
    embed.add_field(name="Voice Chat support (maybe)", value="I might implement VC support if i find it neccesary ¯\_(ツ)_/¯.")
    embed.add_field(name="Done.", value="Thats about it for now. Cya", )
    embed.add_field(name="From", value="Derrick")
    
    
    await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Plans(bot))
