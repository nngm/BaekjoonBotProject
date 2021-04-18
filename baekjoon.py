import re

from bs4 import BeautifulSoup
import discord

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
    return

def get_embed(number: str):
    html_title = '2357번 최솟값과 최댓값'
    if is404(html_title):
        return embed_404
    
    title = "최솟값과 최댓값"
    tier = "골드 I"
    tier_color = 0xec9a00
    tier_icon = "https://static.solved.ac/tier_small/15.svg"

    embed = discord.Embed(title=title, description=tier, color=tier_color)
    embed.set_author(name=number, url=get_url(number), icon_url=tier_icon)
    embed.set_thumbnail(url=tier_icon)
    # embed.add_field(name="제출", value="12074", inline=True)
    # embed.add_field(name="정답", value="5689", inline=True)
    # embed.add_field(name="맞은 사람	", value="4115", inline=True)
    # embed.add_field(name="정답 비율", value="50.103%", inline=True)
    # embed.set_footer(text="분류: ||스포일러||")
    return embed