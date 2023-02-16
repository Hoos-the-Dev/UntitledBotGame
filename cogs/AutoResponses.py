from cgitb import text
from email.mime import application, image
from unicodedata import name

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
import json

import resources.functions as func

async def B_GetMemberPermissions(self, member, channel):
    permissions = channel.permissions_for(member)
    return permissions

class AutoResponse(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    sender = message.author
    msg = message.content
    
    high_chance = await func.B_RandomChance(50)
    mid_chance = await func.B_RandomChance(25)
    low_chance = await func.B_RandomChance(1)
    rare_chance = await func.B_RandomChance(0.5)
    really_low_chance = await func.B_RandomChance(0.1)

    if sender.bot: return

    if message.guild == None:

      if "flam files" in msg.lower():
        flamfiles = self.bot.get_channel(978692091783811112)
        await message.reply("Submitted for the flam files.")
        await flamfiles.send(message.attachments[0].url)
        await flamfiles.send(f"Sent in by: {sender.mention}")
      else:
        channel = self.bot.get_channel(976544625407950848)
        embed = nextcord.Embed(title="Sent a message", description=f"here the @ if you want to message them directly: {sender.mention}", color=nextcord.Color.random())
        embed.add_field(name="Message:", value=f'"{msg}"')
        func.B_SetEmbedAuthor(embed, sender)

        await channel.send(embed=embed)
        await channel.send(message.attachments[0].url)    
    first = msg.lower()
    second = func.B_DeleteSpaces(first)
    third = func.B_DeleteApostrophes(second)
    fourth = func.B_DeletePunctuation(third)
    fifth = func.B_DeleteExclamation(fourth)

    if fifth == "pingtest":
      embed = nextcord.Embed(title="has initiated a ping test", color=nextcord.Color.random()); embed.set_author(name=sender.name, icon_url=sender.avatar)
      embed.add_field(name="Latency:", value=f"{round(self.bot.latency * 1000)}ms")
      await message.reply(embed=embed)

    if message.author.id == 806383966969790494 and mid_chance == True:
      gerald = ["fuck off gerald", "gtfo out of here old man", "go home", "Careful gramps, you might pull a muscle if you keep talking"]
      await message.reply(random.choice(gerald)); return

    cock = {"1":"cock", "2":"penis", "3":"penia", "4":"dick", "5":"schlong", "6":"weiner", "7":"glizzy"}
    if msg.lower() == cock.values() and high_chance == True:
      got_a_feeling = "I've got a feeling you're gonna love it down here."
      ayo = ["pause", "AYO?", ":chicken:", "✝️", '"Wanna repeat that?" - 😈', f'"{got_a_feeling}" - 😈', f'"Choose your words wisely, {sender.name}." - 👿', '"Well in that case, you belong down here with me." - 👿', f"{sender.name} sus asf, ngl"]
      if low_chance == True:
        await message.reply("😏", delete_after=3)
      else:
        await message.reply(random.choice(ayo))
    
    if ('gigachad' in msg or 'sigma male' in msg) and mid_chance == True:
      chad_gifs = ["https://tenor.com/view/gigachad-chad-gif-20773266", "https://tenor.com/view/giga-chad-gif-25088911", "https://c.tenor.com/g1I3SMOUegMAAAAM/gigachad-minecraft-meme.gif", "https://tenor.com/view/valorant-giga-chad-valorant-yes-i-play-valorant-gif-25672461", "https://c.tenor.com/DHcPJYKlKxEAAAAM/gigachad-nightmare315.gif", "https://tenor.com/view/gigachad-nightmare315-gif-24908881"]
      await message.reply(random.choice(chad_gifs))

    if message.author.id == 164061868741099520 and low_chance == True:
      if "False" in json.load(open('giotoggle.json', 'r')): return
      gio = ["shut the fuck up gio", "please be quiet", "bro stfu you like men", "your dick small as shit", "you deserve to be made a tree ornament, pre 1860's style", "omfg SHUT THE FUCK UP ALREADY GIO", "talk all that shit for someone whos dick is smaller than a gorilla'. full size",
      "hey so like whats that prank in your favorites," "hey so what about that 'thing' thats under your bed"]
      await message.reply(random.choice(gio))
      return

    if sender.id == 367009505403338752 and low_chance == True:
      ant = ["heyyyyy antony", "heyyyy ant.", "ur so fucking cute", "ur hair is amazing", "you have such a big cock." "forget ur brother, ur so better than him.", "daddy ant just spoke", "ughhhhh ur so fucking cute <:SM_ahegao:597478334678433793>", ":smirk:"]
      await message.reply(random.choice(ant))
      return

    if message.author.id == 365250952480948234:
      giosbs = ["idon'tlikemen", "idontlikeguys", "imstraight", "imnotgay"] 
      first = msg.lower()
      second = func.B_DeleteApostrophes(first)
      third = func.B_DeletePunctuation(second)
      fourth = func.B_DeleteExclamation(third)
      fifth = func.B_DeleteSpaces(fourth)
      if fifth in giosbs:
        reply = ["stop lying", "ay gio isn't this you bro https://i.imgur.com/na6kc2P.png", "🧢", "stop the cap", "so if we check your favorites, that statement would add up right?", "not only are you gay but your dick small asf", "Antony >>>", "ay bro dont you have erectile dysfunction?", "bro you literally dream about getting dicked down by sean", "https://i.imgur.com/S39TGgF.png", "https://cdn.discordapp.com/attachments/890725952001277993/902967075457368104/IMG_3079.jpg", "bro children????"]
        if random.choice(reply) == "bro children????":
          await message.reply("https://media.discordapp.net/attachments/900122880673718302/978675413544996914/IMG_2517.png")
          await message.reply("<@365250952480948234> ^^^^^ bro wtf")
        await message.reply(random.choice(reply))
        return
      if sender.id == 365250952480948234:
        giosbs = ["imnot", "imnotttt"]
        first = msg.lower()
        second = func.B_DeleteApostrophes(first)
        third = func.B_DeletePunctuation(second)
        fourth = func.B_DeleteExclamation(third)
        fifth = func.B_DeleteSpaces(fourth)
        if fifth in giosbs:
          reply = ["YOU KEEP LYING BITCH", "JUST EMBRACE IT DICK HEAD", "BRO STOP THE CAP", "BUT YOU REALLY ARE", "YOU GET A BONER WHEN YOU THINK ABOUT SEAN FUCKING YOU", "anything for takis right?"] 
          await message.reply(random.choice(reply))
      if sender.id == 365250952480948234:
        if message == "rigged":
          reply = ["rigged where bitch,", "no, you're just really gay", "you'd get head from taylor, its not rigged", '```py\n@nextcord.slash_command(name="gayrate", description="see how gay you or someone else is (no homo)")\nasync def gayrate(self, interaction:Interaction, member: nextcord.User=SlashOption(name="user", description="whos gay rate youre checking", required=True)):\nyouoris = ""\nif member.id == interaction.user.id: youoris = ", you are"\nelse: youoris = " is"\nawait interaction.send(f"{member.name}{youoris} {randint(0, 100)}% gay")\n```']
          await message.reply(random.choice(reply))
      if sender.id == 365250952480948234:
        if ("takis" or "taki" or "tak8s" or "tak8") in msg:
          channel = self.bot.fetch_channel(message.channel.id)
          await message.delete()
          await channel.send("you are in rehab. no takis")


    Nicknames = ['bongo', "dingus", "binnus"]
    bot_name = self.bot.user.name
    if ("bongo" or "dingus" or "binnus") in message.content:
      bot_name = Nicknames
    response = {
      f"hi {bot_name}" : [f"Hi, {sender.name}", f"Hello, {sender.name}", f"What's up, {sender.name}", f"Yo", f"Hola {sender.name}", "wassup"],
      f"fuck {bot_name}" : ["TF I DO TO YOU??", f"man fuck you too {sender.name}", "ya motha", "wanna talk all that shit for a dude with a small dick", "Ima scratch the living shit out of you", "stfu", "shut up hoe", "you suck so much dick its not even funny", ""],
      f"{self.bot.user.mention}" : ["fuck off", "what the fuck do you want", "leave me alone", "can you not", "???", "Yes?", "do you have nothing better to do?", "https://i.imgur.com/HucQJmE.jpeg", "🔫", "What."],
      f"kys {bot_name}" : ["There's been a misunderstanding... I'm not the guy who shat in your cereal this morning!", "I'm gonna sratch the living shit out your face!", "ever heard of sounding? :smiling_imp:"],
      "jaden has erectile dysfunction": ["DAMN THATS WILD 💀", "DAMN JADEN YOU GONNA LET THEM TAlK TO YOU LIKE THAT?", "Personally I wouldn't let that slide.", "JIT GOIN CRAZY"],
      "you get no bitches": ["but where are yours?",  f'"{msg}" -:clown:', '🤓', 'send user hoe count'], # quoting the message
      f"screw {bot_name}" : ["well screw you too", "Just because I'm a bot, that doesn't mean I can't throw hands :fist:"],
      "I get bitches": ["your sister doesn't count, unfortunately", "Didn't I just see a video of you in bed with another dude???", ":billed_cap:", "good one :joy:", "Anime waifus don't count, sorry to say", f"No {sender.name}, your hand doesn't count.", "You know your minecraft girlfriend spawned in your bestfriends house, right?"],
      f"love you {bot_name}" : [":heart:", "ilyt <3", "awww", "prove it by cleaning my litterbox"],
      "goku solos" : ["if you're so eager to start a war, go on twitter", "can you shut the fuck up already", "yo can we time this bozo out already?", "🤓", "facts bro"],
      f"is {bot_name} sentient": ["gotta blast :brain:", "I'm not sentient", "I'm just a bot", "I gotta go....", "I'm outta here", "uhhhhhhhhhhh...", "No.", ":new_moon_with_face:"],
    }

    # Alternate input
    response[f"hey {bot_name}"] = response[f"hi {bot_name}"]
    response[f"hello {bot_name}"] = response[f"hi {bot_name}"]
    response[f"yo {bot_name}"] = response[f"hi {bot_name}"]
    response[f"whats up {bot_name}"] = response[f"hi {bot_name}"]
    response[f"what's up {bot_name}"] = response[f"hi {bot_name}"]
    response[f"wsp {bot_name}"] = response[f"hi {bot_name}"]
    response[f"wassup {bot_name}"] = response[f"hi {bot_name}"]
    response[f"whats good {bot_name}"] = response[f"hi {bot_name}"]
    response[f"what's good {bot_name}"] = response[f"hi {bot_name}"]
    response[f"wsg {bot_name}"] = response[f"hi {bot_name}"]
    response[f"bonjour {bot_name}"] = response[f"hi {bot_name}"]
    response[f"bonsoir {bot_name}"] = response[f"hi {bot_name}"]
    response[f"hola {bot_name}"] = response[f"hi {bot_name}"]
    response[f"aloha {bot_name}"] = response[f"hi {bot_name}"]
    response[f"love {bot_name}"] = response[f"love you {bot_name}"]
    response[f"ily {bot_name}"] = response[f"love you {bot_name}"]

    response[f"fuck you {bot_name}"] = response[f"fuck {bot_name}"]
    response[f"screw you {bot_name}"] = response[f"screw {bot_name}"]
    response[f"you sentient {bot_name}"] = response[f"is {bot_name} sentient"]
    response[f"stfu {bot_name}"] = response[f"fuck {bot_name}"]
    response[f"{bot_name} is a bitch"] = response[f"fuck {bot_name}"]


    for say in list(response.keys()):
      if say.lower() in msg.lower():
        reply = random.choice(response[say])
        if reply == 'send user hoe count':
          embed = nextcord.Embed(name=f"A list of {sender.name}'s bitches", description="\n")
          embed.add_field(text="\n", value="Unsurprisingly this list is empty*")
          await message.reply(embed=embed)
        else:
          await asyncio.sleep(random.randrange(0, 3))
          await message.reply(random.choice(response)); return

      vschannel = self.bot.get_channel(977229937259995168)

    if "prod.liveshare.vsengsaas.visualstudio.com" in msg:
      if not func.B_IsMemberOwner(self, sender):
        return
      else:
        embed = nextcord.Embed(title="sent a liveshare link", description=f"heres the [link]({msg})", color=nextcord.Color.random())
        func.B_SetEmbedAuthor(embed, sender)
        await message.delete()
        await vschannel.send(embed=embed)

def setup(bot):
    bot.add_cog(AutoResponse(bot)) 