import asyncio
import re
import json
import datetime

# import requests
# from bs4 import BeautifulSoup
import discord
from discord.ext import commands

import __token__
import logger
import baekjoon as bj

admins = {279832973841530880}
basic_command_prefix = '/'
bot_name = 'BaekjooneBot'
bot_initial = 'BB'
prefix_file_name = 'prefixes.json'
server_file_name = 'servers.json'
help_command = basic_command_prefix + 'help'
init_command = basic_command_prefix + 'init'
prefixes = {}
servers = {}
invite_link = r"http://baekjoonbot.kro.kr"

def get_help_message(message, by_mention: bool = False) -> str:
    server_id = str(message.guild.id)

    # if message.content == help_command
    if server_id in prefixes:
        descr = f'The prefix for this server is `{prefixes[server_id]}`.\n'
    else:
        descr = f'The prefix for this server is `{basic_command_prefix}`.\n'

    if by_mention:
        return descr

    ansi_init = '\u001b[0m'
    ansi_blue = '\u001b[34m'
    ansi_green = '\u001b[32m'
    ansi_gray = '\u001b[30m'

    try: 
        if message.content.split()[1] == 'mobile':
            ansi_init = ''
            ansi_blue = ''
            ansi_green = ''
            ansi_gray = ''
    except:
        pass

    descr += f'Enter `/help mobile` if you are on mobile.\n'

    descr += f'```ansi'

    descr += f'\n/{ansi_green}<problem number>{ansi_init}\n'
    descr += f'e.g. /1000\n'
    
    descr += f'\n/{ansi_blue}user {ansi_green}<user name>{ansi_init}\n'
    descr += f'e.g. /user solvedac\n'

    descr += f'\n/{ansi_blue}random {ansi_green}[tier]{ansi_init}\n'
    descr += f'e.g. /random {ansi_gray}(which is the same as /random all){ansi_init}\n'
    descr += f'e.g. /random gold lang:ko\n'
    descr += f'e.g. /random s5..g1\n'

    descr += f'\n/{ansi_blue}prefix {ansi_green}<new prefix>{ansi_init}\n'
    descr += f'e.g. /prefix !\n'
    
    descr += f'\n/{ansi_blue}invite{ansi_init}\n'
    descr += f'for the invite link\n'
    
    descr += f'\n/{ansi_blue}step {ansi_green}[step number]{ansi_init}\n'
    descr += f'e.g. /step\n'
    descr += f'e.g. /step 1\n'
    
    descr += f'\n/{ansi_blue}class {ansi_green}[class number]{ansi_init}\n'
    descr += f'e.g. /class\n'
    descr += f'e.g. /class 1\n'

    descr += f'\n/{ansi_blue}lang{ansi_init}\n'
    descr += f'bg cs en fr hr ja ko mn no pl pt ru sv th vi\n'
    
    descr += f'\n*** 사이트 바로가기 ***\n'
    descr += f'/{ansi_blue}replit{ansi_init}\n'
    descr += f'/{ansi_blue}ries{ansi_init}\n'
    descr += f'/{ansi_blue}점투파{ansi_init}\n'
    descr += f'/{ansi_blue}코딩도장{ansi_init}\n'

    descr += f'```'

    return descr

