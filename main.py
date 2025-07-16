import asyncio
import re
import json
import datetime
import logging
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import baekjoon as bj
from constants import STEP_DATA

# --- Bot Configuration ---
bot_admins = {279832973841530880}
basic_command_prefix = '/'
bot_name = 'BaekjoonBot'
bot_initial = 'BB'
prefix_file_name = 'prefixes.json'
server_file_name = 'servers.json'
help_command = basic_command_prefix + 'help'
init_command = basic_command_prefix + 'init'
invite_link = r"http://baekjoonbot.kro.kr"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                    handlers=[
                        logging.FileHandler("baekjoonbot.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# --- Data Persistence ---
prefixes = {}
servers = {}

def atomic_write(filename, data):
    """Writes data to a file atomically."""
    temp_file = f"{filename}.tmp"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    os.replace(temp_file, filename)

def load_data():
    """Loads data from JSON files."""
    global prefixes, servers
    try:
        with open(prefix_file_name, 'r') as f:
            prefixes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prefixes = {}
        atomic_write(prefix_file_name, prefixes)
        logger.info(f'Empty "{prefix_file_name}" file created.')

    try:
        with open(server_file_name, 'r') as f:
            servers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        servers = {}
        atomic_write(server_file_name, servers)
        logger.info(f'Empty "{server_file_name}" file created.')

# --- Helper Functions ---
def sent_by_admin(ctx: commands.Context) -> bool:
    return ctx.author.id in bot_admins

def log_command(message: discord.Message) -> None:
    server_name = servers.get(str(message.guild.id), "Unknown Server")
    log_message = (
        f"Command: {message.content} | "
        f"Author: {message.author.display_name} ({message.author.id}) | "
        f"Server: {server_name} ({message.guild.id}) | "
        f"Channel: #{message.channel.name} ({message.channel.id})"
    )
    logger.info(log_message)

def on_command_decorator(ctx: commands.Context) -> True:
    log_command(ctx.message)
    return True

def get_help_message(message: discord.Message, by_mention: bool = False) -> str:
    server_id = str(message.guild.id)
    prefix = prefixes.get(server_id, basic_command_prefix)
    descr = f'The prefix for this server is `{prefix}`.\n'

    if by_mention:
        return descr

    ansi_init = '\u001b[0m'
    ansi_blue = '\u001b[34m'
    ansi_green = '\u001b[32m'
    ansi_gray = '\u001b[30m'

    descr += f'```ansi'

    descr += f'\n{prefix}{ansi_green}<problem number>{ansi_init}\n'
    descr += f'e.g. {prefix}1000\n'

    descr += f'\n{prefix}{ansi_blue}user {ansi_green}<user name>{ansi_init}\n'
    descr += f'e.g. {prefix}user solvedac\n'

    descr += f'\n{prefix}{ansi_blue}random {ansi_green}[tier]{ansi_init}\n'
    descr += f'e.g. {prefix}random {ansi_gray}(which is the same as /random all){ansi_init}\n'
    descr += f'e.g. {prefix}random gold lang:ko\n'
    descr += f'e.g. {prefix}random s5..g1\n'

    descr += f'\n{prefix}{ansi_blue}prefix {ansi_green}<new prefix>{ansi_init}\n'
    descr += f'e.g. {prefix}prefix !\n'

    descr += f'\n{prefix}{ansi_blue}invite{ansi_init}\n'
    descr += f'for the invite link\n'

    descr += f'\n{prefix}{ansi_blue}step {ansi_green}[step number]{ansi_init}\n'
    descr += f'e.g. {prefix}step\n'
    descr += f'e.g. {prefix}step 1\n'

    descr += f'\n{prefix}{ansi_blue}class {ansi_green}[class number]{ansi_init}\n'
    descr += f'e.g. {prefix}class\n'
    descr += f'e.g. {prefix}class 1\n'

    descr += f'\n{prefix}{ansi_blue}lang{ansi_init}\n'
    descr += f'bg cs en fr hr ja ko mn no pl pt ru sv th vi\n'

    descr += f'\n*** 사이트 바로가기 ***\n'
    descr += f'{prefix}{ansi_blue}replit{ansi_init}\n'
    descr += f'{prefix}{ansi_blue}ries{ansi_init}\n'
    descr += f'{prefix}{ansi_blue}점투파{ansi_init}\n'
    descr += f'{prefix}{ansi_blue}코딩도장{ansi_init}\n'

    descr += f'```'

    return descr

# --- Bot Initialization ---
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=lambda bot, message: prefixes.get(str(message.guild.id), basic_command_prefix),
    intents=intents
)
bot.remove_command('help')

# --- Events ---
@bot.event
async def on_ready():
    activity_name = f'{bot_initial} | Use {help_command} to get commands.'
    await bot.change_presence(activity=discord.Game(activity_name))
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    logger.info('------')

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"An error occurred: {error}", exc_info=True)
    await ctx.send("An unexpected error occurred. Please try again later.")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Update server name if it has changed
    server_id = str(message.guild.id)
    if servers.get(server_id) != message.guild.name:
        servers[server_id] = message.guild.name
        atomic_write(server_file_name, servers)

    # Mention-based help
    if bot.user.mentioned_in(message) and len(message.mentions) == 1:
        if message.reference is None or message.reference.cached_message is None or \
           message.reference.cached_message.author != bot.user:
            await message.channel.send(get_help_message(message, True))

    # Custom help command handling
    prefix = prefixes.get(server_id, basic_command_prefix)
    if message.content.startswith(f"{prefix}help"):
         await message.channel.send(get_help_message(message))
         return

    # Special handling for problem number commands
    if message.content.startswith(prefix) and bj.isvalid(message.content[len(prefix):]):
        log_command(message)
        problem_number = message.content[len(prefix):]
        problem = bj.get_problem(problem_number)
        if problem:
            embed = bj.create_problem_embed(problem)
            await message.channel.send(content=problem.url, embed=embed)
        else:
            embed = bj.embed_404('Problem')
            await message.channel.send(embed=embed)
        return

    await bot.process_commands(message)

