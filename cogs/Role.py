import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class BotUpdates(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

  @nextcord.ui.button(label = "✔️", style=nextcord.ButtonStyle.blurple)
  async def update(self, button: nextcord.ui.Button, interaction: Interaction):
    guild = nextcord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    role = nextcord.utils.get(guild.roles, name="Bingus Updates")
    if role is not None:
      member = nextcord.utils.find(lambda m: m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
        await interaction.response.send_message('You will now be alerted', ephemeral=True)

class Roles(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

 # @commands.command()
  async def bingusupdates(self, ctx):
    view = BotUpdates()
    await ctx.channel.purge(limit=1)
    await ctx.send('If you want to get pinged for updates with bingus bot. Click the button below.', view=view)
    await view.wait()


def setup(bot):
    bot.add_cog(Roles(bot))
 