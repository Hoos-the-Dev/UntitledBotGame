import nextcord
from nextcord import Interaction, SlashOption
import math
import typing
from typing import Optional
import random
from nextcord.ext import commands

async def B_MathematicalError(interaction:Interaction, error:str, text:str, ephemeral=bool):
  if error == None: error = "SYNTAX"
  embed = nextcord.Embed(title=f"***{error.upper()} ERROR***", description=text, color=nextcord.Color.red())
  await interaction.send(embed=embed, ephemeral=ephemeral)

async def B_ConversionFail(interaction:Interaction, text:str, ephemeral=bool):
  embed = nextcord.Embed(title="***CONVERSION FAILED***", description=text, color=nextcord.Color.red())
  await interaction.send(embed=embed, ephemeral=ephemeral)

def B_ConvertEmbed(interaction:Interaction, input:str, output:str, input_num:int, output_num:int):
  embed = nextcord.Embed(title="Converted!", color=nextcord.Color.random())
  embed.add_field(name="Input", value=f"{input_num} {input.lower()}")
  embed.add_field(name="Output", value=f"{output_num} {output.lower()}")

class Math(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  @nextcord.slash_command(name="calc", description="Calculate a math equation")
  async def calc(self, interaction: Interaction, operator: str = SlashOption(name="type", description="Math operator", choices=["Addition", "Subtraction", "Multiplication", "Division", "Power", "Modulo", "Square Root", "Cosine", "Sine", "Tangent", "Hypotenuse", "Cosine-²", "Sine-²"]), num1: float = SlashOption(name="num1", description="Integer", required=True), num2: float = SlashOption(name="num2", description="Integer", required=False)):
#    if num1 == None: await B_MathematicalError(interaction, "``num1`` option not provided!"); return

    if num2 == None:
       num2 = 0

    if operator == "Addition":
      await interaction.send(f"``{num1} + {num2} = {num1 + num2}``")
    elif operator == "Subtraction":
      await interaction.send(f"``{num1} - {num2} = {num1 - num2}``")
    elif operator == "Multiplication":
      await interaction.send(f"``{num1} * {num2} = {num1 * num2}``")
    elif operator == "Division":
      if num2 == 0: await B_MathematicalError(interaction, "Attempted to divide by zero!", "ZERO DIVISION"); return
      await interaction.send(f"``{num1} / {num2} = {num1 / num2}``")
    elif operator == "Power":
      await interaction.send(f"``{num1} ^ {num2} = {num1 ** num2}``")
    elif operator == "Modulo":
      await interaction.send(f"``{num1} % {num2} = {num1 % num2}``")
    elif operator == "Square Root":
      if num1 < 0: await B_MathematicalError(interaction, "Squares cannot be negative integers!", "MATH DOMAIN"); return
      await interaction.send(f"``√{num1} = {math.sqrt(num1)}``")
    elif operator == "Cosine":
      await interaction.send(f"``cos({num1}) = {math.cos(num1)}``")
    elif operator == "Sine":
      await interaction.send(f"``sin({num1}) = {math.sin(num1)}``")
    elif operator == "Tangent":
      await interaction.send(f"``tan({num1}) = {math.tan(num1)}``")
    elif operator == "Hypotenuse":
      await interaction.send(f"``hypot({num1}, {num2}) = {math.hypot(num1, num2)}``")
    elif operator == "Cosine-²":
      await interaction.send(f"``cos-²({num1}) = {math.cos(num1) ** 2}``")
    elif operator == "Sine-²":
      await interaction.send(f"``sin-²({num1}) = {math.sin(num1) ** 2}``")

  @nextcord.slash_command(name="randint", description="Send random number")
  async def randomint(self, interaction:Interaction):
    await interaction.send(f"``{random.random()}``")

  @nextcord.slash_command(name="pi", description="Send a 31.4 trillion number that happens to be a mathematical constant")
  async def math_pi(self, interaction:Interaction):
    await interaction.send(f"``π = {math.pi}...``")
    
def setup(bot):
    bot.add_cog(Math(bot))
 