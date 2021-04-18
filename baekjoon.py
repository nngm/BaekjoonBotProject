import re

import requests
from bs4 import BeautifulSoup
import discord

color = {"Not": 0x2d2d2d, "Unrated": 0x2d2d2d, "Bronze": 0xad5600,
         "Silver": 0x435f7a, "Gold": 0xec9a00, "Platinum": 0x27e2a4,
         "Diamond": 0x0094fc, "Ruby": 0xff0062}

def is404(title: str) -> bool:
    if title == "Baekjoon Online Judge":
        return True
    else:
        return False

def isvalid(number: str) -> bool:
    return number.isdecimal()

def get_url(number: str) -> str:
    return r"https://www.acmicpc.net/problem/" + number

def embed_404():
    embed=discord.Embed()
    embed.add_field(name="404", value="Not found", inline=False)
    return embed

def get_embed(number: str):
    url = get_url(number)
    
    bj_page = requests.get(url)
    bj_soup = BeautifulSoup(bj_page.content, 'html.parser')
    sv_page = requests.get(r"https://solved.ac/search?query=" + number)
    sv_soup = BeautifulSoup(sv_page.content, 'html.parser')

    html_title = bj_soup.title.string
    if is404(html_title):
        return embed_404()
    
    title = re.sub("^[0-9]+번: ", '', html_title)
    tier = re.sub('" class=".*$', '', str(sv_soup.img))[10:]
    tier_color = color[tier.split()[0]]
    tier_icon = re.sub('^.*src="', '', str(sv_soup.img))[0:-3]

    embed = discord.Embed(title=title, description=tier, color=tier_color)
    embed.set_author(name=number, url=get_url(number), icon_url=tier_icon)
    embed.set_thumbnail(url=tier_icon)
    # embed.add_field(name="제출", value="12074", inline=True)
    # embed.add_field(name="정답", value="5689", inline=True)
    # embed.add_field(name="맞은 사람	", value="4115", inline=True)
    # embed.add_field(name="정답 비율", value="50.103%", inline=True)
    # embed.set_footer(text="분류: ||스포일러||")
    return embed