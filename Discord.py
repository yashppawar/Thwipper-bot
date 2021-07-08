import discord
from discord.utils import get
from discord.ext import commands, tasks
import os
import sys
import pytz
import json
import random
import asyncio
import calendar
import datetime
import regex
import ffmpeg
import requests
import youtube_dl 
import urllib.request
from googlesearch import search
import mysql.connector as ms

# SETUP
bot = commands.Bot(command_prefix="t!")
intents = discord.Intents().all()
client = discord.Client(intents=intents)
# MEMES
meme_links = []
# MUSIC
queue = []
autoplay = 0
loop = 0
current = {}
FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ydl_op = {'format':'bestaudio/best','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'96',}],}
# FACTS
facts_list = []
# Utility
num_req = 1
# SQL
file = open("../env.txt","r")
txt_from_file = str(file.read())
print(txt_from_file)
start_password = txt_from_file.find("MySQL=") + len("MySQL=")
print(start_password)
end_password = txt_from_file.find('"',start_password + 3) + 1
print(end_password)
mysql_password = str(eval(txt_from_file[start_password:end_password]))
print()
conn = ms.connect(host="localhost", user="root", passwd=mysql_password, database="discord")
cursor = conn.cursor()
# EXTRAS
url_date_time = "https://www.intego.com/mac-security-blog/wp-content/uploads/2020/07/macos-date-time-lead.png"
url_thumbnails = ["https://c4.wallpaperflare.com/wallpaper/42/823/767/spiderman-hd-wallpaper-preview.jpg","https://c4.wallpaperflare.com/wallpaper/517/160/840/spiderman-ps4-spiderman-games-hd-wallpaper-preview.jpg","https://c4.wallpaperflare.com/wallpaper/107/848/913/spiderman-ps4-spiderman-games-hd-wallpaper-preview.jpg","https://wallpapercave.com/wp/AVIUso6.jpg","https://wallpapercave.com/wp/n9L3kJf.jpg","https://images.hdqwalls.com/wallpapers/thumb/spider-man-miles-morales-minimal-art-4k-43.jpg","https://images.hdqwalls.com/wallpapers/thumb/northern-spider-5k-f3.jpg","https://images.hdqwalls.com/wallpapers/thumb/spider-and-deadpool-4k-ys.jpg","https://images.hdqwalls.com/wallpapers/thumb/spiderman-into-the-spider-verse-y7.jpg","https://wallpapercave.com/wp/wp2018132.png","https://wallpapercave.com/wp/wp2018145.jpg","https://wallpapercave.com/wp/wp2018203.jpg","https://images3.alphacoders.com/593/thumbbig-593562.webp","https://images6.alphacoders.com/107/thumbbig-1071152.webp","https://images6.alphacoders.com/107/thumbbig-1070974.webp","https://i.pinimg.com/236x/38/a4/f6/38a4f62d74d7aeb2ae2396c991fcde52.jpg","https://i.pinimg.com/236x/ed/76/cc/ed76cc8bfe41347d979c93e23fbe51a0.jpg","https://i.pinimg.com/236x/91/87/2d/91872d5c92e8339036106bc832656a49.jpg","https://i.pinimg.com/236x/e3/94/05/e39405072916bb996caee3a4045f573a.jpg","https://i.pinimg.com/236x/36/2c/42/362c4298860d79a4b49acd9370cabe04.jpg","https://i.pinimg.com/236x/cf/3c/f4/cf3cf4ef7239868b1abc243168c41647.jpg","https://i.pinimg.com/236x/b1/3e/e7/b13ee7a8a8d72fbe39153569b5618c21.jpg"]
url_author_sql = "https://miro.medium.com/max/361/1*WzqoTtRUpmJR26dzlKdIwg.png"
url_author_music = "https://i.pinimg.com/236x/74/d8/46/74d8469c377334ffd7ae49d54491b477.jpg"
url_author_python = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/1200px-Python.svg.png"

def youtube_download(ctx,url):
    if True:
        with youtube_dl.YoutubeDL(ydl_op) as ydl:
            URL = ydl.extract_info(url, download=False)['formats'][0]['url']
    return URL

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    # FACTS
    global facts_list
    b = requests.get("https://www.thefactsite.com/1000-interesting-facts/").content.decode().replace("<i>","*").replace("</i>","*").replace("&#8220;",'"').replace("&#8221;",'"').replace("&#8217;","'")
    stop = 0
    for i in range(0,117):
        n1 = b.find('<p class="list">',stop) + len('<p class="list">')
        n2 = b.find("</p>",stop)
        stop = n2 + len("</p>")
        output = ""
        if not b[n1:n2]:
            continue
        else:
            output = b[n1:n2]
            facts_list += [output]    
    # MEMES
    global meme_links
    raw = requests.get("https://in.pinterest.com/nevaehgracesmom/superhero-memes/")
    html_content = raw.content.decode()
    stop = 0
    for i in range(0,500):
        a = html_content.find("GrowthUnauthPinImage__Image",stop)
        b = html_content.find('src="',a) + len('src="')
        c = html_content.find('" ',b)
        stop = c
        if i == 0:
            continue
        link = html_content[b:c]
        if link.find("</div>") != -1 or link.find("<html") != -1:
            continue
        meme_links += [link]
    # UPDATION
    @tasks.loop(seconds=5.0)
    async def updation():
        # requests
        global cursor
        # music queue 
        global queue
        global cursor
        operation_queue = "SELECT * FROM music_queue"
        cursor.execute(operation_queue)
        songs = cursor.fetchall()
        for song in songs:
            if song not in queue:
                   queue.append(song)
            else:
                continue
        # sql table 
        global conn
        conn.commit()
    updation.start()

# //////////////////////////////////// SPECIAL ACCESS /////////////////////////////////////////

@bot.command(aliases=["allow","alw"])
async def allow_access(ctx, member:discord.Member):
    global url_author_python
    global cursor
    if ctx.author.id == 622497106657148939:
        cursor.execute("INSERT INTO dev_users(id)values({})".format(str(member.id)))
        embed = discord.Embed(description="{} has been allowed access".format(member), color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="Python Shell", icon_url=url_author_python)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="Access Denied", color=discord.Color.from_rgb(70, 96, 253))


