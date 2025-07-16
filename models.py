from dataclasses import dataclass
from typing import Union

@dataclass
class Problem:
    """Represents a single Baekjoon problem from the solved.ac API."""
    id: int
    title: str
    level: int
    is_level_locked: bool
    is_sprout: bool

    @classmethod
    def from_api_response(cls, data: dict) -> 'Problem':
        """Creates a Problem instance from the API's JSON response."""
        return cls(
            id=data.get("problemId", 0),
            title=data.get("titleKo", "Unknown Title"),
            level=data.get("level", 0),
            is_level_locked=data.get("isLevelLocked", False),
            is_sprout=data.get("sprout", False)
        )

    @property
    def url(self) -> str:
        """Returns the URL for the problem on the BOJ website."""
        return f"https://www.acmicpc.net/problem/{self.id}"

@dataclass
class User:
    """Represents a single Baekjoon user from the solved.ac API."""
    handle: str
    tier: int
    solved_count: int
    rating: int

    @classmethod
    def from_api_response(cls, data: dict) -> 'User':
        """Creates a User instance from the API's JSON response."""
        return cls(
            handle=data.get("handle", "Unknown User"),
            tier=data.get("tier", 0),
            solved_count=data.get("solvedCount", 0),
            rating=data.get("rating", 0)
        )

    @property
    def acmicpc_url(self) -> str:
        """Returns the URL for the user's profile on the BOJ website."""
        return f"https://www.acmicpc.net/user/{self.handle}"

    @property
    def solvedac_url(self) -> str:
        """Returns the URL for the user's profile on the solved.ac website."""
        return f"https://solved.ac/profile/{self.handle}"


class TierData:
    """A single source of truth for all tier-related data."""
    _TIER_INFO_BY_LEVEL = {
        0: ("Unrated", 0x2d2d2d, "<:unranked:833235211181490186>"),
        1: ("Bronze V", 0xad5600, "<:bronze5:833235210476191764>"),
        2: ("Bronze IV", 0xad5600, "<:bronze4:833235210380247050>"),
        3: ("Bronze III", 0xad5600, "<:bronze3:833235210627186688>"),
        4: ("Bronze II", 0xad5600, "<:bronze2:833235210187046922>"),
        5: ("Bronze I", 0xad5600, "<:bronze1:833235209608364053>"),
        6: ("Silver V", 0x435f7a, "<:silver5:833235211213865010>"),
        7: ("Silver IV", 0x435f7a, "<:silver4:833235210908336158>"),
        8: ("Silver III", 0x435f7a, "<:silver3:833235210920525835>"),
        9: ("Silver II", 0x435f7a, "<:silver2:833235211121983518>"),
        10: ("Silver I", 0x435f7a, "<:silver1:833235211051204628>"),
        11: ("Gold V", 0xec9a00, "<:gold5:833235210715529227>"),
        12: ("Gold IV", 0xec9a00, "<:gold4:833235210534387763>"),
        13: ("Gold III", 0xec9a00, "<:gold3:833235210945691648>"),
        14: ("Gold II", 0xec9a00, "<:gold2:833235210468196383>"),
        15: ("Gold I", 0xec9a00, "<:gold1:833235210408689665>"),
        16: ("Platinum V", 0x27e2a4, "<:platinum5:833235211151212544>"),
        17: ("Platinum IV", 0x27e2a4, "<:platinum4:833235210925244466>"),
        18: ("Platinum III", 0x27e2a4, "<:platinum3:833235211155537951>"),
        19: ("Platinum II", 0x27e2a4, "<:platinum2:833235210757734431>"),
        20: ("Platinum I", 0x27e2a4, "<:platinum1:833235210996416522>"),
        21: ("Diamond V", 0x0094fc, "<:diamond5:833235209931456573>"),
        22: ("Diamond IV", 0x0094fc, "<:diamond4:833235209977724939>"),
        23: ("Diamond III", 0x0094fc, "<:diamond3:833235210346692608>"),
        24: ("Diamond II", 0x0094fc, "<:diamond2:833235210346561536>"),
        25: ("Diamond I", 0x0094fc, "<:diamond1:833235210165682206>"),
        26: ("Ruby V", 0xff0062, "<:ruby5:833235211164450836>"),
        27: ("Ruby IV", 0xff0062, "<:ruby4:833235210858004480>"),
        28: ("Ruby III", 0xff0062, "<:ruby3:833235211121852437>"),
        29: ("Ruby II", 0xff0062, "<:ruby2:833235211021058050>"),
        30: ("Ruby I", 0xff0062, "<:ruby1:833235210958929940>"),
        31: ("Master", 0xb300e0, "<:master:860880287172788265>"),
    }

    _SPECIAL_TIERS_BY_NAME = {
        "Not ratable": (0x2d2d2d, "<:notratable:833235211121852427>"),
        "Administrator": (0x17ce3a, "<:admin:863338449935138847>"),
        "새싹": (0x96cc00, "<:sprout:999597535863783444>"),
    }

    def get_by_level(self, level: int) -> Union[tuple, None]:
        """Efficiently get tier info by its numeric level."""
        return self._TIER_INFO_BY_LEVEL.get(level)

    def get_by_name(self, name: str) -> Union[tuple, None]:
        """Get special tier info by name."""
        return self._SPECIAL_TIERS_BY_NAME.get(name)

tiers = TierData()
