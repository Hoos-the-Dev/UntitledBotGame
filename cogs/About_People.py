from selectors import SelectorKey
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Embed

class Dropdown(nextcord.ui.Select):
    def __init__(self):
      selectoptions = [
        nextcord.SelectOption(label="Flam", description="papi flam"),
        nextcord.SelectOption(label="Spaghettios", description="JAMES"),
        nextcord.SelectOption(label="Benny Boy", description="renee?"),
        nextcord.SelectOption(label="baguetee", description="The Inner Mac and Cheese of her mind is an enigma"),
        nextcord.SelectOption(label="Mediocre", description="What happens when you mix FNF, 2k22, and Roblox together"),
        nextcord.SelectOption(label="Antony", description="is not associated with Flam"),
        nextcord.SelectOption(label="Sheen", description="nice hair"),
        nextcord.SelectOption(label="Lucid", description="Derricks Cousin"),
        nextcord.SelectOption(label="soup", description="BRI"),
        nextcord.SelectOption(label="Aiire", description="NPC that is tree"),
        nextcord.SelectOption(label="Lost", description="child prodigy"),
        nextcord.SelectOption(label="Derrick", description="who you callin tubby?"),
        nextcord.SelectOption(label="Hoo", description="child prodigy but tech support"),
        nextcord.SelectOption(label="Slim-Z", description="he went to dorney park for free, because he was smart"),
        nextcord.SelectOption(label="Skybound", description="how's the weather down there?"),
        nextcord.SelectOption(label="ysa", description="pookie gone wild"),
        nextcord.SelectOption(label="Forxmify", description="forxmify ≠ Christian"),
        nextcord.SelectOption(label="Jahames", description="not a chubby hispanic, just big boned")
      ]
      super().__init__(placeholder='Click to select a Person', min_values=1, max_values=1, options=selectoptions)
    async def callback(self, interaction: Interaction):
      if self.values[0] == "Flam":
        embed = nextcord.Embed(title="About Flam", description="Flam is the online identity of Giovanni. He's tall, says the n word, has a small dick, and sometimes kind")
        embed.add_field(name="Sexuality:", value="Flam is confused ¯\_(ツ)_/¯")
        embed.add_field(name="Age:", value="15. nearly legal...")
        embed.add_field(name="Favorite Games:", value="2K22, Roblox (ABA, YBA, GPO, etc)")
        embed.add_field(name="Relationships:", value="Antony181 = *not associated with*, Sheen = Ex, benny boy = Crush/Hate")
        embed.add_field(name="Ethnicity: Confused", value="Hispanic")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Spaghettios":
        embed = nextcord.Embed(title="About sphagetti0s", description="spaghetti0s (also known as james) is the online identity of Rylee. She's not tall but not short, dream smp / ranboo enjoyer, apartment owner, and a bit quiet but we still love her!")
        embed.add_field(name="Sexuality:", value="unlabled")
        embed.add_field(name="Age:", value="7")
        embed.add_field(name="Favorite Games:", value="minecraft?")
        embed.add_field(name="Relationships:", value="soup and baguetee = Bestie")
        embed.add_field(name="Ethnicity:", value="White")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Benny Boy":
        embed = nextcord.Embed(title="About benny boy", description="benny boy is known IRL as Renee. She's chubby and racist. thats it")
        embed.add_field(name="Sexuality:", value="lesbian")
        embed.add_field(name="Age:", value="16")
        embed.add_field(name="Favorite Games:", value="valorant, roblox, and maybe minecraft")
        embed.add_field(name="Relationships:", value="baguetee = Sister, Ashiro = Lover :heart_eyes:, Flam = hates")
        embed.add_field(name="Ethnicity:", value="Asian")
        await interaction.send(embed=embed, ephemeral=True) 
      elif self.values[0] == "baguetee":
        embed = nextcord.Embed(title="About baguetee", description="baguetee is known as beaky IRL, she is shy and barely talks but is still really nice!!")
        embed.add_field(name="Sexuality:", value="straight(?)")
        embed.add_field(name="Age:", value="14 or 15")
        embed.add_field(name="Favorite Games:", value="osu!")
        embed.add_field(name="Relationships:", value="benny boy = sister")
        embed.add_field(name="Ethnicity:", value="Asian")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Mediocre":
        embed = nextcord.Embed(title="About mediocre_", description="_mediocre is known as Alec irl. He's not short but not tall, hot, and a fucking fiend. yeah he's mediocre :unamused:")
        embed.add_field(name="Sexuality:", value="Demisexual")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="2K22, FNF, Roblox (Arsenal)")
        embed.add_field(name="Relationships:", value="Antony181 = Friend, Flam = Friend, Hoo = Friend")
        embed.add_field(name="Ethnicity:", value="filipino")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Lucid":
        embed = nextcord.Embed(title="About Lucid", description="Lucid aka Mikey has been annoying me about this fucking command since i made the Flam command. Hes an elf, weird and something else im not saying here. His nsfw list is not to be mentioned as it might throw him in jail")
        embed.add_field(name="Sexuality:", value="Bi")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="The games on his phone, and Spiderman for PS5")
        embed.add_field(name="Relationships:", value="Derrick = cousin. Crushes = too many to list")
        embed.add_field(name="Ethnicity:", value="Black")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Sheen":
        embed = nextcord.Embed(title="About Sheen", description="Sheen / Sean is nearly tall, ginger with long curly hair, and on the verge of being racist")
        embed.add_field(name="Sexuality:", value="heh :smirk:")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="roblox (YBA, GPO, ABA)")
        embed.add_field(name="Relationships:", value="soup = great friend, ETHYNEL = secret lover")
        embed.add_field(name="Ethnicity:", value="White")
        await interaction.send(embed=embed, ephemeral=True) 
      elif self.values[0] == "soup":
        embed = nextcord.Embed(title="About soup", description="soup aka brianna is smol, blonde, and very interesting")
        embed.add_field(name="Sexuality:", value="Bisexual")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="Roblox")
        embed.add_field(name="Relationships:", value="spaghetti0s = besties, Sheen = a very good freind")
        embed.add_field(name="Ethnicity:", value="i was just told that she was brazilian but idk that for sure")
        await interaction.send(embed=embed, ephemeral=True) 
      elif self.values[0] == "Lost":
        embed = nextcord.Embed(title="About Lost", description="Lost / Nana is a child prodigy, elitist, and weeb.")
        embed.add_field(name="Sexuality:", value="Straight")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="i dont know")
        embed.add_field(name="Relationships:", value="Flam = Friend, Antony181 = Friend, Ashiro = Friend.")
        embed.add_field(name="Ethnicity:", value="isn't ethnicity your culture, not skin tone?")
        await interaction.send(embed=embed, ephemeral=True)  
      elif self.values[0] == "Hoo":
        embed = nextcord.Embed(title="Hoos that?:face_with_raised_eyebrow:", description="Nah but Hoo / Matthew is another Child Prodigy. He's open to try anything, blender fiend, votech non, and is petrified by frickin dolphins. :dolphin:")
        embed.add_field(name="Sexuality:", value="Bisexual")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="none, he literally uses blender all day")
        embed.add_field(name="Relationships:", value="Derrick = Friend, Antony181 = Friend, Flam = Friend, Audacity = Friend, Karen Chan = Technical Support Brother")
        embed.add_field(name="Ethnicity:", value="Indian")
        embed.set_footer(text="🐬")
        await interaction.send(embed=embed, ephemeral=True)   
      elif self.values[0] == "Derrick":
        embed = nextcord.Embed(title="About Derrick", description="Derrick aka Aurora Rpg online is literally the creator of Bingus Bot")
        embed.add_field(name="Ok but a brief description:", value="Tall, nerd, and does alot. he does coding, and video editing. how did i get myself to where i am right now. oh im also fat")    
        embed.add_field(name="Sexuality:", value="guys im straight, i swear. :flushed:")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="Minecraft, Roblox, osu!, After Effects:cry:")
        embed.add_field(name="Relationships:", value="Friends = nearly everyone in this server")
        embed.add_field(name="Ethnicity:", value="i dont even know but im black.. NIG-")
        await interaction.send(embed=embed, ephemeral=True)  
      elif self.values[0] == "Aiire":
        embed = nextcord.Embed(title="About Aiire", description="Aiire aka Jaden irl, is shy and tall and always wears his jacket even in the heat")
        embed.add_field(name="Sexuality:", value=":new_moon_with_face:")
        embed.add_field(name="Age:", value="15, the new 22")
        embed.add_field(name="Favorite Games:", value="Minecraft, Roblox, others he never speaks of (www.srb2.org)")
        embed.add_field(name="Relationships:", value="Little bro = Rou, Homies = Versailles, Sheen, Lucid, etc")
        embed.add_field(name="Ethnicity:", value="Black")
        await interaction.send(embed=embed, ephemeral=True)  
      elif self.values[0] == "Antony":
        embed = nextcord.Embed(title="About Antony", description="Antony is a pretty tall guy with curly hair and an unrelated twin brother who feinds for Anigame and figured out how to capitalize off of it somehow")
        embed.add_field(name="Sexuality:", value="Straight")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="2K, Roblox, Anigame")
        embed.add_field(name="Relationships:", value="*Not Associated with*: Flam. Matthew, Alec, Pranay, Jeremy, Nana, Andrei, Derrick, and more: Friends")
        embed.add_field(name="Ethnicity:", value="Dominican Republic")
        await interaction.send(embed=embed, ephemeral=True) 
      elif self.values[0] == "Slim-Z":
        embed = nextcord.Embed(title="About Zlim-C", description="Slim-Z aka Benjamin is um ✨unique✨, and literally went to dorney park for free. im jealous of him")
        embed.add_field(name="Sexuality:", value="idk what he is but it aint straight")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="Unreal Engine and Minecraft")
        embed.add_field(name="Relationships:", value="Matthew, Alec, Pranay, Jeremy, and Derrick. prolly more but im lazy")
        embed.add_field(name="Ethnicity:", value="mans a half breed (European / Asian)")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Skybound":
        embed = nextcord.Embed(title="About Skybound", description="Skybound aka taylor is a pretty cool guy, he's a pretty good artist (well i think), has a napoleon complex, being 4'11 isnt easy.")
        embed.add_field(name="Sexuality:", value="check <#1019954279211077669> and come to your own answer")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="Basketball, Roblox")
        embed.add_field(name="Relationships:", value='"iTs mE aGaInSt ThE wOrLd"')
        embed.add_field(name="Ethinicity:", value="NI-")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] ==  "ysa":
        embed = nextcord.Embed(title="About Ysa", description="YSA IS DAT FILIPINA GURLL ONG. she does ✨acting✨, and just hangouts in the discord. you'll probably find her lost asf. best sugar mommy ong. mommy-.")
        embed.add_field(name="Sexuality:", value="Filipino")
        embed.add_field(name="Age:", value="16 *how tf is she older than me 😭*")
        embed.add_field(name="Favorite Games:", value="Filipino, UNOfficial")
        embed.add_field(name="Relationships:", value='My Mans: Her bf, Cycide: Opp, Forxmify: Opp, Taylor: pookieeeee, Derrick: ppoooookie')
        embed.add_field(name="Ethinicity:", value="Filipina")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Forxmify":
        embed = Embed(title="About Forxmify", description="Forxmify or Christian in da real world has curly hair. nice eyes, and is not the same person irl as he is in discord. we love christian!")
        embed.add_field(name="Sexuality:", value="Straight")
        embed.add_field(name="Age:", value="idfk")
        embed.add_field(name="Favorite Games:", value="Minecraft, Roblox, Among us (espeically with us)")
        embed.add_field(name="Relationships:", value="Friends = Ysa, Cycide, Taylor, Derrick, and more WEEEEE")
        embed.add_field(name="Ethinicity:", value="HE WHITE BOIIIII (idk his ethnicity)")
        await interaction.send(embed=embed, ephemeral=True)
      elif self.values[0] == "Jahames":
        embed = Embed(title="About what ever the fuck his name is rn", description="Jahames aka JAMES is a bulky man with nice hair and wears red,a lot.")
        embed.add_field(name="Sexuality:", value="Straight")
        embed.add_field(name="Age:", value="15")
        embed.add_field(name="Favorite Games:", value="roblox")
        embed.add_field(name="Relationships:", value="This huggable teddy bear is friends with everyone")
        embed.add_field(name="Ethinicity:", value="Hispanic")
        await interaction.send(embed=embed, ephemeral=True)
      
class DropdownView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Dropdown())


class About(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  testServerId = 937841015648292934
  @nextcord.slash_command(name="about", description="About a person")
  async def about(self, interaction: Interaction):
    view = DropdownView()
    await interaction.send("Who do you want to learn about?:", view=view)
      
def setup(bot):
    bot.add_cog(About(bot))