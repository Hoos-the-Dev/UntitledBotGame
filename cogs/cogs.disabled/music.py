from re import A
import nextcord
from nextcord.ext import commands
from nextcord import ApplicationInvokeError, Embed, Interaction
import asyncio
import youtube_dl
import random
import resources.console as console


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': "bestaudio"}


RequesterBlacklist = {

}


song_queue = []
requeste = []

def shuffle_queue():
      temp = []
      temp2 = []
      for i in range(len(song_queue)):
          temp.append(song_queue[i])
          temp2.append(requeste[i])
      queuedotzip = list(zip(temp, temp2))
      random.shuffle(queuedotzip)
      temp, temp2 = zip(*queuedotzip)
      for i in range(len(song_queue)):
          song_queue[i] = temp[i]
          requeste[i] = temp2[i]

def update_queue():
        song_queue.pop(0)
        requeste.pop(0)


async def play_next(ctx: commands.Context):
  if len(song_queue) == 0:
    embed = Embed(title="That's all folks", description="The queue has finished playing", color=nextcord.Color.red())
    await ctx.send(embed=embed)
    console.printf("Queue finished playing")
    return None
  song = song_queue[0]
  if  "http" not in song:
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(f"ytsearch:{song}", download=False)
      url2 = info['entries'][0]["formats"][0]['url']
      video_title = info.get('entries')[0].get('title')
      Author = info.get('entries')[0].get('uploader')
      source = await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable="D:\\Bingus Rewrite\\ffmpeg\\bin\\ffmpeg.exe")
      ctx.voice_client.play(source, after=lambda x=None: play_next(ctx))
      embed = Embed(title="Now Playing", description=f"{video_title}", color=nextcord.Color.blurple())
      embed.set_footer(text=f"Uploader: {Author} | Requested by {requeste[0]}")
      await ctx.send(embed=embed)
      update_queue()
      console.printf(f"Now Playing: {video_title}")
  else:
    console.printf("Playing from URL")
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(song, download=False)
      try:
        url2 = info['formats'][0]['url']
      except:
        url2 = info['entries'][0]['url']
      source = await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable="D:\\Bingus Rewrite\\ffmpeg\\bin\\ffmpeg.exe")
      ctx.voice_client.play(source, after=lambda x=None: play_next(ctx))
      embed = Embed(title="Now Playing", description=f"{info['title']}", color=nextcord.Color.blurple())
      Author = info.get('entries')[0].get('uploader')
      embed.set_footer(text=f"Uploader: {Author} | Requested by {requeste[0]}")
      await ctx.send(embed=embed)
      update_queue()
      console.printf(f"Playing {info['title']}")

# async def play_eboy(ctx: commands.Context):
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   song_queue.append("moaning e boy")
#   requeste.append(f"FUCK YOU! LISTEN TO MOANING EBOYS")
#   if len(song_queue) == 0:
#     embed = Embed(title="That's all folks", description="The queue has finished playing", color=nextcord.Color.red())
#     await ctx.send(embed=embed)
#     console.printf("Queue finished playing")
#     return None
#   song = song_queue[0]
#   if  "http" not in song:
#     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
#       info = ydl.extract_info(f"ytsearch:{song}", download=False)
#       url2 = info['entries'][0]["formats"][0]['url']
#       video_title = info.get('entries')[0].get('title')
#       source = await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable="D:\\Bingus Rewrite\\ffmpeg\\bin\\ffmpeg.exe")
#       ctx.voice_client.play(source, after=lambda x=None: play_eboy(ctx))
#       embed = Embed(title="Now Playing", description=f"{video_title}", color=nextcord.Color.blurple())
#       embed.set_footer(text=f"Requested by {requeste[0]}")
#       await ctx.send(embed=embed)
#       update_queue()
#       console.printf(f"Now Playing: {video_title}")
#   else:
#     console.printf("Playing from URL")
#     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
#       info = ydl.extract_info(song, download=False)
#       try:
#         url2 = info['formats'][0]['url']
#       except:
#         url2 = info['entries'][0]['url']
#       source = await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable="D:\\Bingus Rewrite\\ffmpeg\\bin\\ffmpeg.exe")
#       ctx.voice_client.play(source, after=lambda x=None: play_eboy(ctx))
#       embed = Embed(title="Now Playing", description=f"{info['title']}", color=nextcord.Color.blurple())
#       embed.set_footer(text=f"Requested by {requeste[0]}")
#       await ctx.send(embed=embed)
#       update_queue()
#       console.printf(f"Playing {info['title']}")

