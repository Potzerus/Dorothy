class Skill:

    def __init__(self, char, **info):
        self.char = char
        self.name = info['name']
        self.level = info['level']
        self.xp = info['xp']

    def __iadd__(self, other):
        if isinstance(other, Skill):
            if other.name == self.name:
                self.level + 0