bot = commands.Bot(
    command_prefix=lambda bot, message: prefixes[str(message.guild.id)] 
        if str(message.guild.id) in prefixes else basic_command_prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    global prefixes
    global servers

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

    try:
        with open(server_file_name, 'r') as json_file:
            if json_file.read() == '':
                raise FileNotFoundError
    except FileNotFoundError:
        with open(server_file_name, 'w') as json_file:
            json_file.write(json.dumps({}))
        print('Empty "servers.json" file made.')
    
    with open(server_file_name, 'r') as json_file:
        servers = json.loads(json_file.read())

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
        await ctx.send(f'The prefix for this server has changed to `{new_prefix}`.')

@bot.command(aliases=['s'])
async def step(ctx):    # https://www.acmicpc.net/step
    dic = [ 0, 1, 4, 3, 6,  5,  7,  8, 10, 19, 22,
            9, 49, 50, 18, 34, 16, 48, 33, 11, 12,
           20, 29, 13, 17, 24, 26, 59, 41, 23, 14,
           15, 21, 45, 31, 27, 25, 40, 43, 35, 39,
           47, 37, 38, 36, 42, 44, 60, 28, 30, 58,
           32, 46]
    titles = ["", "입출력과 사칙연산", "조건문", "반복문", "1차원 배열", "함수", "문자열", "기본 수학 1", "기본 수학 2",
              "재귀", "브루트 포스", "정렬", "집합과 맵", "기하 1", "정수론 및 조합론", "백트래킹", "동적 계획법 1",
              "누적 합", "그리디 알고리즘", "스택", "큐, 덱", "분할 정복", "이분 탐색", "우선순위 큐", "동적 계획법 2",
              "그래프와 순회", "최단 경로", "투 포인터", "동적 계획법과 최단거리 역추적", "트리", "유니온 파인드",
              "최소 신장 트리", "트리에서의 동적 계획법", "기하 2", "동적 계획법 3", "문자열 알고리즘 1", "위상 정렬",
              "최소 공통 조상", "강한 연결 요소", "세그먼트 트리", "스위핑", "동적 계획법 4", "컨벡스 헐", "이분 매칭",
              "네트워크 플로우", "MCMF", "더 어려운 수학", "고속 푸리에 변환", "문자열 알고리즘 2", "어려운 구간 쿼리",
              "세그먼트 트리 (Hard)", "동적 계획법 최적화", "매우 어려운 자료구조와 알고리즘 (수정 예정)"]
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
        elif num < len(dic):
            url += '/' + str(dic[num])
            title = titles[num]
            embed = discord.Embed()
            embed.set_author(name=f'{num}. ' + title, url=url)
            await ctx.send(content=url, embed=embed)

@bot.command(aliases=['u'])
async def user(ctx):    # user profile
    bj_url = r"https://www.acmicpc.net/user/"
    ac_url = r"https://solved.ac/profile/"

    try:
        user_name = bj.get_user_name(ctx.message.content.split()[1])
        if user_name is None:
            user_name = ctx.message.content.split()[1]
    except:
        await ctx.send(f'Type `{help_command} user` for usage.')
        return

    # message = bj_url + user_name

    # bj_page = requests.get(bj_url)
    # bj_soup = BeautifulSoup(bj_page.content, 'html.parser')
    
    # if bj.is404(bj_soup.title.string):
    #     embed = bj.embed_404('User')
    # else:
    bj_url += user_name
    ac_url += user_name
    message = bj_url
    
    tier = bj.get_ac_tier(user_name)

    if user_name in bj.ac_administrators:
        tier = 'Administrator'
    if user_name in bj.ac_notratable:
        tier = 'Not ratable'
        
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
            url = r"https://solved.ac/search?query=in_class:" + str(num)
            # page = requests.get(url)
            # soup = BeautifulSoup(page.content, 'html.parser')
            # title = soup.title.string
            embed = discord.Embed()
            embed.set_author(name='CLASS ' + str(num), url=url)
            await ctx.send(content=url, embed=embed)

@bot.command(aliases=['rd', 'rand', 'randomdefense', 'randomdefence'])
async def random(ctx):
    voted_tiers = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby'] + list('bsgpdr')
    
    try:
        tier_range = ctx.message.content.split()[1].lower()
    except:
        tier_range = 'all'
    try:
        arg = ' '.join(ctx.message.content.split()[2:])
    except:
        arg = ''

    if re.match('.+\.\..+', tier_range):
        tier_from, tier_to = tier_range.split('..')

        if tier_from[:-1] in voted_tiers and tier_from[-1] in '12345':
            tier_from = tier_from[0] + tier_from[-1]
        if tier_to[:-1] in voted_tiers and tier_to[-1] in '12345':
            tier_to = tier_to[0] + tier_to[-1]

        if tier_from in voted_tiers:
            tier_from = tier_from[0] + '5'
        if tier_to in voted_tiers:
            tier_to = tier_to[0] + '1'

        if tier_from.isdecimal() and 1 <= int(tier_from) <= 30:
            tier_from = 'bsgpdr'[~-int(tier_from) // 5] + '54321'[~-int(tier_from) % 5]
        if tier_to.isdecimal() and 1 <= int(tier_to) <= 30:
            tier_to = 'bsgpdr'[~-int(tier_to) // 5] + '54321'[~-int(tier_to) % 5]

        tier_range = tier_from + '..' + tier_to
    else:
        if tier_range == 'all' or tier_range == 'a':
            tier_range = 'u..r1'

        if tier_range in voted_tiers:
            tier_range = tier_range[0] + '5..' + tier_range[0] + '1'

        if tier_range[:-1] in voted_tiers and tier_range[-1] in '12345':
            tier_range = tier_range[0] + tier_range[-1]

        if tier_range.isdecimal() and 1 <= int(tier_range) <= 30:
            tier_range = 'bsgpdr'[~-int(tier_range) // 5] + '54321'[~-int(tier_range) % 5]

    if re.match('(u|unrated|0|(b|s|g|p|d|r)(1|2|3|4|5))(\.\.(b|s|g|p|d|r)(1|2|3|4|5))?$', tier_range) is None:
        await ctx.send('Argument is not valid.')
        return

    problem_number = bj.search_tier(tier_range, arg)

    if problem_number is None:
        await ctx.send(content="No problem found")
        return

    url = bj.get_url(problem_number)
    embed = bj.get_embed(problem_number)
    await ctx.send(content=url, embed=embed)

@bot.command(aliases=['language', 'languages'])
async def lang(ctx):
    await ctx.send("Languages available in solved.ac: bg cs en fr hr ja ko mn no pl pt ru sv th vi")

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

@bot.command(aliases=['colour'])
async def color(ctx):
    color_code = ctx.message.content.split()[1]
    import re
    if re.search(r"^[a-fA-F0-9]{6}$", color_code):
        await ctx.send(embed=discord.Embed(title='#'+color_code.upper(), color=int(color_code, 16)))

@bot.event
async def on_message(message):
    global servers
    server = message.guild
    if server.id not in servers or servers[server.id] != server.name:
        servers[server.id] = server.name
        try:
            with open(server_file_name, 'w') as json_file:
                json_file.write(json.dumps(servers))
        except:
            pass

    if message.author.bot:
        return

    if bot.user.mentioned_in(message) and len(message.mentions) == 1:
        if message.reference is None or message.reference.cached_message is None or\
           message.reference.cached_message.author != bot.user:
            await message.channel.send(get_help_message(message, True))

    if message.content == help_command or message.content.startswith(help_command + ' '):
        await message.channel.send(get_help_message(message))

    if message.content.startswith(init_command) and message.author.id in admins:
        if len(message.content.split()) > 1:
            server_id = message.content.split()[1]
            prefixes[server_id] = '/'
            print('command initialized in', server_id)

    command_prefix = prefixes[str(message.guild.id)] if str(message.guild.id) in prefixes\
                     else basic_command_prefix

    if message.content.startswith(command_prefix) and bj.isvalid(message.content[len(command_prefix):]):
        problem_number = message.content[len(command_prefix):]
        url = bj.get_url(problem_number)
        embed = bj.get_embed(problem_number)
        await message.channel.send(content=url, embed=embed)

    await bot.process_commands(message)

if __name__ == '__main__':
    bot.run(__token__.get_token())
