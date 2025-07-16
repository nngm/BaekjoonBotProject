# https://solvedac.github.io/unofficial-documentation/

import json
from typing import List, Union

import requests
import discord

from models import Problem, User, tiers

ac_administrators = {'solvedac'}
ac_notratable = {'startlink'}


def get_user(user_name: str) -> Union[User, None]:
    url = r"https://solved.ac/api/v3/user/show?handle=" + user_name
    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code == 404:
        return None

    return User.from_api_response(response.json())


def isvalid(number: str) -> bool:
    return number.isdecimal()


def embed_404(what: str):
    embed = discord.Embed()
    embed.add_field(name="404", value=what + " not found", inline=False)
    return embed


def create_problem_embed(problem: Problem) -> discord.Embed:
    """Creates a Discord embed from a Problem object."""
    tier_name_override = None
    if problem.is_level_locked:
        if problem.level == 0:
            tier_name_override = "Not ratable"
        elif problem.is_sprout:
            tier_name_override = "새싹"

    if tier_name_override:
        tier_info = tiers.get_by_name(tier_name_override)
        name, color, emoji = tier_info
        description = f"{emoji} {tier_name_override}"
    else:
        tier_info = tiers.get_by_level(problem.level)
        if tier_info:
            name, color, emoji = tier_info
            description = f"{emoji} {name}"
        else:
            # Fallback for unknown tier
            description = "Unknown Tier"
            color = 0x2d2d2d

    embed = discord.Embed(title=problem.title, description=description, color=color)
    embed.set_author(name=str(problem.id), url=problem.url)
    return embed


def create_user_embed(user: User) -> discord.Embed:
    """Creates a Discord embed from a User object."""
    tier_name_override = None
    if user.handle in ac_administrators:
        tier_name_override = "Administrator"
    if user.handle in ac_notratable:
        tier_name_override = "Not ratable"

    if tier_name_override:
        tier_info = tiers.get_by_name(tier_name_override)
        name, color, emoji = tier_info
        description = f"{emoji} {tier_name_override}"
    else:
        tier_info = tiers.get_by_level(user.tier)
        if tier_info:
            name, color, emoji = tier_info
            description = f"{emoji} {name}"
        else:
            # Fallback for unknown tier
            description = "Unknown Tier"
            color = 0x2d2d2d
    
    embed = discord.Embed(title=user.handle, description=description, color=color)
    embed.set_author(name='User', url=user.acmicpc_url)
    return embed


def get_problem(problem_id: str) -> Union[Problem, None]:
    problem_id = str(int(problem_id))
    api_url = r"https://solved.ac/api/v3/problem/show?problemId=" + problem_id
    response = requests.get(
        api_url, headers={'Content-Type': 'application/json'})

    if response.status_code == 404:
        return None

    return Problem.from_api_response(response.json())


def search_tier(tier_range: str, arg: str) -> Union[Problem, None]:
    api_url = r"https://solved.ac/api/v3/search/problem?sort=random&query=solvable:true tier:"
    response = requests.get(api_url + tier_range + ' ' +
                            arg, headers={'Content-Type': 'application/json'})

    if response.status_code == 404:
        return None

    try:
        problem_data = response.json()["items"][0]
    except (IndexError, KeyError):
        return None

    return Problem.from_api_response(problem_data)


def search_problem(query: str, raw: bool) -> List[Problem]:
    api_url = r"https://solved.ac/api/v3/search/problem?query="

    if not raw:
        query = '"' + query + '"'
    
    response = requests.get(api_url + query, headers={'Content-Type': 'application/json'})

    if response.status_code == 404:
        return []

    response_json = response.json()
    if not raw and response_json.get("count", 0) == 0:
        raw = True
        query = query[1:-1]
        response = requests.get(api_url + query, headers={'Content-Type': 'application/json'})
        if response.status_code == 404:
            return []
        response_json = response.json()

    limit = 5 if raw else 1
    problems_data = response_json.get("items", [])[:limit]

    return [Problem.from_api_response(p) for p in problems_data]
