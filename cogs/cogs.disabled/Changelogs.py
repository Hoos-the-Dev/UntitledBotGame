from cProfile import label
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class Dropdown(nextcord.ui.Select):
    def __init__(self):
      selectoptions = [
        nextcord.SelectOption(label="Bingus v1.1.0", description="I dont remember when i updated the bot to this version"),
        nextcord.SelectOption(label="Changelogs v2.0.0", description="Upcoming Release"),
      ]
      super().__init__(placeholder='Click to select changelog version', min_values=1, max_values=1, options=selectoptions)
    async def callback(self, interaction: Interaction):
      if self.values[0] == "Changelogs v1.1.0":
        embed = nextcord.Embed(title="Changelogs v1.1.0 :newspaper:", description='The first edition of changelogs. The bot has been updated, here we go!', color=nextcord.Color.green())
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.add_field(name="Rework of staff commands", value="Staff commands have been re done to support embeding instead of plain generic text. This will also be coming to some other commands aswell", inline=True)
        embed.add_field(name="Addition of Changelogs", value="the addition of the changelogs themselves", inline=True)
        embed.add_field(name="Thats it?", value="Yeah we didnt have much changed to the bot for this changelog but this is the end of the changes. thank you for reading")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Changelogs v2.0.0":
        embed = nextcord.Embed(title="Changelogs v2.0 :newspaper:", description='ITS FINALLY HERE! VERSION 2 HAS BEEN RELEASED. LETS THE CHANGES:', color=nextcord.Color.green())
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.add_field(name="No More Prefixes", value="Prefixes have been removed from the bot as future proofing. now all the commands work in the form of a slash command.\nOld Commands work better than ever and new commands too!\n which leads us into....", inline=True)
        embed.add_field(name="New Commands", value="New commands have been added to the bot.\n/avatar, /ltg, /info, /snipe, etc\n Im grateful to have aiire along as alot of this stuff wouldn't have been possible without him. but the show must continue.\n ooo look my favorite", inline=True)
        embed.add_field(name="Oh shi-", value='**The Blacklist**\n simply put it. "fuck around, find out" -Zach Fox until the bot restarts, then it resets. will fix later.')
        embed.add_field(name="AutoResponses", value="AutoResponses have been added to the bot. basically you say some dumb shit or something nice. and the bot will reply to you. and if your name is Flam. theres some special things for you :)", inline=True)
        embed.add_field(name="wait the ride is slowing down?", value="yeah thats about it, theres alot here and more to come. just you wait")
        embed.set_footer(text="made with love by Aiire and Derrick")
        await interaction.send(embed=embed, ephemeral=True)

class DropdownView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Dropdown())

class Changelogs(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @nextcord.slash_command(name="changelogs", description="Shows the changelogs for the bot")
  async def changelogs(self, interaction: Interaction):
    view = DropdownView()
    await interaction.send("View the Changelogs:", view=view, ephemeral=True)

  @nextcord.slash_command()
  async def plans(self, interaction: Interaction):
    ###Edit changelogs to fit the changes
    embed = nextcord.Embed(title="Bot Plans :scroll:", description='Da Plans for the bot', color=nextcord.Color.magenta())
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
    embed.add_field(name="Completed:", value="Heres a list of stuff that we completed since last time:\n**Migrated to Nextcord**\nEven though the developer of Discord.py came back it was too late for all that shit\n\n**Slash Commands**:\n turns out that after april we could still use prefixes... oh well. fuck discord for lying like they always do.", inline=True)
    embed.add_field(name="Buttons?", value="fuck buttons. the end.", inline=True)
    embed.add_field(name="Voice Chat support", value=f"The Next Update to {self.bot.user.name} should Primarily focus on getting Voice Chat to work. basically working like a music bot.")
    embed.add_field(name="Cut the mic", value="Thats about it for now. Cya", )
    embed.add_field(name="From", value="Derrick and Aiire!")
    await interaction.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Changelogs(bot))
