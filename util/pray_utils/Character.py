import random


class Character:
    default_values = {
        "max_health": 20,
        "health": 20,
        "max_level": 20,
        "level": 1,
        # Material inventory non-unique "name":amount
        "materials": {},
        # Items inventory unique list of item-dicts
        "items": [],
        # Equipped inventory, unique equipped items
        "equipped": [],
        # Achievements that increase skills string set
        "titles": set(),
        # Temporary alterations to stats
        "effects": set(),
        # permanent level up apply bonuses to/enable certain stats/actions list of skill objects
        "skills": [],
    }
    named_attrs = [
        "max_health",
        "health",
        "max_level",
        "level",
        "materials",
        "items",
        "equipped",
        "titles",
        "effects",
    ]

    def __init__(self, owner_id, **info):
        self.owner = owner_id
        self.name = info.pop("name", "Adventurer%d" % random.randint(0, 1024))
        for attr in self.named_attrs:
            setattr(self, attr, info.pop(attr, self.default_values[attr]))
        # TODO: implement loading from dict

        self.others = {k: v for k, v in info.items()}
