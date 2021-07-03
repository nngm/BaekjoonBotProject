import re

import requests
from bs4 import BeautifulSoup
import discord

color = {"Not": 0x2d2d2d, "Unrated": 0x2d2d2d, "Bronze": 0xad5600,
         "Silver": 0x435f7a, "Gold": 0xec9a00, "Platinum": 0x27e2a4,
         "Diamond": 0x0094fc, "Ruby": 0xff0062, "Master": 0xb300e0}

emoji = {"Unrated": "<:unranked:833235211181490186>", 
         "Not ratable": "<:notratable:833235211121852427>",
         "Bronze V": "<:bronze5:833235210476191764>",
         "Bronze IV": "<:bronze4:833235210380247050>",
         "Bronze III": "<:bronze3:833235210627186688>",
         "Bronze II": "<:bronze2:833235210187046922>",
         "Bronze I": "<:bronze1:833235209608364053>",
         "Silver V": "<:silver5:833235211213865010>",
         "Silver IV": "<:silver4:833235210908336158>",
         "Silver III": "<:silver3:833235210920525835>",
         "Silver II": "<:silver2:833235211121983518>",
         "Silver I": "<:silver1:833235211051204628>",
         "Gold V": "<:gold5:833235210715529227>",
         "Gold IV": "<:gold4:833235210534387763>",
         "Gold III": "<:gold3:833235210945691648>",
         "Gold II": "<:gold2:833235210468196383>",
         "Gold I": "<:gold1:833235210408689665>",
         "Platinum V": "<:platinum5:833235211151212544>",
         "Platinum IV": "<:platinum4:833235210925244466>",
         "Platinum III": "<:platinum3:833235211155537951>",
         "Platinum II": "<:platinum2:833235210757734431>",
         "Platinum I": "<:platinum1:833235210996416522>",
         "Diamond V": "<:diamond5:833235209931456573>",
         "Diamond IV": "<:diamond4:833235209977724939>",
         "Diamond III": "<:diamond3:833235210346692608>",
         "Diamond II": "<:diamond2:833235210346561536>",
         "Diamond I": "<:diamond1:833235210165682206>",
         "Ruby V": "<:ruby5:833235211164450836>",
         "Ruby IV": "<:ruby4:833235210858004480>",
         "Ruby III": "<:ruby3:833235211121852437>",
         "Ruby II": "<:ruby2:833235211021058050>",
         "Ruby I": "<:ruby1:833235210958929940>",
         "Master": "<:master:857632512334364722>"}

def rom2num(number: str) -> str:
    number = re.sub(' v$', '5', number)
    number = re.sub(' iv$', '4', number)
    number = re.sub(' iii$', '3', number)
    number = re.sub(' ii$', '2', number)
    number = re.sub(' i$', '1', number)
    return number

def is404(title: str) -> bool:
    if title == "Baekjoon Online Judge":
        return True
    else:
        return False

def get_ac_tier(content: str) -> str:
    tag = re.search('<div><div>AC RATING</div>.* -->[a-zA-Z]+ ?[a-zA-Z]*</span></div>', content)

    if tag is None:
        return
    
    return re.search('[a-zA-Z]+ ?[a-zA-Z]*</span></div>$', tag.group()).group()[:-13]

def isvalid(number: str) -> bool:
    return number.isdecimal()

def get_url(number: str) -> str:
    return r"https://www.acmicpc.net/problem/" + str(int(number))

def embed_404(what: str):
    embed=discord.Embed()
    embed.add_field(name="404", value=what + " not found", inline=False)
    return embed

def set_embed(title: str, tier: str):
    tier_color = color[tier.split()[0]]
    tier_emoji = emoji[tier] + ' '

    return discord.Embed(title=title, description=tier_emoji+tier, color=tier_color)

def get_embed(number: str):
    number = str(int(number))
    url = get_url(number)
    
    bj_page = requests.get(url)
    bj_soup = BeautifulSoup(bj_page.content, 'html.parser')
    ac_page = requests.get(r"https://solved.ac/search?query=" + number)
    ac_soup = BeautifulSoup(ac_page.content, 'html.parser')

    html_title = bj_soup.title.string
    if is404(html_title):
        return embed_404('Problem')
    
    title = re.sub('^[0-9]+번: ', '', html_title)
    tier = re.sub('" class=".*$', '', str(ac_soup.img))[10:]
    if number == '9999':
        tier = 'Not ratable'
    tier_icon = re.sub('^.*src="', '', str(ac_soup.img))[:-3]

    embed = set_embed(title, tier)
    # embed.set_thumbnail(url=tier_icon)
    embed.set_author(name=number, url=get_url(number))

    # https://mochalatte.dev/posts/today-i-learned/programming/py-crawling-request

    # row_tag = bj_soup.select_one('body > div.wrapper > div.container.content > div.row ')
    # if re.search('<section id="problem_tags">', str(row_tag)):
    #     text = '분류: '
    #     pattern = '<a href="/problem/tag/[0-9]+" class="spoiler-link">.+</a>'
        
    #     for tag in re.findall(re.search(pattern, str(row_tag))):
    #         pattern2 = '<a href="/problem/tag/[0-9]+" class="spoiler-link">'
    #         text += re.sub(pattern2, '', tag)[:-4] + ', '
        
    #     embed.set_footer(text=text[:-2])
        
    # embed.add_field(name="제출", value="12074", inline=True)
    # embed.add_field(name="정답", value="5689", inline=True)
    # embed.add_field(name="맞은 사람	", value="4115", inline=True)
    # embed.add_field(name="정답 비율", value="50.103%", inline=True)
    return embed