from ast import Global
import nextcord
from nextcord.ext import commands
from nextcord import Member, SlashOption, Interaction
from servers import *

class HHSD(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
    
  @commands.Cog.listener()
  async def on_member_join(self, member: Member):
    guild = member.guild
    if guild.id == GC:
      if member.id in GCBlacklist.values():
        GCGeneral = self.bot.get_channel(1019954279211077668)
        try:
          embed = nextcord.Embed(title='Yikes..', description=f"We wish to welcome you to **{guild.name}** but unfortunantly it seems you're not allowed in these parts\n Sorry for the Incovienece", color=nextcord.Color.red())
          embed.set_footer(text="Don't yell at me, i'm just the bot")
          embed.set_image(url=guild.icon)
          await member.send(embed=embed)
        except:
          pass
        await GCGeneral.send(f"welp it looks like {member.mention} tried to join")
        await member.kick(reason="Blacklisted") 
      else: pass
    else: pass 

  @commands.command()
  async def addserverbl(self, ctx, member: Member):
    guild = member.guild
    if ctx.author.id in self.bot.owners.values():
      GCGeneral = self.bot.get_channel(1019954279211077668)
      GCBlacklist.update({member.name: member.id})
      await ctx.send(f'Added {member} to the blacklist')
      if member.id in GCBlacklist.values():
        try:
          embed = nextcord.Embed(title='Yikes..', description=f"We wish to welcome you to **{guild.name}** but unfortunantly it seems you're not allowed in these parts\n Sorry for the Incovienece", color=nextcord.Color.red())
          embed.set_footer(text="Don't yell at me, i'm just the bot")
          embed.set_image(url=guild.icon)
          await member.send(embed=embed)
        except:
          pass
        await GCGeneral.send(f"its so sad to see {member.mention} get blacklisted. YOU'RE OUT")
        await member.kick(reason="Blacklisted")
    else:
      await ctx.send("what made you think that you could do that?")
  
  @commands.command()
  async def removebl(self, ctx, member: int = Member):
    #fetch user by id
    member = self.bot.get_user(member)
    if ctx.author.id in self.bot.owners.values():
      if member.id in GCBlacklist.values():
        GCBlacklist.pop(member.name)
        await ctx.send(f'Removed {member} from the blacklist')
        try:
          await member.send(f'You have been removed from the blacklist of {ctx.guild.name}')
        except:
          pass
      else:
        await ctx.send(f'{member} is not in the blacklist')
    else:
      await ctx.send("if you cant add people, what makes you think you can remove them?")

def setup(bot):
    bot.add_cog(HHSD(bot))