@bot.command(aliases=["restrict","rstr"])
async def remove_access(ctx, member:discord.Member):
    global url_author_python
    global cursor
    if ctx.author.id == 622497106657148939:    
        cursor.execute("DELETE FROM dev_users WHERE id={}".format(member.id))    
        embed = discord.Embed(description="{} is now restricted".format(str(member.display_name)), color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="Python Shell", icon_url=url_author_python)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="Access Denied", color=discord.Color.from_rgb(70, 96, 253))    


@bot.command(aliases=["t"])
async def python_shell(ctx, *, expression):
    global cursor
    global url_author_python
    operation = "SELECT * FROM dev_users"
    cursor.execute(operation)
    dev_ids = cursor.fetchall()
    for dev_id in dev_ids:
        if ctx.author.id == int(dev_id[0]) or ctx.author.id == 622497106657148939:
            try:
                embed_acc = discord.Embed(title=str(expression), description=str(eval(expression)), color=discord.Color.from_rgb(70, 96, 253))
                embed_acc.set_author(name="Python Shell", icon_url=url_author_python)
                await ctx.send(embed=embed_acc)
                break
            except Exception as e:
                embed_err = discord.Embed(title="𝗘𝗥𝗥𝗢𝗥", description=str(e), color=discord.Color.from_rgb(70, 96, 253))
                embed_err.set_author(name="Python Shell", icon_url=url_author_python)
                await ctx.send(embed=embed_err)
                break
    else:
        embed_dc = discord.Embed(title="Access Denied", color=discord.Color.from_rgb(70, 96, 253))
        embed_dc.set_author(name="Python Shell",icon_url=url_author_python)
        await ctx.send(embed=embed_dc)
        

