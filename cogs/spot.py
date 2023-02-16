from re import A
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog, Context, command, has_permissions
from nextcord import ApplicationInvokeError, Embed, Interaction
import asyncio
import youtube_dl
import wavelink
from wavelink import Node, Player, Track, NodePool
from wavelink.ext import spotify
import random
import resources.console
import spotipy 

SPOTIFY_CLIENT_ID = "7ccdc6415d4b4596b1df027c18d70d49"
SPOTIFY_CLIENT_SECRET = "0f438af4f9c24fd8833bc8b54c36bc3a"



spot = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri="http://localhost:8888/callback", scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing,streaming,app-remote-control,playlist-read-private,playlist-read-collaborative,playlist-modify-public,playlist-modify-private,user-library-read,user-library-modify,user-read-recently-played,user-top-read,ugc-image-upload,user-follow-read,user-follow-modify,"))

#for youtube playback
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': "bestaudio"}


youtube_urls = ["youtube.com", "youtu.be", "www.youtube.com", "www.youtu.be"]


RequesterBlacklist = {

}


song_queue = {}
requeste = {}
np = {}
np_requester = {}

async def node_connect(self):
    await self.bot.wait_until_ready()
    await NodePool.create_node(bot=self.bot, host="10.0.0.52", port=2096, password="youshallnotpass", spotify_client=spotify.SpotifyClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
    
async def play_next(self, ctx: commands.Context):
    if len(song_queue) == 0:
        embed = Embed(title="That's all folks", description="The queue has finished playing", color=nextcord.Color.red())
        print("Queue finished playing")
        await ctx.send(embed=embed)
        return
    vc: Player = ctx.voice_client
    cs= str(song_queue[0])
    try:
        if cs.startswith("https://youtube.com") or cs.startswith("https://youtu.be") or cs.startswith("https://www.youtube.com"):
            song = await wavelink.YouTubeTrack.search(song_queue[0], return_first=True)
            np.append(song.title)
            np_requester.append(requeste[0])
            vc: Player = ctx.voice_client
            print(f"Attempted to play {song.title}")
            print(song)
            await vc.play(song)
            embed = Embed(title="Now Playing", description=f"{song.title}", color=nextcord.Color.blurple())
            embed.set_footer(text=f"Uploader: {song.author} | Requested by {requeste[0]}")
            await ctx.send(embed=embed)
            Song.update_queue()
            return
        if cs.startswith("https://music.youtube.com"):
            song = await wavelink.YouTubeMusicTrack.search(song_queue[0], return_first=True)
            np.append(song.title)
            np_requester.append(requeste[0])
            vc: Player = ctx.voice_client
            print(f"Attempted to play {song.title}")
            print(song)
            await vc.play(song)
            embed = Embed(title="Now Playing", description=f"{song.title}", color=nextcord.Color.blurple())
            embed.set_footer(text=f"Uploader: {song.author} | Requested by {requeste[0]}")
            await ctx.send(embed=embed)
            Song.update_queue()
            return
        if not cs.startswith("https://open.spotify.com/"):
            spot_song=spot.search(cs, limit=1, type="track")["tracks"]["items"][0]["uri"]
            track = await spotify.SpotifyTrack.search(query=spot_song, return_first=True)
            np.append(track.title)
            np_requester.append(requeste[0])
            await vc.play(track)
            embed = Embed(title="Now Playing", description=f"{track.title}", color=nextcord.Color.blurple())
            embed.set_footer(text=f"Requested by {ctx.author}")
            Song.update_queue()
            await ctx.send(embed=embed)
            return
        else:
            vc: Player = ctx.voice_client
            print("Spotify Link Detected")
            track = await spotify.SpotifyTrack.search(query=cs, return_first=True)
            np.append(track.title)
            np_requester.append(requeste[0])
            print(f"Attempted to play {track.title}")
            await vc.play(track)
            embed = Embed(title="Now Playing", description=f"{track.title}", color=nextcord.Color.blurple())
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
            Song.update_queue()
            return
    except Exception as e:
        print(e)
        Song.update_queue()
    



        


class Song:
    def __init__(self, url, requester):
        self.url = url
        self.requester = requester


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
    
    def add_song(url, requester):
        self:self
        ctx: Context = self.bot.get_context()
        vc: Player = ctx.voice_client
        song_queue[vc.channel.id] += url
        requeste[vc.channel.id] += requester
        print(song_queue)


        

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(aliases=["j"])
    async def join(self, ctx: commands.Context):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)
        await ctx.author.voice.channel.connect(cls=Player)
    @command(aliases=["l"])
    async def leave(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

    @commands.command(aliases=["p"])
    async def play(self, ctx: commands.Context, *, url):
        resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
        if ctx.author.id in RequesterBlacklist:
            await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect(cls=Player)
        vc: Player=ctx.voice_client
        try:
            if not vc.is_playing():
                Song.add_song(url, f"{ctx.author.name}#{ctx.author.discriminator}")
                await play_next(self,ctx)
                return
            else:
                Song.add_song(url, f"{ctx.author.name}#{ctx.author.discriminator}")
                embed = Embed(description=f"Added {url} to the queue", color=nextcord.Color.green())
                await ctx.send(embed=embed)
                return
        except Exception as e:
            pass
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
        vc: wavelink.Player=ctx.voice_client
        await vc.pause()
        await ctx.send("Music paused")
    
    @commands.command()
    async def resume(self, ctx: commands.Context):
        resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
        if ctx.author.id in RequesterBlacklist:
            await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
        vc: wavelink.Player=ctx.voice_client
        await vc.resume()
        await ctx.send("Music resumed")
    
    @commands.command()
    async def stop(self, ctx: commands.Context):
        vc: wavelink.Player=ctx.voice_client
        resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
        if ctx.author.id in RequesterBlacklist:
            await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
        await vc.stop()
        await ctx.send("Music stopped")

    @commands.command()
    async def skip(self, ctx: commands.Context):
        resp = ["now go reflect on your actions", "you feel like a dumb ass dont you?", "go home"]
        if ctx.author.id in RequesterBlacklist:
            await ctx.send(f"You've been blacklisted from using the music commands. {random.choice(resp)}")
        vc: wavelink.Player=ctx.voice_client
        await vc.stop()
        embed = Embed(description=f"Skipped", color=nextcord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def progress(self, ctx: commands.Context):
        vc: wavelink.Player=ctx.voice_client
        await ctx.send(f"Position: {vc.position} / {vc.track.duration}")
    
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
        vc: wavelink.Player=ctx.voice_client; 
        try: vc.loop ^= True 
        except Exception: setattr(vc, "loop", False); 
        if vc.loop: await ctx.send("Looping enabled"); 
        else: await ctx.send("Looping disabled")
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
    async def shuffle(self, ctx: commands.Context):
        if len(song_queue) == 0:
            await ctx.send("i can't shuffle NOTHING DICHEAD")
            return
        Song.shuffle_queue()
        embed = Embed(description=f"Shuffled the queue", color=nextcord.Color.dark_purple())
        await ctx.send(embed=embed)

    @commands.command()
    async def volume(self, ctx: commands.Context, volume: int):
        vc: wavelink.Player = ctx.voice_client
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        vc.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
    
    @commands.command()
    async def move(self, ctx: commands.Context, pos1, pos2):
        song_queue.insert(int(pos2)-1, song_queue.pop(int(pos1)-1))
        requeste.insert(int(pos2)-1, requeste.pop(int(pos1)-1))
        await ctx.send(f"Moved {pos1} to {pos2}")
    
    @commands.command(name="Now_Playing", aliases=["np"])
    async def now_playing(self, ctx: commands.Context):
        try:
            embed = Embed(title="Now Playing", description=f"{np[0]}", color=nextcord.Color.blurple())
            embed.set_footer(text=f"Requested by {np_requester[0]}")
            await ctx.send(embed=embed)
        except IndexError:
            embed = Embed(title="¯\_(ツ)_/¯", description=f"Nothing is playing", color=nextcord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(aliases=["fp"])
    async def fplay(self, ctx: commands.Context, url):
        track = await wavelink.YouTubeTrack.search(url, return_first=True)
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect(cls=Player)
        vc: wavelink.Player = ctx.voice_client
        await vc.play(track)
        print(url)

    @commands.command()
    async def splay(self, ctx: commands.Context, *, query: str):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect(cls=Player)
        vc: wavelink.Player = ctx.voice_client
        try:
            if not query.startswith("https://open.spotify.com/"):
                song = spot.search(query, limit=1, type="track")["tracks"]["items"][0]["uri"]
                track = await spotify.SpotifyTrack.search(query=song, return_first=True)
                await vc.play(track)
                embed = Embed(title="Now Playing", description=f" {track.author} - {track.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)
            else:
                track = await spotify.SpotifyTrack.search(query=query, return_first=True)
                await vc.play(track)
                embed = Embed(title="Now Playing", description=f"{track.author} - {track.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        print(query)

    @Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(node_connect(self))
    @Cog.listener()
    async def on_wavelink_node_ready(self, node: Node):
        print(f"Node {node.identifier} is ready.")
    @Cog.listener()
    async def on_wavelink_node_connect(self, node: Node):
        print(f"Node {node.identifier} is connected.")
    @Cog.listener()
    async def on_wavelink_track_end(player: Player, reason):
        self: self
        ctx: commands.Context
        if len(song_queue) == 0:
            titles=["That's all folks", "Show's over folks", "fin", "*crickets*", "i got nothing folks"]
            embed = Embed(title=random.choice(titles), description="The queue has finished playing", color=nextcord.Color.red())
        np.pop(0)
        np_requester.pop(0)
        vc: Player = ctx.voice_client
        cs= str(song_queue[vc.channel.id][0])
        if vc.loop:
            vc.play(track)
        try:
            if cs.startswith("https://youtube.com") or cs.startswith("https://youtu.be") or cs.startswith("https://www.youtube.com"):
                song = await wavelink.YouTubeTrack.search(song_queue[0], return_first=True)
                np.append(song.title)
                np_requester.append(requeste[0])
                vc: Player = ctx.voice_client
                print(f"Attempted to play {song.title}")
                print(song)
                await vc.play(song)
                embed = Embed(title="Now Playing", description=f"{song.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Uploader: {song.author} | Requested by {requeste[0]}")
                await ctx.send(embed=embed)
                Song.update_queue()
                return
            if cs.startswith("https://music.youtube.com"):
                song = await wavelink.YouTubeMusicTrack.search(song_queue[0], return_first=True)
                np.append(song.title)
                np_requester.append(requeste[0])
                vc: Player = ctx.voice_client
                print(f"Attempted to play {song.title}")
                print(song)
                await vc.play(song)
                embed = Embed(title="Now Playing", description=f"{song.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Uploader: {song.author} | Requested by {requeste[0]}")
                await ctx.send(embed=embed)
                Song.update_queue()
                return
            if not cs.startswith("https://open.spotify.com/"):
                spot_song=spot.search(cs, limit=1, type="track")["tracks"]["items"][0]["uri"]
                track = await spotify.SpotifyTrack.search(query=spot_song, return_first=True)
                np.append(track.title)
                np_requester.append(requeste[0])
                await vc.play(track)
                embed = Embed(title="Now Playing", description=f"{track.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Requested by {ctx.author}")
                Song.update_queue()
                await ctx.send(embed=embed)
                return
            else:
                vc: Player = ctx.voice_client
                print("Spotify Link Detected")
                track = await spotify.SpotifyTrack.search(query=cs, return_first=True)
                np.append(track.title)
                np_requester.append(requeste[0])
                print(f"Attempted to play {track.title}")
                await vc.play(track)
                embed = Embed(title="Now Playing", description=f"{track.title}", color=nextcord.Color.blurple())
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)
                Song.update_queue()
                return
        except Exception as e:
            print(e)
            Song.update_queue()
            print("Track ended")



    
def setup(bot):
    bot.add_cog(Music(bot))




