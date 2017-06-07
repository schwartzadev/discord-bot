#!/usr/bin/env python

import json
from random import randint

import aiohttp
import asyncio
import async_timeout

import discord
from discord.ext.commands import Bot

startup_extensions = ['members', 'animals']

print('running...')
my_bot = Bot(command_prefix = '!!')

with open('config.json') as configFile: # import config
    config = json.load(configFile)

@my_bot.event
async def on_ready():
    print('Logged in as: ' + my_bot.user.name + ' (' + my_bot.user.id + ')')
    print('------------------')

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
            session.close()

    def randomComicNum(self):
        return randint(1, self.totalComics)

    async def setCount(self):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://xkcd.com/info.0.json')
            d = json.loads(html)
            self.totalComics = d['num']
            session.close()

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


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            my_bot.load_extension(extension)
            print('imported ' + extension)
        except Exception as e:
            raise(e)
            # exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


my_bot.run(config['botkey']) # Shibbot's Cousin (debate)