@bot.command()
async def clear(ctx, text, num=10000000000000):
    global cursor
    operation = "SELECT * FROM dev_users"
    cursor.execute(operation)
    devs_id = cursor.fetchall()
    for dev_id in devs_id:
        if str(ctx.author.id) == dev_id or ctx.author.id == 622497106657148939:
            await ctx.channel.purge(limit=1)
            if str(text) == "OK":
                await ctx.channel.purge(limit=num)
                break
            else:
                await ctx.send("Incorrect Password")
                break
        else:
            await ctx.send("Access Denied")
            break


@bot.command(aliases=["exit"])
async def stop_program(ctx):
    if ctx.author.id == 622497106657148939:
        await ctx.send("Bye {}!".format(ctx.author.name))
        exit()
    else:
       await ctx.send("Access Denied")

#///////////////////////////////////// STANDARD //////////////////////////////////////////////

@bot.command(aliases=['hello', 'hi', 'hey', 'hey there', 'salut',"kon'nichiwa","hola","aloha"])
async def greet_bot(ctx):
    greetings = ["Hey {}".format(ctx.author.name), "Hi {}".format(ctx.author.name),"What can I do for you {}?".format(ctx.author.name), "What's up {}?".format(ctx.author.name), "Hello {}".format(ctx.author.name)]
    await ctx.send(random.choice(greetings))


@bot.command(aliases=['h'])
async def embed_help(ctx):
    global url_thumbnails
    embed = discord.Embed(title="🕸𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗠𝗲𝗻𝘂🕸",
                        description="Prefix => `t!`",
                        color=discord.Color.from_rgb(70, 96, 253))
    embed.add_field(name="𝗦𝘁𝗮𝗻𝗱𝗮𝗿𝗱",value="hello to greet bot\nh to get this embed", inline=False)
    embed.add_field(name="𝗨𝘁𝗶𝗹𝗶𝘁𝘆", value="ping to get user latency", inline=False)
    embed.add_field(name="𝗗𝗮𝘁𝗲 & 𝗧𝗶𝗺𝗲", value="dt to get IST date and time\ncal.m <year, month(in number)> to get calendar", inline=False)
    embed.add_field(name="𝗠𝘆𝗦𝗤𝗟", value="; <query> to use SQL Shell", inline=False)
    embed.add_field(name="𝗜𝗻𝘁𝗲𝗿𝗻𝗲𝘁",value="g <topic> to google\nfact to get an interesting fact\nmeme to get superhero memes",inline=False)
    embed.add_field(name="𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹",value="cn to get the bot to join voice channel\ndc to remove bot from voice channel",inline=False)
    embed.add_field(name="𝗣𝗹𝗮𝘆𝗲𝗿",value="p <name> or <index> to play songs\nres to resume a song\npause to pause a song\nst to stop a song", inline=False)
    embed.add_field(name="𝗤𝘂𝗲𝘂𝗲",value="q <name> to add a song to the queue\nv to view the queue\ncq to clear queue", inline=False)
    embed.set_thumbnail(url=random.choice(url_thumbnails))
    embed.set_footer(text="New Features Coming Soon! [🛠]\n1)Autoplay  2)Next  3)Previous  4)Loop Queue  5)Repeat Song  6)Remove")
    await ctx.send(embed=embed)

# //////////////////////////////////// INTERNET //////////////////////////////////////////////

@bot.command(aliases=['g'])
async def browse(ctx, *, thing_to_search):
    results = " "
    for result in search(thing_to_search, tld='com', lang='en', safe='off', num=10, start=0,stop=10, pause=2.0):
        results += result + "\n\n"
    await ctx.send(results)


@bot.command(aliases=["fact"])
async def get_fact(ctx):
    try:
        await ctx.send(embed=discord.Embed(description=random.choice(facts_list), color=discord.Color.from_rgb(70, 96, 253)))
    except TypeError as te:
        await ctx.send(embed=discord.Embed(description=str(te), color=discord.Color.from_rgb(70, 96, 253)))
    

@bot.command(aliases=["meme"])
async def get_meme(ctx):
    await ctx.send(random.choice(meme_links))

#///////////////////////////////////// UTILITY ///////////////////////////////////////////////

