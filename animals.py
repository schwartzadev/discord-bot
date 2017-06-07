import discord
from discord.ext import commands

import json
from random import randint

import aiohttp
import asyncio
import async_timeout

class Animals():
    shib = ''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['c'])
    async def cat(self, ctx):
        """(c) random cat picture"""
        print('cat')
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://random.cat/meow') as r:
                res = await r.json()
                cs.close()
        em = discord.Embed()
        await self.bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=res['file']))
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, aliases=['d'])
    async def dog(self, ctx):
        """(d) random dog picture"""
        print('dog')
        isVideo = True
        while isVideo:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://random.dog/woof.json') as r:
                    res = await r.json()
                    res = res['url']
                    cs.close()
            if res.endswith('.mp4'):
                pass
            else:
                isVideo = False
        em = discord.Embed()
        await self.bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=res))
        await self.bot.delete_message(ctx.message)

    class Shibs():
        data = None
        size = None

        async def start(self):
            with open('config.json') as configFile: # import config
                config = json.load(configFile)
            async with aiohttp.ClientSession() as session:
                url = 'https://api.github.com/repos/RobIsAnxious/shibesbot-db/contents/pictures'
                with async_timeout.timeout(10):
                    auth = aiohttp.BasicAuth(config['github']['username'], password=config['github']['pass'])
                    async with session.get(url, auth=auth) as response:
                        html = await response.text()
                session.close()
                self.data = json.loads(html)
                self.size = len(self.data)

        def getAttr(self, num, attr):
            return self.data[num][attr]

        def getRand(self):
            return randint(1, self.size)

        def getImgUrl(self, num):
            return self.data[num]['download_url']

    @commands.command(pass_context=True, aliases=['s'])
    async def shib(self, ctx):
        """(s) basically hijacks the shibs database to provide shibs"""
        n = self.shib.getRand()
        print('shib')
        em = discord.Embed()
        await self.bot.send_message(ctx.message.channel, content=ctx.message.author.mention, embed=em.set_image(url=self.shib.getImgUrl(n)))
        await self.bot.delete_message(ctx.message)

    async def on_ready(self):
        self.shib = self.Shibs()
        await self.shib.start()
        print('made shib instance')

def setup(bot):
    bot.add_cog(Animals(bot))