class Music(commands.Cog):
  def __init__(self, bot):
      self.bot = bot



  @commands.command()
  async def join(self, ctx: commands.Context):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)


  @commands.command()
  async def leave(self, ctx: commands.Context):
    await ctx.voice_client.disconnect()

  @commands.command(aliases=["p"])
  async def play(self, ctx: commands.Context, *, url):
    resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
    if ctx.author.id in RequesterBlacklist:
      await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
    if ctx.voice_client is None:
      await ctx.author.voice.channel.connect()
    vc = ctx.voice_client
    if "list" in url:
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        for i in info['entries']:
          song_info = i['webpage_url']
          song = ydl.extract_info(song_info, download=False)
          video_title = song.get('title')
          song_queue.append(video_title)
          requeste.append(f"{ctx.author.name}#{ctx.author.discriminator}")
          console.printf(f"Added {i['title']} to the queue")
      embed = Embed(title="Added to queue", description=f"Added {len(info['entries'])} songs to the queue", color=nextcord.Color.green())
      await ctx.send(embed=embed)
      if not vc.is_playing():
        await play_next(ctx)
      return

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info(f"ytsearch:{url}", download=False)
      except:
        info = ydl.extract_info(url, download=False)
        Author = info.get('uploader')
        if "linechu asmr" in Author.lower():
          needhelp = ["go to hell", "you need jesus", "im not putting this on for you, demon.", "omfg you suck", "i hate you", "go to church"]
          embed = Embed(title="oh hell no", description=random.choice(needhelp), color=nextcord.Color.red())
          return await ctx.send(embed=embed)

    song_queue.append(url)
    requeste.append(f"{ctx.author.name}#{ctx.author.discriminator}")
    if not vc.is_playing():
      await play_next(ctx)
    elif vc.is_playing():
      embed = Embed(description=f"Added {url} to the queue", color=nextcord.Color.blurple())
      await ctx.send(embed=embed)



  #if song is age restricted send error message
  @play.error
  async def play_error(self, ctx: commands.Context, error):
    if isinstance(error, ApplicationInvokeError):
      await ctx.send("This video is age restricted and cannot be played")
  
  #if the user doesnt send a link send error message
  @play.error
  async def play_error(self, ctx: commands.Context, error):
    if isinstance(error, IndexError):
      await ctx.send("Please send a link to a song")
  
  @commands.command()
  async def pause(self, ctx: commands.Context):
    resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
    if ctx.author.id in RequesterBlacklist:
      await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
    ctx.voice_client.stop()
    ctx.voice_client.pause()
    await ctx.send("Music paused")
  
  @commands.command()
  async def resume(self, ctx: commands.Context):
    resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
    if ctx.author.id in RequesterBlacklist:
      await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
    ctx.voice_client.stop()
    ctx.voice_client.resume()
    await ctx.send("Music resumed")
  
  @commands.command()
  async def stop(self, ctx: commands.Context):
    resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
    if ctx.author.id in RequesterBlacklist:
      await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
    ctx.voice_client.stop()
    await ctx.send("Music stopped")

  @commands.command()
  async def skip(self, ctx: commands.Context):
    resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
    if ctx.author.id in RequesterBlacklist:
      await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
    ctx.voice_client.stop()
    embed = Embed(description=f"Skipped", color=nextcord.Color.red())
    await ctx.send(embed=embed)

  # @commands.command()
  # async def eboy(self, ctx: commands.Context):
  #   vc = ctx.voice_client
  #   vc.stop()
  #   song_queue.append("moaning e boy")
  #   requeste.append("YOU STARTED THIS")
  #   await play_eboy(ctx)

  @commands.command()
  async def progress(self, ctx: commands.Context):
    vc = ctx.voice_client
    source = vc.source
    position = source.position
    await ctx.send(f"Position: {position}")
  
  @commands.command(aliases=["q"])
  async def queue(self, ctx: commands.Context):
    if len(song_queue) == 0:
      embed = Embed(title="Queue", description="The queue is empty. use `-p` to play a song", color=nextcord.Color.red())
      await ctx.send(embed=embed)
      return
    embed = Embed(title="Queue", description=f"Upcoming Songs", color=nextcord.Color.blurple())
    for i in range(len(song_queue)):
      embed.add_field(name=f"{i+1}. {song_queue[i]}", value=f"Requested by {requeste[i]}", inline=False)

    await ctx.send(embed=embed)

  @commands.command()
  async def clear(self, ctx: commands.Context):
    song_queue.clear()
    requeste.clear()
    await ctx.send("Queue cleared")

  @commands.command()
  async def loop(self, ctx: commands.Context):
    vc = ctx.voice_client
    source = vc.source
    source.loop = True
    await ctx.send("Looping song")
  @commands.command()
  async def clear(self, ctx: commands.Context):
    song_queue.clear()
    requeste.clear()
    await ctx.send("Queue cleared")
  @commands.command()
  async def remove(self, ctx: commands.Context, *, number):
    song_queue.pop(int(number)-1)
    requeste.pop(int(number)-1)
    await ctx.send(f"Removed song {number} from queue")
  @commands.command()
  async def np(self, ctx: commands.Context):
    embed = Embed(title="Now Playing", description=f"{song_queue[0]}", color=nextcord.Color.blurple())
    embed.set_footer(text=f"Requested by {requeste[0]}")
    await ctx.send(embed=embed)
  @commands.command()
  async def shuffle(self, ctx: commands.Context):
    if len(song_queue) == 0:
      await ctx.send("i can't shuffle NOTHING DICHEAD")
      return
    shuffle_queue()
    embed = Embed(description=f"Shuffled the queue", color=nextcord.Color.dark_purple())
    await ctx.send(embed=embed)

  @commands.command()
  async def volume(self, ctx: commands.Context, volume: int):
    if ctx.voice_client is None:
      return await ctx.send("Not connected to a voice channel.")
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")
  
  @commands.command()
  async def move(self, ctx: commands.Context, pos1, pos2):
    song_queue.insert(int(pos2)-1, song_queue.pop(int(pos1)-1))
    requeste.insert(int(pos2)-1, requeste.pop(int(pos1)-1))
    await ctx.send(f"Moved {pos1} to {pos2}")

def setup(bot):
    bot.add_cog(Music(bot))
