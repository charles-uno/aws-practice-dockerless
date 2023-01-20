"""
A single card is stored as a string. We use a class for a collection of cards.
"""


from typing import NamedTuple, Optional, Set
import yaml

from .mana import Mana, mana
from . import helpers


with open("assets/card-data.yaml") as handle:
    CARD_DATA = yaml.safe_load(handle)


class Card(NamedTuple):
    name: str

    def __hash__(self) -> int:
        return tuple.__hash__(self)

    @property
    def slug(self) -> str:
        return helpers.slugify(self.name)

    def __repr__(self):
        return f"Card({repr(self.name)})"

    def __str__(self):
        return helpers.highlight(helpers.squish(self.name), "green")

    @property
    def types(self) -> Set[str]:
        return set(CARD_DATA[self.name].get("type", "").split(","))

    @property
    def is_land(self) -> bool:
        return "land" in self.types

    @property
    def is_spell(self) -> bool:
        return not self.is_land

    @property
    def is_green_creature(self):
        return self.mana_cost >= mana("G") and "creature" in self.types

    @property
    def mana_cost(self) -> Mana:
        m = CARD_DATA[self.name].get("mana_cost")
        assert m is not None
        return mana(m)

    @property
    def enters_tapped(self) -> bool:
        return CARD_DATA[self.name].get("enters_tapped", False)

    @property
    def taps_for(self) -> Mana:
        return mana(CARD_DATA[self.name].get("taps_for", ""))
