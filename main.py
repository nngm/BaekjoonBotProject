import asyncio
import json
import datetime

import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

import __token__
import logger
import baekjoon as bj

basic_command_prefix = '/'
bot_name = 'BaekjooneBot'
bot_initial = 'BB'
prefix_file_name = 'prefixes.json'
help_command = basic_command_prefix + 'help'
init_command = basic_command_prefix + 'init'
prefixes = {}
invite_link = r"https://baekjoonbot.kro.kr"

def get_help_message(message) -> str:
    server_id = str(message.guild.id)

    # if message.content == help_command
    if server_id in prefixes:
        descr = f'Prefix for this server is `{prefixes[server_id]}`.'
    else:
        descr = f'Prefix for this server is `{basic_command_prefix}`.'
    descr += '\n```'
    descr += '/prefix [new prefix]\n'
    descr += 'ex) /prefix !\n'
    descr += '\n/invite\n'
    descr += 'for the invite link\n'
    descr += '\n/[problem number]\n'
    descr += 'ex) /1000\n'
    descr += '\n/step (step number)\n'
    descr += 'ex) /step\n'
    descr += 'ex) /step 1\n'
    descr += '\n/user [user name]\n'
    descr += 'ex) /user startlink\n'
    descr += '\n/class (class number)\n'
    descr += 'ex) /class\n'
    descr += 'ex) /class 1\n'
    descr += '\n*** 사이트 바로가기 ***\n'
    descr += '/replit\n'
    descr += '/ries\n'
    descr += '/점투파\n'
    descr += '/코딩도장\n'
    descr += '```'
    return descr

bot = commands.Bot(
    command_prefix=lambda bot, message: prefixes[str(message.guild.id)] 
        if str(message.guild.id) in prefixes else basic_command_prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    global prefixes

    # custom activity for bots are not available now
    activity_name = f'{bot_initial} | Use {help_command} ' + \
                     'to get current prefix and commands.'
    await bot.change_presence(activity=discord.Game(activity_name))

    try:
        with open(prefix_file_name, 'r') as json_file:
            if json_file.read() == '':
                raise FileNotFoundError
    except FileNotFoundError:
        with open(prefix_file_name, 'w') as json_file:
            json_file.write(json.dumps({}))
        print('Empty "prefixes.json" file made.')
    
    with open(prefix_file_name, 'r') as json_file:
        prefixes = json.loads(json_file.read())

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(datetime.datetime.today().strftime('%Y-%m-%d %X'))
    print('------')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        return
    raise error

@bot.command()
async def prefix(ctx):  # change prefix
    server_id = str(ctx.guild.id)
    
    try:
        new_prefix = ctx.message.content.split()[1]
    except:
        await ctx.send(f'Type `{help_command} prefix` for usage.')
        return
    
    prefixes[server_id] = new_prefix
    
    try:
        with open(prefix_file_name, 'w') as json_file:
            json_file.write(json.dumps(prefixes))
        # raise Exception('Test')
    except Exception as e:
        await ctx.send('Failed to change prefix.')
        logger.log(f'{e}: An exception occurred while changing prefix.')
        logger.log(f'server: {server_id} ({ctx.guild.name})')
        logger.log(f'author: {ctx.author.id} ({ctx.author.name})')
        logger.log(f'used command: {ctx.message.content}')
    else:
        await ctx.send(f'Prefix for this server changed to `{new_prefix}`')

@bot.command(aliases=['s'])
async def step(ctx):    # https://www.acmicpc.net/step
    dic = [0, 1, 4, 3, 2, 6, 5, 7, 8, 10, 19, 22, 9, 49, 34, 16, 33, 18, 11, 12, 20,
           29, 13, 17, 24, 26, 59, 41, 23, 14, 15, 21, 45, 31, 27, 25, 40, 43, 35, 39, 47,
           37, 38, 36, 42, 44, 60, 28, 30, 32, 46]
    url = r"https://www.acmicpc.net/step"
    if len(ctx.message.content.split()) == 1:
        embed = discord.Embed()
        embed.set_author(name="단계별로 풀어보기", url=url)
        await ctx.send(content=url, embed=embed)
    elif ctx.message.content.split()[1].isdecimal():
        num = int(ctx.message.content.split()[1])
        if num == 0:
            embed = discord.Embed()
            embed.set_author(name="단계별로 풀어보기", url=url)
            await ctx.send(content=url, embed=embed)
        elif num <= 50:
            url += '/' + str(dic[num])
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.title.string
            embed = discord.Embed()
            embed.set_author(name=f'{num}. ' + title, url=url)
            await ctx.send(content=url, embed=embed)

@bot.command(aliases=['u'])
async def user(ctx):    # user profile
    bj_url = r"https://www.acmicpc.net/user/"
    ac_url = r"https://solved.ac/profile/"

    try:
        user_name = ctx.message.content.split()[1]
    except:
        await ctx.send(f'Type `{help_command} user` for usage.')
        return
    
    bj_url += user_name
    ac_url += user_name

    bj_page = requests.get(bj_url)
    bj_soup = BeautifulSoup(bj_page.content, 'html.parser')
    ac_page = requests.get(ac_url)
    ac_soup = BeautifulSoup(ac_page.content, 'html.parser')

    message = bj_url

    if bj.is404(bj_soup.title.string):
        embed = bj.embed_404('User')
    else:
        tier = bj.get_ac_tier(str(ac_soup))
        if tier is not None:
            embed = bj.set_embed(user_name, tier)
            message += '\n' + ac_url
        else:
            embed = discord.Embed(title=user_name)

        embed.set_author(name='User', url=bj_url)

    await ctx.send(content=message, embed=embed)

@bot.command(aliases=['class'])
async def c(ctx):   # solved.ac/class
    url = r"https://solved.ac/class"
    if len(ctx.message.content.split()) == 1:
        await ctx.send(url)
    elif ctx.message.content.split()[1].isdecimal():
        num = int(ctx.message.content.split()[1])
        if num == 0:
            await ctx.send(url)
        elif num <= 10:
            url += '/' + str(num)
            # page = requests.get(url)
            # soup = BeautifulSoup(page.content, 'html.parser')
            # title = soup.title.string
            embed = discord.Embed()
            embed.set_author(name='CLASS ' + str(num), url=url)
            await ctx.send(content=url, embed=embed)

@bot.command(aliases=['repl'])
async def replit(ctx):
    await ctx.send(r"https://repl.it/")

@bot.command()
async def ries(ctx):
    await ctx.send(r"https://blog.naver.com/PostList.nhn?blogId=kks227&categoryNo=299")

@bot.command()
async def 점투파(ctx):
    await ctx.send(r"https://wikidocs.net/book/1")

@bot.command()
async def 코딩도장(ctx):
    await ctx.send(r"https://dojang.io/course/view.php?id=7")

@bot.command(aliases=['invite_link'])
async def invite(ctx):
    await ctx.send(invite_link)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content == help_command or message.content.startswith(help_command + ' '):
        await message.channel.send(get_help_message(message))

    if message.content == init_command + ' ' + str(message.guild.id):
        server_id = str(message.guild.id)
        print('command initialized in', server_id)
        prefixes[server_id] = '/'

    command_prefix = prefixes[str(message.guild.id)] if str(message.guild.id) in prefixes\
                     else basic_command_prefix

    if message.content.startswith(command_prefix) and bj.isvalid(message.content[1:]):
        problem_number = message.content[1:]
        url = bj.get_url(problem_number)
        embed = bj.get_embed(problem_number)
        await message.channel.send(content=url, embed=embed)

    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(__token__.get_token())