@bot.command(aliases=["ping"])
async def get_ping(ctx):
    await ctx.send(embed=discord.Embed(description="𝙇𝙖𝙩𝙚𝙣𝙘𝙮 : {} ms".format(round(bot.latency * 1000)), color=discord.Color.from_rgb(70, 96, 253)))


@bot.command(aliases=["req"])
async def show_req(ctx):
    global cursor
    operation_num_req = "SELECT * FROM requests"
    cursor.execute(operation_num_req)
    req_num = cursor.fetchall()
    await ctx.send(embed=discord.Embed(title="Requests", description=str(req_num).replace("["," ").replace("]"," ").replace(","," ").replace("("," ").replace(")"," ").replace("0"," "), color=discord.Color.from_rgb(70, 96, 253)))

# /////////////////////////////////////// DATE & TIME /////////////////////////////////////////

@bot.command(aliases=["dt"])
async def date_time_ist(ctx):
    tzinfo = pytz.timezone("Asia/Kolkata")
    dateTime = datetime.datetime.now(tz=tzinfo)
    embed = discord.Embed(color=discord.Color.from_rgb(70, 96, 253))
    embed.add_field(name="𝗗𝗮𝘁𝗲", value="%s/%s/%s" % (dateTime.day, dateTime.month, dateTime.year), inline=True)
    embed.add_field(name="𝗧𝗶𝗺𝗲", value="%s:%s:%s" % (dateTime.hour, dateTime.minute, dateTime.second), inline=True)
    await ctx.send(embed=embed)   


@bot.command(aliases=["cal.m"])
async def get_calendar(ctx, year, month):
    global url_date_time
    embed = discord.Embed(title="𝗖𝗮𝗹𝗲𝗻𝗱𝗮𝗿", description="```{}```".format(calendar.month(int(year), int(month))), color=discord.Color.from_rgb(70, 96, 253))
    embed.set_thumbnail(url=url_date_time)
    await ctx.send(embed=embed)

#///////////////////////////////////// STORAGE(SQL SHELL) ////////////////////////////////////

@bot.command(aliases=[";"])
async def sql_shell(ctx, *, expression):
    global cursor
    try:
        output = ""
        cursor.execute(expression)
        for item in cursor.fetchall():
            output += str(item) + "\n"
        conn.commit()
        embed = discord.Embed(title=str(expression), description=str(output), color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="MySQL Shell", icon_url=url_author_sql)   
        await ctx.send(embed=embed)
    except Exception as e:
        embed_err = discord.Embed(title="𝗘𝗥𝗥𝗢𝗥", description=str(e), color=discord.Color.from_rgb(70, 96, 253))
        embed_err.set_author(name="MySQL Shell", icon_url=url_author_sql)   
        await ctx.send(embed=embed_err)

#///////////////////////////////////////// MUSIC /////////////////////////////////////////////

@bot.command(aliases=["cn","connect"])
async def join_vc(ctx):
    try:
        if not ctx.message.author.voice:
            await ctx.send("{}, connect to a voice channel first".format(ctx.author.name))
        else:    
            channel = ctx.message.author.voice.channel
            await channel.connect()
            message = await ctx.send("Connected")
            await asyncio.sleep(2)
            await message.edit(content="Use `t!p <name> or <index>` to play songs") 
    except Exception as e:
        embed_error = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
        embed_error.set_author(name="𝗠𝘂𝘀𝗶𝗰", icon_url=url_author_music)
        await ctx.send(embed=embed_error)


@bot.command(aliases=["dc","disconnect"])
async def leave_vc(ctx):
    voice_client = ctx.message.guild.voice_client
    channel = ctx.message.author.voice.channel
    try:
        if voice_client.is_connected():
            await voice_client.disconnect()
            message = await ctx.send("Disconnected")
            await asyncio.sleep(2)
            await message.edit(content="See ya later!")
    except:        
        embed = discord.Embed(description="Not in a voice channel to disconnect from [❌]", color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="𝗠𝘂𝘀𝗶𝗰", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["queue","q"])
