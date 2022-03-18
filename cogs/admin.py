from urllib import response
import nextcord
from nextcord import Member
from nextcord.ext import commands
from nextcord.ext.commands import Bot, has_permissions, MissingPermissions
import asyncio
import requests

class Admin(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  @has_permissions(kick_members=True)
  async def kick(self, ctx, member: nextcord.Member, *, reason=None):
      embed = nextcord.Embed(title="Kicked! :boot::boom:", description=f"{member} was kicked from the nextcord")
      await member.kick(reason=reason)
      await ctx.reply(embed=embed)


  @kick.error
  async def kick_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        kickerror = nextcord.Embed(title="Missing Permission :x:", description="You dont have the permissions to kick members!")
      await ctx.reply(embed=kickerror, delete_after=5)


  @commands.command()
  @has_permissions(kick_members=True)
  async def ban(self, ctx, member: nextcord.Member, user: nextcord.User *, reason=None):
    if member = None:
      rembed = nextcord.Embed(title="???", description="You gotta say who tf you're trying to ban. Dumbass.")
      ctx.reply(embed=rembed)
    else:
      embed = nextcord.Embed(title="Banned! :boot::boom:", description=f"{member} was banned from the discord")
      dembed = nextcord.Embed(title="You were banned from", description="Insane Asylum")
      dembed.add_field(name="Banned by", value=ctx.Author)
      dembed.add_field(name="For the reason", value=reason)
      await member.send(embed=dembed)
      await member.ban(reason=reason)
      await ctx.reply(embed=embed)

  @ban.error
  async def ban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        banerror = nextcord.Embed(title="Missing Permission :x:", description="You dont have the permissions to ban members!")
      await ctx.reply(embed=banerror, delete_after=5)


  @commands.command()
  @has_permissions(manage_messages=True)
  async def purge(self, ctx, amount=11):
      amount = amount + 1
      if amount < 3:
        purgemin = nextcord.Embed(title='You are trying to purge to little', description='You couldnt delete one message on your own?')
        await ctx.reply(embed=purgemin, delete_after=5)
        return
      if amount > 101:
        purgefail = nextcord.Embed(title="Fail to Purge", description="Cannot remove more than 100 messages")
        await ctx.reply(embed=purgefail, delete_after=5)
      else:
        embed = nextcord.Embed(title='Purged!:bomb:', description=f'Deleted {amount-1} messages')
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=embed, delete_after=5)
  
  @purge.error
  async def purge_error(self, ctx, error,):
      if isinstance(error, commands.MissingPermissions):
        purgeerror = nextcord.Embed(title="Missing Permission :x:", description="You dont have the permissions to Purge Messages!")
      await ctx.reply(embed=purgeerror, delete_after=5)

def setup(bot):
    bot.add_cog(Admin(bot))
 