import discord
from discord import File, Streaming, Game, Activity, ActivityType, Status
from discord.ext import commands
import io, aiohttp, asyncio, json, random, logging, requests


foxmsgs = [
        'floofy fox',
        'here fops',
        'owo',
        'uwu',
        'heres ur fox',
        ]

async def is_ginlang(ctx):
    """
    are you ginlang or the other dude?
    """
    if ctx.author.id in [287885666941927424, 894034804503351366]:
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
            await ctx.send(random.choice(foxmsgs),file=file)

@bot.command(brief="cattttttttt")
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/cat') as resp:
            json = await resp.json()
            await ctx.send(json["fact"])
            await ctx.send(json["image"])

@bot.command(brief="gives you a fluffy panda")
async def panda(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/panda') as resp:
            json = await resp.json()
            await ctx.send(json["fact"])
            await ctx.send(json["image"])


@bot.command(brief="omg koala")
async def koala(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/koala') as resp:
            json = await resp.json()
            await ctx.send(json["fact"])
            await ctx.send(json["image"])


@bot.command(brief="bin eaters")
async def raccoon(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://some-random-api.ml/animal/raccoon') as resp:
            json = await resp.json()
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
    await bot.change_presence(activity=Activity(name=aname, type=atypes[atype], url="https://twitch.tv/xginlang"))
    await ctx.send('Success!')


@bot.command(brief="gives bot invite link")
async def invite(ctx):
    await ctx.send("Add this bot to your server: https://discord.com/oauth2/authorize?client_id=909103805264724038&permissions=274878203904&scope=bot")

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

@bot.command(brief="gives credits")
async def credits(ctx):
    await ctx.send("""Images used in this bot are taken from:
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
Foxtrot is open source! Find the code at <https://code.cat.casa/Helixu/Foxtrot>
""")
@bot.command(brief="random meme")
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://shitfest.net/api/random.php') as resp:
            json = await resp.json()
            await ctx.send(json["url"])

#@bot.command()
#async def help(ctx):
#    await ctx.send("""The current list of commands are:
#fox (Gets an image of a fox)
#activity (Sets bot activity, only works if you are a developer)
#invite (Gives bot invite link)
#help (this)
#""")


@bot.event
async def on_ready():
    await asyncio.sleep(1) # someone on stackoverflow said discord does not like if you are speedy
    await bot.change_presence(activity=Streaming(name="Testing - bot may go offline at any point", url="https://twitch.tv/xginlang"))

with open('token.json', 'r') as file:
    token = ''.join([line[:-1] for line in file.readlines()])
    bot.run(token)