async def queue_song(ctx, *, name):
    global cursor
    name = name.replace(" ", "+")
    htm = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + name) # the 11 lettered string which is like an ID for videos is stored inside the variable video
    video = regex.findall(r"watch\?v=(\S{11})", htm.read().decode())
    url = "https://www.youtube.com/watch?v=" + video[0] # we got the html code of the full search page
    htm_code = str(urllib.request.urlopen(url).read().decode()) # htm_code contains the entire HTML code of the web page where we see the video
    starting = htm_code.find("<title>") + len("<title>") # now we use .find method to find the title of the vid which is in between <title></title> tags
    ending = htm_code.find("</title>")        
    name_of_the_song = htm_code[starting:ending].replace("&#39;","'").replace("&amp;","&") # here we replace uncessary things like tags because we only want the title
    cursor.execute("INSERT INTO music_queue(song_name, song_url)VALUES('{first}','{last}')".format(first=name_of_the_song, last=url))
    embed = discord.Embed(description="{} [✅]".format(name_of_the_song).replace(" - YouTube", " "), color=discord.Color.from_rgb(70, 96, 253))
    embed.set_author(name="Song added", icon_url=url_author_music)
    await ctx.send(embed=embed)


@bot.command(aliases=["play","p"])
async def play_music(ctx, *, char):
    global ydl_op
    global queue
    global cursor
    global FFMPEG_OPTS
    char = char.replace(" ","+")
    htm = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + char)
    video = regex.findall(r"watch\?v=(\S{11})",htm.read().decode())
    url = "https://www.youtube.com/watch?v=" + video[0]
    URL = youtube_download(ctx,url)
    htm_code = str(urllib.request.urlopen(url).read().decode())
    starting = htm_code.find("<title>") + len("<title>")
    ending = htm_code.find("</title>")
    name_of_the_song = htm_code[starting:ending].replace("&#39;","'").replace("&amp;","&")
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice_client = ctx.message.guild.voice_client
    playing = ctx.voice_client.is_playing()
    if char.isnumeric() == False:
        try:
            if playing != True:
                embed = discord.Embed(description="{}".format(name_of_the_song).replace(" - YouTube", " "), color=discord.Color.from_rgb(70, 96, 253))
                embed.set_author(name="Now playing [🎸]", icon_url=url_author_music)
                await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTS))
            else:
                embed = discord.Embed(description="{}".format(name_of_the_song).replace(" - YouTube", " "), color=discord.Color.from_rgb(70, 96, 253))
                embed.set_author(name="Now playing [🎸]", icon_url=url_author_music)
                voice.stop()
                await ctx.send(embed=embed)
                voice.play(discord.FFmpegOpusAudio(URL, bitrate=96, codec=None, executable=FFMPEG_OPTS))
        except Exception as e:
            embed = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
            embed.set_author(name="𝗘𝗥𝗥𝗢𝗥", icon_url=url_author_music)
            await ctx.send(embed=embed)
    else:
        URL = youtube_download(ctx, queue[int(char)][1])
        try: 
            if not ctx.guild.id in list(current.keys()) and int(char) < len(queue):
                current[ctx.guild.id] = int(char)
            if playing != True:
                embed = discord.Embed(description="{}".format(queue[int(char)][0]).replace(" - YouTube", " "), color=discord.Color.from_rgb(70, 96, 253))
                embed.set_author(name="Now playing [🎸]", icon_url=url_author_music)
                await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTS))
            else:
                embed = discord.Embed(description="{}".format(queue[int(char)][0]).replace(" - YouTube", " "), color=discord.Color.from_rgb(70, 96, 253))
                embed.set_author(name="Now playing [🎸]", icon_url=url_author_music)
                voice.stop()
                await ctx.send(embed=embed)
                voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTS))
        except Exception as e:
            embed = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
            embed.set_author(name="𝗘𝗥𝗥𝗢𝗥", icon_url=url_author_music)
            await ctx.send(embed=embed)    


