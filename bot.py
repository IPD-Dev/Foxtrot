 

import discord
from discord import File, Streaming, Game, Activity, ActivityType, Status
from discord.ext import commands, tasks
import io, aiohttp, asyncio, json, random, logging, requests


foxmsgs = [
        'floofy fox',
        'here fops',
        'owo',
        'uwu',
        'fox hugz u',
        'fox fox fox',
        'heres ur fox',
        ]

def getAllUsers():
    membercount = 0
    for guild in bot.guilds:
        membercount += guild.member_count
    return membercount

async def is_ginlang(ctx):
    """
    are you ginlang or the other dudes?
    """
    if ctx.author.id in [287885666941927424, 160091312081731584, 894034804503351366, 296736767158255616, 831598877320413244]:
        return True
    else:
        logchannel = await bot.fetch_channel(910622485916037150)
        await logchannel.send('User '+ctx.author.name+'#'+ctx.author.discriminator+' ('+str(ctx.author.id)+') has attempted to use a whitelist only command.')
        return False

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='gib ')

@bot.command(brief="gives you a fluffy fox")
async def fox(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://foxrudor.de/') as resp:
            file = File(io.BytesIO(await resp.read()),filename='fox.jpg')
            try:
                await ctx.send(random.choice(foxmsgs),file=file)
            except:
                     embed = discord.Embed(
                         title = "Command 'fox' failed",
                         description = "Received unexpected error, foxes occupied by ginlang, who is currently hugging them! 413 Payload too Large"
                     )
                     return await ctx.send(embed = embed)

@bot.command(brief="give someone a cuddle")
async def hug(ctx, *, name=None):
	if not name:
		return await ctx.send("Foxtrot hugs "+ctx.author.name+"! :3")
	await ctx.send(ctx.author.name+f" hugs {name}! :3")

@bot.command(brief="gives the top.gg vote link")
async def vote(ctx):
    await ctx.send("Vote for Foxtrot on top.gg! <https://top.gg/bot/909103805264724038/vote>")
 
@bot.command(brief="cattttttttt")
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/cat') as resp:
            json = await resp.json()
            error = json.get('error')
            if error:
                return await ctx.send(f'Received unexpected error, unclear instructions, got stuck in toaster! ({error})')
            await ctx.send(json["fact"])
            await ctx.send(json["image"])

@bot.command(brief="gives you a fluffy panda")
async def panda(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/panda') as resp:
            json = await resp.json()
            error = json.get('error')
            if error:
                return await ctx.send(f'Received unexpected error, thats not good! ({error})')
            await ctx.send(json["fact"])
            await ctx.send(json["image"])


@bot.command(brief="omg koala")
async def koala(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/koala') as resp:
            json = await resp.json()
            error = json.get('error')
            if error:
                return await ctx.send(f'Received unexpected error, try our sister game, Minceraft! ({error})')
            await ctx.send(json["fact"])
            await ctx.send(json["image"])

@bot.command(hidden=True)
@commands.check(is_ginlang)
async def restart(ctx):
	await ctx.send("shutting down. beep boop.")
	await exit()

@bot.command(brief="bin eaters")
async def raccoon(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/raccoon') as resp:
            json = await resp.json()
            error = json.get('error')
            if error:
                return await ctx.send(f'Received unexpected error, blame ginlang! ({error})')
            await ctx.send(json["fact"])
            await ctx.send(json["image"])



@bot.command(hidden=True)
@commands.check(is_ginlang)
async def activity(ctx, atype, *, aname):
    atypes = {'streaming': ActivityType.streaming, 'playing': ActivityType.playing, 'listening': ActivityType.listening, 'watching': ActivityType.watching, 'competing': ActivityType.competing}
    atype = atype.lower()
    if atype not in atypes:
        await ctx.send("invalid activity type. the valid types are "+' '.join(atypes.keys()))
        return
    await bot.change_presence(activity=Activity(name=(aname + f" ¦ {str(getAllUsers())} users"), type=atypes[atype], url="https://www.youtube.com/watch?v=1xBO4pUAs4M"))
    await ctx.send('Success!')


@bot.command(brief="gives bot invite link")
async def invite(ctx):
    await ctx.send("""Add this bot to your server: https://discord.com/oauth2/authorize?client_id=909103805264724038&permissions=274878203904&scope=bot
You can also join our official Discord server at https://discord.gg/NAdRyjykv8!""")

@bot.command(brief="gives information about a minecraft user")
async def mc(ctx, *, name = None):
    if not name:
        embed = discord.Embed(
            title = "No Minecraft user given!",
            description = "You have not given a minecraft username, therefore I cannot find anything for you! usage: gib mc (name)"
        )
        return await ctx.send(embed = embed)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/mc?username={name}') as resp:
            json = await resp.json()
            error = json.get('error')
            if error:
                return await ctx.send(f'Received unexpected error, blame Mojang! ({error})')
            username = json["username"]
            uuid = json["uuid"]
            #namehistory = ', '.join([f"Name: {i['name']} Changed at: {i['changedToAt']}" for i in json["name_history"]])
            embed = discord.Embed(title='Minecraft User Information')
            embed.set_author(name=f'User {username}')
            embed.add_field(name='UUID', value=f'{uuid}', inline=False)
            embed.add_field(name='Name History', value=f"Name changes: {len(json['name_history'])}", inline=False)
            for i in json["name_history"]:
                embed.add_field(name=i['name'], value=f"Changed on: {i['changedToAt']}")
            await ctx.send(embed = embed)
            await ctx.send(f'To view names that did not show up here, go to <https://namemc.com/{username}>')

@bot.command(brief="gives credits")
async def credits(ctx):
    await ctx.send("""API endpoints used in this bot are taken from:
https://foxrudor.de/
https://some-random-api.ml
https://shitfest.net
""")

@bot.command(brief="shows contributors to Foxtrot")
async def contributors(ctx):
    await ctx.send("""Contributors to the Foxtrot bot are:
Helixu#1111
xfnw#1113 
<https://cat.casa/~julia/> (shitfest memes API)
TFTWPhoenix#9240 (I dont know, hes cool I guess.)
remi#9948 (also pretty cool ig)
Ecolipsy#0001
Foxtrot is open source! Find the code at <https://code.cat.casa/IPD/Foxtrot>
""")
@bot.command(brief="random meme")
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.shitfest.net/v2/random.php') as resp:
            json = await resp.json()
            try:
                await ctx.send("https://shitfest.net/"+json["name"])
            except:
                     embed = discord.Embed(
                          title = "Command 'meme' failed",
                          description = "An error has occured with this command. cat.casa could possibly be offline or limited."
                     )
                     return await ctx.send(embed = embed)
 

@bot.command(brief='IPD Discord server invite', aliases=["support"])
async def server(ctx):
	await ctx.send("""The official discord server for Foxtrot is discord.gg/mDBfnysAqd
Our server contains everything we do and work on.""")
 
@bot.command(brief='makes things gay')
async def gay(ctx, url = None):
    await ctx.trigger_typing()
    async with aiohttp.ClientSession() as session:
        async with session.get(
        f'https://some-random-api.ml/canvas/gay?avatar={url}'
        ) as af:
            if 300 > af.status >= 200 :
                fp = io.BytesIO(await af.read())
                file = discord.File(fp, "gay.png")
                embed = discord.Embed(
                    title="gaaaaaay",
                    color=0xf1f1f1,
                    )
                embed.set_image(url="attachment://gay.png")
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send("""An unexpected error happened, Steve.. I told you this already!
Are you sure that the image URL you sent is correct? Image attachments currently do not work!""")

    

@bot.event
async def on_ready():
    await asyncio.sleep(1) # someone on stackoverflow said discord does not like if you are speedy
    await bot.change_presence(activity=Streaming(name=f"Dev Mode ¦ {str(getAllUsers())} users", url="https://www.youtube.com/watch?v=1xBO4pUAs4M"))

with open('token.json', 'r') as file:
    # this breaks if you are on windows
    token = ''.join([line[:-1] for line in file.readlines()])
    bot.run(token)

