#!/usr/bin/env python

import json
from random import randint

import io
import aiohttp
import asyncio
import async_timeout

import discord
from discord.ext.commands import Bot
import aiohttp


print('running...')
my_bot = Bot(command_prefix = '!!')

@my_bot.command(pass_context=True)
async def hello(ctx):
    """say hi!"""
    print('hello')
    await my_bot.delete_message(ctx.message)
    return await my_bot.say('Hello, world!')


async def fetch(session, url): # gets a url to text asynchronously
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

class Comic: # for xkcd command
    totalComics = 0
    loop = None

    async def getImgUrl(self, num):
        async with aiohttp.ClientSession(loop = self.loop) as session:
            html = await fetch(session, 'https://xkcd.com/' + str(num) + '/info.0.json')
            d = json.loads(html)
            return d['img']

    async def saveImg(self, url):
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                test = await resp.read()
                with open("file/xkcd.png", "wb") as f:
                    f.write(test)
                    return f

    def randomComicNum(self):
        return randint(1, self.totalComics)

    async def setCount(self):
        async with aiohttp.ClientSession(loop = self.loop) as session:
            html = await fetch(session, 'https://xkcd.com/info.0.json')
            d = json.loads(html)
            self.totalComics = d['num']

    def getRandomComic(self):
        return self.getImgUrl(self.randomComicNum())

@my_bot.command(pass_context=True)
async def xkcd(ctx, *args):
    """gets an xkcd comic. optional number following the command"""
    print('xkcd')
    c = Comic()
    c.loop = asyncio.get_event_loop()
    await c.setCount()
    if args:
        try:
            n = int(args[0])
        except Exception as e:
            return await my_bot.say('`Error: args must be a number`')
    else:
        n = c.randomComicNum()
    url = await c.getImgUrl(n)
    # await my_bot.say('`XKCD comic #' + str(n) + ':`')
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content='`XKCD comic #' + str(n) + ':`', embed=em.set_image(url=url))
    await my_bot.delete_message(ctx.message)


@my_bot.command(pass_context=True)
async def iconify(ctx, *args):
    """turns text into emoji. must have a string following the command"""
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

    await my_bot.delete_message(ctx.message)
    if args:
        args = ' '.join(args) # collapse ares to a string
        iconstring = args.lower()
        return await my_bot.say(make(iconstring))
    else:
        return await my_bot.say('`Error: must specify a string`')
    print('iconify: ' + iconstring)

@my_bot.command(pass_context=True, aliases=['c'])
async def cat(ctx):
    """(also c) random cat picture"""
    print('cat')
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://random.cat/meow') as r:
            res = await r.json()
    em = discord.Embed()
    await my_bot.send_message(ctx.message.channel, content=None, embed=em.set_image(url=res['file']))
    await my_bot.delete_message(ctx.message)

@my_bot.command(pass_context=True, aliases=['d'])
async def dog(ctx):
    """(also d) random dog picture"""
    print('dog')
    await my_bot.delete_message(ctx.message)
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
    await my_bot.send_message(ctx.message.channel, content=None, embed=em.set_image(url=res))

my_bot.run('MzIxMDYxMjE4ODk3MTAwODAy.DBYjHw.IIk2oxT597yadkC0SCIbGMipg98') # Shibbot's Cousin (debate)
