from email.mime import application, image
import imp

from pip import main
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from urllib import response
from nextcord import Member
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption
import asyncio
import requests
import random
from random import randint
import humanfriendly
import aiohttp
from datetime import datetime as dt
from lib import *

def B_DeleteSpaces(string:str):
  return string.replace(" ", "")

def B_DeletePunctuation(string:str):
  return string.replace(".", "")

def B_DeleteExclamation(string:str):
  return string.replace("!", "")
  
def B_StringMask(string:str, old:str, new:str):
  return string.replace(old, new)

def B_CheckBlacklist(self, member:nextcord.Member):
  return member.id in blacklist

def B_IsMemberOwner(self, member:nextcord.Member):
  return member.id in botowners.values()

def B_DeleteApostrophes(string:str):
  return string.replace("'", "")
  
async def B_RandomChance(chance:int):
  if random.random() < (chance / 100):
    return True

  return False

def B_DictToList(table:dict):
    lines = f'\n{list(table.values())}'
    lines = B_StringMask(lines, "'", "")
    lines = B_StringMask(lines, ",", "")
    lines = B_StringMask(lines, "[", "")
    lines = B_StringMask(lines, "]", "")
    return lines


async def B_BlacklistEmbed(self, interaction:Interaction, commandname:str, pagenumber=randint(90, 150)):
  blacklist = nextcord.Embed(title="Oh hell no", description=f"According to **The Official {self.bot.user.name} Handbook**, it says here on **page {pagenumber}** that you, **{interaction.user.name}**, have been blacklisted from using ANY kind of administrator commands... NEXT TIME, THINK BEFORE YOU ACT!", color=nextcord.Color.red())
  await interaction.send(f"So anyways, {interaction.user.mention}, it looks like you can't use the ``{commandname}`` command, here's why", embed=blacklist)

def B_SetEmbedAuthor(embed, member:nextcord.Member, thumbnail=bool):
  if member.guild_avatar:
    if thumbnail == True:
      embed.set_thumbnail(url=member.guild_avatar)
    else:
      embed.set_author(name=member.display_name, icon_url=member.guild_avatar)
  else:
    if thumbnail == True:
      embed.set_thumbnail(url=member.avatar)
    else:
      embed.set_author(name=member.display_name, icon_url=member.avatar)

def B_CheckHorniJail(self, member):
  return member.id in hornijail

def B_AddHorniJail(self, member:nextcord.Member):
  hornijail[member.id] = member.mention

def B_CreateEmbed(title, description, color):
  embed = nextcord.Embed(title=title, description=description, color=nextcord.Color(color))
  return embed

def B_Lower(string:str):
  return string.lower()

clock = dt.now().strftime("%H:%M")
date = dt.now().strftime("%d/%m/%Y")
