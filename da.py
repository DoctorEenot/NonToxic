import os
import random
import discord
from discord.ext import commands,tasks
import random
from discord import File
import ScrolllerApi
from ScrolllerApi import get_random_photo
import LessRelevant
import _4it
import Timer
import time
import threading
import asyncio
import Pornhub
import traceback
import donjon
import Rule34
import gelbooru as gelb
import Porfirevich
import hashlib
import aiohttp
import aiofiles
import siaskynet as skynet
import Prekol


it4_api = _4it.api()

description = '''Roses are red\nViolets are blue\nYou are fucking retard\nI fucking hate you'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

 
timers = []

PH = Pornhub.API()


@bot.event
async def on_ready():
    #asyncio.create_task(timers_watcher)
    timers_watcher.start()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    

@bot.command()
async def fap(ctx, *argv):
    '''Gives you erotic photo with given tag'''
    #tag = ctx.message.content[5:]
    tag = ''
    for arg in argv:
        tag +=arg
    #tag = tag.replace(' ','')
    channel_sended = str(ctx.message.channel.id)
    try:
        image = get_random_photo(tag)
        await ctx.reply(image)
    except Exception as e:
        await ctx.reply('Чё ты ищешь?')

    
@bot.command()
async def stuff(ctx,*argv):
    '''Random video !stuff some text to search -r view_rate(int)'''
    query = ''
    is_r = False
    rate = 100
    for arg in argv:
        if arg == '-r':
            is_r = True
            continue
        if is_r:
            rate = int(arg)
            break
        else:
            query +=arg+' ' 
    for i in range(4):
        try:
            videos = LessRelevant.good_stuff(rate,query)
            break
        except:
            pass
    if videos == []:
        await ctx.reply('Nothing found!')
        return None
    video = 'https://www.youtube.com/watch?v='+random.choice(videos)
    await ctx.reply(video)
   
@bot.command()
async def whois(ctx,q:str):
    '''whois pass ip/host'''
    
    res = it4_api.get_whois(q)['clearResponse']
    await ctx.reply(res)

@bot.command()
async def ports(ctx,q:str,ports_raw=''):
    if ports_raw == '':
        return
    #splitted = q.split(' ')
    ports = []
    list_string = ports_raw.replace('[','')
    list_string = list_string.replace(']','')
    for part in list_string.split(','):
        try:
            ports.append(int(part))
        except:
            await ctx.reply('Something wrong with ports format')
            return 
    res = it4_api.port_scan(q,ports)
    to_return = ''
    for key,item in res.items():
        to_return += f'{key} : {item}\n'
    await ctx.reply(to_return)


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.reply('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.reply(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

async def upload_to_skynet(filename) -> str:
    loop = asyncio.get_event_loop()
    client = skynet.SkynetClient()
    link = await loop.run_in_executor(None,
                                       client.upload_file,
                                       filename,{"api_key":''})
    #link = await link_future
    link = link.replace('sia://','https://siasky.net/')
    return link

async def download_by_url(url:str) -> str:
    filename = hashlib.sha1(url.encode('utf-8')).hexdigest() + '.mp4'
    async with aiohttp.ClientSession() as session:
        f = await aiofiles.open(filename,mode='wb')
        async with session.get(url, timeout=None) as resp:
            if resp.status == 200:
                while True:
                    data = await resp.content.read(1048576)
                    if not data:
                        break
                    await f.write(data)
            await f.close()

    skynet_link = await upload_to_skynet(filename)
    os.remove(filename)
    return skynet_link



@bot.command()
async def phub(ctx,key:str,*argv):
    '''
    Function for working with PornHub
    !phub -s query - get random video
    !phub -d link_to_video - get link to download video
    !phub -t link_to_video - get thumbnails
    '''
    query = ''
    for arg in argv[:-1]:
        query += arg+' '
    query += argv[-1]
    if key == '-s':
        try:
            video = PH.get_random_video(query)
            
        except:
            tr = traceback.format_exc()
            await ctx.send('Pornhub killed SEX!')
            print(tr)
            return
        try:
            video.get_file_urls()
        except:
            pass
        await ctx.reply(f'{video.thumb}\n\n{video.title}\nhttps://www.pornhub.com'+video.url+f'')
    elif key == '-d':
        try:
            video = Pornhub.Video(query,'none')
            source = video.get_best_quality()
            source = await download_by_url(source)
        except:
            tr = traceback.format_exc()
            await ctx.reply('Pornhub killed SEX!')
            print(tr)
            #await ctx.send(str(tr))
            return
        await ctx.send(source)
    elif key == '-t':
        try:
            video = Pornhub.Video(query,'none')
            video.get_file_urls()
            nb = random.randint(0,video.thumbnails.max_thumbnails)           
        except:
            tr = traceback.format_exc()
            await ctx.reply('Pornhub killed SEX!')
            print(tr)
            return
        await ctx.reply(video.thumbnails.get_thumbnail(nb))


@bot.command()
async def timer(ctx,*argv):
    '''sets timer hours:minutes:seconds @user1 @user2...'''
    mentions = argv[1:]
    
    for tm in timers:
        found_all = True
        for mention in mentions:
            if mention not in tm.mentions:
                found_all = False
                break
        if found_all:
            await ctx.send('No no no, I will not set that')
            return

    delta = 0
    time_splitted = argv[0].split(':')
    delta = int(time_splitted[0])*3600 + int(time_splitted[1])*60 + int(time_splitted[0])
    tm = Timer.Timer(delta,ctx.message.channel.id,mentions)
    timers.append(tm)
    message = 'Таймер поставлен '
    if len(mentions) == 1:
        for mention in mentions:
            message += mention
        message += ' , лучше бы тебе поторопиться'
    else:
        for mention in mentions:
            message += mention
        message += ' , советую вам не опаздывать'
    await ctx.send(message)

@bot.command()
async def rule(ctx,*argv):
    '''
    Yep, it does what it says,
    searches your sick fantasies
    '''
    query = argv[0]
    for arg in argv[1:]:
        query += '+'+arg
    
    data = Rule34.search(query)
    if len(data[0]) == 0:
        await ctx.reply("Well, you'l have to imagine that")
        return
    next_search = random.randint(0,1)
    while next_search == 1 and data[1] != None:
        query = data[1]
        data = Rule34.search(query,True)
        next_search = random.randint(0,1)
    
    page_url = random.choice(data[0])
    source_url = Rule34.get_content_url(page_url,data[2])
    await ctx.reply(source_url)

@bot.command()
async def gelbooru(ctx,*argv):
    '''
    rule 34 but for https://gelbooru.com
    '''
    query = argv[0]
    for arg in argv[1:]:
        query += ' '+arg
    
    data = gelb.search(query)
    if len(data[0]) == 0:
        await ctx.reply("Well, you'l have to imagine that")
        return
    next_search = random.randint(0,1)
    while next_search == 1 and data[1] != None:
        query = data[1]
        data = gelb.search(query,True)
        next_search = random.randint(0,1)
    
    page_url = random.choice(data[0])
    source_url = gelb.get_content_url(page_url,data[2])
    await ctx.reply(source_url)

def dungeon_help(argument_name:str):
    text = f'```\n{argument_name}\nsub parameters:\n'
    for param in donjon.HELP_TYPES[argument_name[1:]]:
        text += param+'\n'
    text += '```'
    return text


@bot.command()
async def dungeon(ctx,name:str,*argv):
    '''
    Create random dungeon
    !dungeon name another_arguments
    !dungeon -help -argument_name
    name - name of the dungeon
    -motif - string
    -seed - int
    -map_style - string
    -grid - string
    -dungeon_layout - string
    -dungeon_size - string
    -colsxrows - intxint
    -peripheral_egress - string
    -add_stairs - string
    -room_layout - string
    -room_size - string
    -door_set - string
    -corridor_layout - string
    -remove_deadends - string
    '''
    if name == '-help':
        await ctx.send(dungeon_help(argv[0]))
        return
    dng = donjon.Dungeon(name)
    for arg_pos in range(0,len(argv),2):
        arg = argv[arg_pos]
        res = donjon.HELP_TYPES.get(arg[1:],False)
        if res == False:
            await ctx.send(f'Undefined parameter {arg}!')
            return None
        try:
            sub_arg = argv[arg_pos+1]
        except Exception as e:
            await ctx.send(f'Bloody hell, pigger, !dungeon {arg} subargument')
            return None
        #if sub_arg not in res:
        #    await ctx.send(dungeon_help(argv[0]))
        #    return
        if arg == '-level':
            dng.level = sub_arg
        elif arg == '-motif':
            dng.motif = sub_arg
        elif arg == '-seed':
            dng.seed = sub_arg
        elif arg == '-map_style':
            dng.map_style = sub_arg
        elif arg == '-grid':
            dng.grid = sub_arg
        elif arg == '-dungeon_layout':
            dng.dungeon_layout = sub_arg
        elif arg == '-dungeon_size':
            dng.dungeon_size = sub_arg
        elif arg == '-colsxrows':
            colsrows = sub_arg.lower().split('x')
            dng.cols = int(colsrows[0])
            dng.rows = int(colsrows[1])
        elif arg == '-peripheral_egress':
            dng.peripheral_egress = sub_arg
        elif arg == '-add_stairs':
            dng.add_stairs = sub_arg
        elif arg == '-room_layout':
            dng.room_layout = sub_arg
        elif arg == '-room_size':
            dng.room_size = sub_arg
        elif arg == '-door_set':
            dng.door_set = sub_arg
        elif arg == '-corridor_layout':
            dng.corridor_layout = sub_arg
        elif arg == '-remove_deadends':
            dng.remove_deadends = sub_arg
    full_map_img = dng.generate()
    
    full_map_html = dng.get_html()
    await ctx.send(f'For DM only!:\n{full_map_html}\n\n{full_map_img}')
    
    
@bot.command()
async def porf(ctx,*argv):
    '''
    !porf text/nothing
    '''
    prompt = None
    if len(argv) != 0:
        prompt = ''
        for arg in argv:
            prompt += arg + ' '
    await ctx.send(await Porfirevich.get_reply(prompt))
    


def append_mentions(mentions, insult):
    to_return = ''
    for mention in mentions:
        to_return += mention
    to_return += ' '+insult
    return to_return

@tasks.loop(seconds=1)
async def timers_watcher():
    for number,timer in enumerate(timers):
        res = timer.check()
        if res[0]:
            channel = bot.get_channel(timer.channel)
            await channel.send(append_mentions(timer.mentions,res[1]))
            del timers[number]
            break
        else:
            if res[1] != False:
                channel = bot.get_channel(timer.channel)
                await channel.send(append_mentions(timer.mentions,res[1]))
   
CHANNELS_TO_SEND_PREKOL = {763817309159686205:True,
                           757687979908268172:True}

image_filenames = ('.png','.jpg','.jpeg')
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    is_image = False
    if len(message.attachments) > 0:
        for filename in image_filenames:
            if filename in message.attachments[0].filename.lower():
                is_image = True
                break

    if not is_image:
        await bot.process_commands(message)
        return

    if message.channel.id not in CHANNELS_TO_SEND_PREKOL:
        return

    downloaded_data = b''
    async with aiohttp.ClientSession() as session:
        async with session.get(message.attachments[0].url, timeout=None) as resp:
            if resp.status == 200:
                while True:
                    data = await resp.content.read(1048576)
                    if not data:
                        break
                    downloaded_data += data

    image = Prekol.generate_prikol(downloaded_data)
    await message.channel.send(file=image)


    


#asyncio.create_task(timers_watcher)

bot.run('TOKEN')