@bot.command(aliases=["view","v"])
async def view_queue(ctx):
    global queue
    global current
    string = ""
    song_index = 0
    toggle = 0
    if len(queue) > 0:
        for song in queue:
            string += str(song_index) + ". " + str(queue[song_index][0]) + "\n"
            song_index += 1
        embed = discord.Embed(description=string.replace(" - YouTube"," "), color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="𝗤𝘂𝗲𝘂𝗲", icon_url=url_author_music)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="No songs in queue [⭕]", color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="𝗤𝘂𝗲𝘂𝗲", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["pause"])
async def pause_song(ctx):
    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()
    try:
        if playing == True:    
            voice_client.pause()
            message = await ctx.send("Song paused")
            await message.add_reaction("⏸")
        else:
            if pause == True:
                await ctx.send(embed=discord.Embed(description="Song is already paused [❗]", color=discord.Color.from_rgb(70, 96, 253)))
            else:
                embed = discord.Embed(description="No song playing currently [❗]", color=discord.Color.from_rgb(70, 96, 253))
                await ctx.send(embed=embed)
    except Exception as e: 
        embed = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="𝗘𝗥𝗥𝗢𝗥", icon_url=url_author_music)
        await ctx.send(embed=embed)


@bot.command(aliases=["resume","res"])
async def resume_song(ctx):
    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()
    try:
        if pause == True:
            voice_client.resume()
            message = await ctx.send("Song resumed")
            await message.add_reaction("▶")
        else:
            if playing == True:
                embed = discord.Embed(description="Song isn't paused [❓]\nUse _pause to pause the song.", color=discord.Color.from_rgb(70, 96, 253))
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(description="No song playing currently [❗]\nUse _p <name>  or <index> to play a song.", color=discord.Color.from_rgb(70, 96, 253)))
    except Exception as e:
            embed = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
            embed.set_author(name="𝗘𝗥𝗥𝗢𝗥", icon_url=url_author_music)
            await ctx.send(embed=embed)


@bot.command(aliases=["stop","st"])
async def stop_song(ctx):
    voice_client = ctx.message.guild.voice_client
    pause = ctx.voice_client.is_paused()
    playing = ctx.voice_client.is_playing()
    try:
        if playing == True or pause == True:    
            voice_client.stop()
            message = await ctx.send("Song stopped")
            await message.add_reaction("⏹")
        else:
            await ctx.send(embed=discord.Embed(description="Nothing is playing right now [❗]", color=discord.Color.from_rgb(70, 96, 253))
            )
    except Exception as e:
            embed = discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253))
            embed.set_author(name="𝗘𝗥𝗥𝗢𝗥", icon_url=url_author_music)
            await ctx.send(embed=embed)


@bot.command(aliases=["rem","remove"])
async def remove_song(ctx, index):
    global queue
    global cursor
    try:
        operation_remove = "DELETE FROM music_queue WHERE song_name={first} AND song_url={last}".format(first=queue[index][0], last=queue[index][1])
        await ctx.send(embed=discord.Embed(title="Song removed", description="`{}` [✅]".format(queue[index][0]), color=discord.Color.from_rgb(70, 96, 253)))
        cursor.execute(operation_remove)
    except Exception as e:
        await ctx.send(embed=discord.Embed(description=str(e), color=discord.Color.from_rgb(70, 96, 253)))


@bot.command(aliases=["clear_queue","cq"])
async def clear_song_queue(ctx):
    global queue
    global cursor
    if len(queue) > 0:
        operation_clear_song = "DELETE FROM music_queue"
        cursor.execute(operation_clear_song)
        queue.clear()
        message = await ctx.send("Queue Cleared")
        await message.add_reaction("✅")
    else:
        embed = discord.Embed(description="Queue is already empty [⭕]", color=discord.Color.from_rgb(70, 96, 253))
        embed.set_author(name="𝗛𝗺𝗺...", icon_url=url_author_music)
        await ctx.send(embed=embed)


start_token = txt_from_file.find("token=") + len("token=")
end_token = txt_from_file.find('"',start_token + 3) + 1
bot.run(eval(txt_from_file[start_token:end_token]))