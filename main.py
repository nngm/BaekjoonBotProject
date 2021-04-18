import asyncio
import json

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
    descr += '\n/[problem number]\n'
    descr += 'ex) /1000\n'
    descr += '\n/step (step number)\n'
    descr += 'ex) /step\n'
    descr += 'ex) /step 1\n'
    descr += '\n/user [user name]\n'
    descr += 'ex) /user startlink\n'
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
        await ctx.send(url)
    elif ctx.message.content.split()[1].isdecimal():
        num = int(ctx.message.content.split()[1])
        if num == 0:
            await ctx.send(url)
        elif num <= 50:
            url += '/' + str(dic[num])
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.title.string
            embed = discord.Embed()
            embed.set_author(name=title, url=url)
            await ctx.send(content=url, embed=embed)

@bot.command(aliases=['u'])
async def user(ctx):    # user profile
    bj_url = r"https://www.acmicpc.net/user/"
    sv_url = r"https://solved.ac/profile/"

    try:
        user_name = ctx.message.content.split()[1]
    except:
        await ctx.send(f'Type `{help_command} user` for usage.')
        return
    
    bj_url += user_name
    sv_url += user_name

    bj_page = requests.get(bj_url)
    bj_soup = BeautifulSoup(bj_page.content, 'html.parser')
    sv_page = requests.get(sv_url)
    sv_soup = BeautifulSoup(sv_page.content, 'html.parser')

    message = bj_url

    if bj.is404(bj_soup.title.string):
        embed = bj.embed_404()
    else:
        embed = discord.Embed()
        embed.set_author(name=user_name, url=bj_url)
        # tier
    
    # if not sv 404
    message += '\n' + sv_url

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

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content == help_command or message.content.startswith(help_command + ' '):
        await message.channel.send(get_help_message(message))

    if message.content == init_command:
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