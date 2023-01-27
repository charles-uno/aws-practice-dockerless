from typing import List
from django.http import HttpRequest
from django.http.request import QueryDict

from .amulet_model import OpenerDict


def get_opener_dict_from_request(request: HttpRequest) -> OpenerDict:
    hand = _get_list_from_query_qict(request.GET, "hand")
    library = _get_list_from_query_qict(request.GET, "library")
    on_the_play = _get_bool_from_query_dict(request.GET, "on_the_play")
    return {
        "hand": hand,
        "library": library,
        "on_the_play": on_the_play,
    }


def _get_bool_from_query_dict(qd: QueryDict, key: str) -> bool:
    val = qd.get(key)
    if val == "true":
        return True
    elif val == "false":
        return False
    else:
        raise ValueError(f"unable to get bool from {repr(val)}")


def _get_list_from_query_qict(qd: QueryDict, key: str) -> List[str]:
    val = qd.get(key)
    if isinstance(val, list):
        return [str(x) for x in val]
    elif isinstance(val, str):
        # htmx gets a bit confused when you put structured data into hx-vals so
        # we just join our lists with semicolons.
        return val.split(";")
    else:
        raise ValueError(f"unable to get List[str] from {repr(val)}")


def load_deck_list() -> List[str]:
    deck_list = []
    with open("assets/deck-list.txt") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            n, card_name = line.rstrip().split(None, 1)
            deck_list += [card_name] * int(n)
    return deck_list
