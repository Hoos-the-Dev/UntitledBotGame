import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime
import humanfriendly

class Dropdown(nextcord.ui.Select):
    def __init__(self):
      selectoptions = [
        nextcord.SelectOption(label="The School Shooting Threat", description="April 27th 2022"),
        nextcord.SelectOption(label="The Stabbing?", description="April 27th 2022"),
        nextcord.SelectOption(label="The Dance!", description="April 27th 2022"),
        nextcord.SelectOption(label="Summer Jobs Announced!", description="April 28th 2022"),
        nextcord.SelectOption(label="THERE WAS A GUNSHOT?!", description="September 19th 2022"),
      ]
      super().__init__(placeholder='Click to select an Event', min_values=1, max_values=1, options=selectoptions)
    async def callback(self, interaction: Interaction):
      if self.values[0] == "The School Shooting Threat":
        embed = nextcord.Embed(title="The School Shooting threat", description="April 26th 2022... someone threated to shoot up the high school, leaving us in lockdown for nearly an hour during state testing", color=nextcord.Color.red())
        embed.set_footer(text="Updated on April 27th, 2022")
        embed.add_field(name="Sources:", value="Word of Mouth at HHS")
        Derrick = interaction.guild.get_member(164061868741099520)
        embed.set_author(name="Derrick", icon_url=Derrick.avatar)
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "The Stabbing?":
        embed = nextcord.Embed(title="The Stabbing 🔪?", description="April 27th 2022... A group of seniors beat up and stabbed a special ed kid nammed Maryland. The Result? Maryland's jaw was broken, and bleeding out since he was stabbed in the eye. leaving a weird feeling amongst the rest of the students", color=nextcord.Color.red())
        embed.add_field(name="April 27th 2022, Update:", value="The Police and Security Guards called home saying that there was no weapon involved. Which is good. Though it was a fight. Denying what people might of said about either a stabbing or Maryland running into a locker")
        embed.add_field(name="Sources:", value="-[RLSMedia](https://www.rlsmedia.com/article/significant-injuries-reported-student-jumped-inside-bathroom-hillside-high-school)\n -The Students of HHS")
        embed.set_footer(text="Last Updated on April 27th, 2022")
        Derrick = interaction.guild.get_member(164061868741099520)
        embed.set_author(name="Derrick", icon_url=Derrick.avatar)
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "The Dance!":
        embed = nextcord.Embed(title="The Dance! 🎉", description="Enough Negativity. Let's get this party started! The School Dance is happening this week! Its $7 for the ticket, You can pay with either Cash or CashApp. Cant wait to see you there if you go!", color=nextcord.Color.random())
        embed.add_field(name="Update:", value="it got postponed. Date:\nTBD")
        embed.set_footer(text="Last Updated on May 7th, 2022")
        Derrick = interaction.guild.get_member(164061868741099520)
        embed.set_author(name="Derrick", icon_url=Derrick.avatar)
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Summer Jobs Announced!":
        embed = nextcord.Embed(title="Summer Jobs Announced! 💸", description="The summer jobs have been announced! The Current Options for a summer job with there nesscessary details are:", color=nextcord.Color.random())
        embed.add_field(name="Student Technology Assistant ", value="**Details**: \n\n **Job Requirements**:\n -Knowledge of computer systems, including Hardware & Software.\n -Assist with troubleshooting, installation of new programs.\n -Must be student of Hillside High School.\n\n **Salary**:\n $13/h", inline=True)
        embed.add_field(name="Custodian", value="**Details**: \n\n **Job Requirements**:\n -Be able to clean shit...\n -Must be student of Hillside High School.\n\n **Salary**:\n -$13/h", inline=True)
        embed.add_field(name="Interested? Apply Today!", value="Check out the recruitment email in your hillsidek12 email! The Email sent out by Randal McMcoy will have a orange button to apply. If you have any questions, dont ask me!", inline=True)
        embed.set_footer(text="Last Updated on April 28th, 2022")
        Derrick = interaction.guild.get_member(164061868741099520)
        embed.set_author(name="Derrick", icon_url=Derrick.avatar)
        await interaction.send(embed=embed, ephemeral=True)


class DropdownView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Dropdown())


class HSEvents(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  testServerId = 937841015648292934
  InsaneAsylum = 880866540906508289
  @nextcord.slash_command(name="events", description="The Events and Incidents at HHS", guild_ids=[InsaneAsylum, testServerId])
  async def events(self, interaction: Interaction):
    view = DropdownView()
    await interaction.send("What event do you want to learn about?:", view=view)

      
def setup(bot):
    bot.add_cog(HSEvents(bot))
