#!/usr/bin/env python

import json
from random import randint

import aiohttp
import asyncio
import async_timeout

import discord
from discord.ext.commands import Bot


print('running...')
my_bot = Bot(command_prefix = '!!')

with open('config.json') as configFile: # import config
    config = json.load(configFile)



@my_bot.command(pass_context=True)
async def hello(ctx):
    """say hi!"""
    print('hello')
    await my_bot.say(ctx.message.author.mention + ' Hello, world!')
    await my_bot.delete_message(ctx.message)


async def fetch(session, url): # gets a url to text asynchronously
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

class Comic: # for xkcd command
    totalComics = 0

    async def getImgUrl(self, num):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://xkcd.com/' + str(num) + '/info.0.json')
            d = json.loads(html)
            return d['img']

    def randomComicNum(self):
        return randint(1, self.totalComics)

    async def setCount(self):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://xkcd.com/info.0.json')
            d = json.loads(html)
            self.totalComics = d['num']

    def getRandomComic(self):
        return self.getImgUrl(self.randomComicNum())

c = Comic()
my_bot.loop.run_until_complete(c.setCount())
@my_bot.command(pass_context=True, aliases=['x'])
async def xkcd(ctx, *args):
    """(x) gets an xkcd comic. optional number following the command"""
    if args:
        try:
            n = int(args[0])
        except Exception as e:
            return await my_bot.say(ctx.message.author.mention + ' `Error: args must be a number`')
    else:
        n = c.randomComicNum()
    url = await c.getImgUrl(n)
    # await my_bot.say('`XKCD comic #' + str(n) + ':`')
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content=ctx.message.author.mention + ' `XKCD comic #' + str(n) + ':`', embed=em.set_image(url=url))
    await my_bot.delete_message(ctx.message)
    print('xkcd #' + str(n))


@my_bot.command(pass_context=True, aliases=['i'])
async def iconify(ctx, *args):
    """(i) turns text into emoji. must have a string following the command"""
    def toNum(x):
        return {0:'zero',1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine'}[x]

    def toIconCode(x):
        try: return ':' + toNum(int(x)) + ':'
        except Exception as e:
            if x == ' ': return '  '
            if x == '?': return ':question:'
            if x == '!': return ':exclamation:'
            else: return ':regional_indicator_' + x + ':'

    def make(s):
        icontext = ''
        for char in s:
            icontext += toIconCode(char)
            icontext += ' '
        return icontext
    iconstring = ''
    if args:
        args = ' '.join(args) # collapse ares to a string
        iconstring = args.lower()
        await my_bot.say(ctx.message.author.mention + ' ' + make(iconstring))
    else:
        await my_bot.say(ctx.message.author.mention + ' `Error: must specify a string`')
    await my_bot.delete_message(ctx.message)
    print('iconify: ' + iconstring)

@my_bot.command(pass_context=True, aliases=['c'])
async def cat(ctx):
    """(c) random cat picture"""
    print('cat')
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://random.cat/meow') as r:
            res = await r.json()
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=res['file']))
    await my_bot.delete_message(ctx.message)

@my_bot.command(pass_context=True, aliases=['d'])
async def dog(ctx):
    """(d) random dog picture"""
    print('dog')
    isVideo = True
    while isVideo:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                res = await r.json()
                res = res['url']
        if res.endswith('.mp4'):
            pass
        else:
            isVideo = False
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=res))
    await my_bot.delete_message(ctx.message)


class Shibs():
    data = None
    size = None
    async def start(self):
        async with aiohttp.ClientSession() as session:
            url = 'https://api.github.com/repos/RobIsAnxious/shibesbot-db/contents/pictures'
            with async_timeout.timeout(10):
                auth = aiohttp.BasicAuth(config['github']['username'], password=config['github']['pass'])
                async with session.get(url, auth=auth) as response:
                    html = await response.text()
            self.data = json.loads(html)
            self.size = len(self.data)

    def getAttr(self, num, attr):
        return self.data[num][attr]

    def getRand(self):
        return randint(1, self.size)

    def getImgUrl(self, num):
        return self.data[num]['download_url']


s = Shibs()
my_bot.loop.run_until_complete(s.start())

@my_bot.command(pass_context=True, aliases=['s'])
async def shib(ctx):
    """(s) basically hijacks the shibs database to provide shibs"""
    n = s.getRand()
    print('shib')
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=s.getImgUrl(n)))
    await my_bot.delete_message(ctx.message)



my_bot.run(config['botkey']) # Shibbot's Cousin (debate)
