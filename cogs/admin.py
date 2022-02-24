from urllib import response
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
import asyncio
import requests

class Admin(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  @has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
      embed = discord.Embed(title="Kicked! :boot::boom:", description=f"{member} was kicked from the discord")
      await member.kick(reason=reason)
      await ctx.reply(embed=embed)


  @kick.error
  async def kick_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        kickerror = discord.Embed(title="Missing Permission :x:", description="You dont have the permissions to kick members!")
      await ctx.reply(embed=kickerror, delete_after=5)


  @commands.command()
  @has_permissions(kick_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
      embed = discord.Embed(title="Banned! :boot::boom:", description=f"{member} was banned from the discord")
      await member.ban(reason=reason)
      await ctx.reply(embed=embed)


  @ban.error
  async def ban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        banerror = discord.Embed(title="Missing Permission :x:", description="You dont have the permissions to ban members!")
      await ctx.reply(embed=banerror, delete_after=5)


  @commands.command()
  @has_permissions(manage_messages=True)
  async def purge(self, ctx, amount=11):
      amount = amount + 1
      if amount < 3:
        purgemin = discord.Embed(title='You are trying to purge to little', description='You couldnt delete one message on your own?')
        await ctx.reply(embed=purgemin, delete_after=5)
        return
      if amount > 101:
        purgefail = discord.Embed(title="Fail to Purge", description="Cannot remove more than 100 messages")
        await ctx.reply(embed=purgefail, delete_after=5)
      else:
        embed = discord.Embed(title='Purged!:bomb:', description=f'Deleted {amount-1} messages')
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=embed, delete_after=5)
  
  @purge.error
  async def purge_error(self, ctx, error,):
      if isinstance(error, commands.MissingPermissions):
        purgeerror = discord.Embed(title="Missing Permission :x:", description="You dont have the permissions to Purge Messages!")
      await ctx.reply(embed=purgeerror, delete_after=5)

def setup(bot):
    bot.add_cog(Admin(bot))
 