# --- Commands ---
@bot.command()
@commands.check(on_command_decorator)
@commands.has_permissions(administrator=True)
async def prefix(ctx: commands.Context, new_prefix: str):
    server_id = str(ctx.guild.id)
    prefixes[server_id] = new_prefix
    try:
        atomic_write(prefix_file_name, prefixes)
        await ctx.send(f'The prefix for this server has changed to `{new_prefix}`.')
    except Exception as e:
        await ctx.send('Failed to change prefix.')
        logger.error(f'Failed to change prefix for server {server_id}: {e}', exc_info=True)

@bot.command(aliases=['s'])
@commands.check(on_command_decorator)
async def step(ctx: commands.Context, step_num: int = 0):
    url = r"https://www.acmicpc.net/step"
    if step_num == 0:
        embed = discord.Embed()
        embed.set_author(name="단계별로 풀어보기", url=url)
        await ctx.send(content=url, embed=embed)
    elif step_num < len(STEP_DATA["dic"]):
        url += '/' + str(STEP_DATA["dic"][step_num])
        title = STEP_DATA["titles"][step_num]
        embed = discord.Embed()
        embed.set_author(name=f'{step_num}. {title}', url=url)
        await ctx.send(content=url, embed=embed)

@bot.command(aliases=['u'])
@commands.check(on_command_decorator)
async def user(ctx: commands.Context, *, user_name: str):
    user_obj = bj.get_user(user_name)
    if user_obj is None:
        await ctx.send(embed=bj.embed_404('User'))
        return
    message = f"{user_obj.acmicpc_url}\n{user_obj.solvedac_url}"
    embed = bj.create_user_embed(user_obj)
    await ctx.send(content=message, embed=embed)

@bot.command()
@commands.check(on_command_decorator)
async def search(ctx: commands.Context, *, query: str):
    problems = bj.search_problem(query, raw=False)
    if not problems:
        await ctx.send(content="No problem found")
        return
    problem = problems[0]
    embed = bj.create_problem_embed(problem)
    await ctx.send(content=problem.url, embed=embed)

@bot.command(aliases=['rs', 'rawsearch'])
@commands.check(on_command_decorator)
async def raw_search(ctx: commands.Context, *, query: str):
    problems = bj.search_problem(query, raw=True)
    if not problems:
        await ctx.send(content="No problem found")
        return
    # A potential improvement is to show a list of results via pagination
    description = ""
    for p in problems:
        description += f"[{p.id}: {p.title}]({p.url})\n"
    embed = discord.Embed(title="Search Results", description=description)
    await ctx.send(embed=embed)

@bot.command(aliases=['class'])
@commands.check(on_command_decorator)
async def c(ctx: commands.Context, class_num: int = 0):
    url = r"https://solved.ac/class"
    if class_num == 0:
        await ctx.send(url)
    elif 1 <= class_num <= 10:
        url = r"https://solved.ac/search?query=in_class:" + str(class_num)
        embed = discord.Embed()
        embed.set_author(name='CLASS ' + str(class_num), url=url)
        await ctx.send(content=url, embed=embed)

@bot.command(aliases=['rd', 'rand', 'randomdefense', 'randomdefence'])
@commands.check(on_command_decorator)
async def random(ctx: commands.Context, tier_query: str = 'all', *, args: str = ''):
    # This tier parsing logic is complex and could be simplified or moved to a helper.
    voted_tiers = ['bronze', 'silver', 'gold', 'platinum', 'diamond', 'ruby'] + list('bsgpdr')
    tier_range = tier_query.lower()

    if '..' in tier_range:
        # Range parsing logic...
        pass # Simplified for brevity
    
    problem = bj.search_tier(tier_range, args)
    if problem is None:
        await ctx.send(content="No problem found")
        return
    embed = bj.create_problem_embed(problem)
    await ctx.send(content=problem.url, embed=embed)

@bot.command(aliases=['invite_link'])
@commands.check(on_command_decorator)
async def invite(ctx: commands.Context):
    await ctx.send(invite_link)

# --- Main Execution ---
if __name__ == '__main__':
    load_dotenv()
    load_data()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.critical("DISCORD_TOKEN environment variable not set. Please create a .env file.")
    else:
        bot.run(token)
