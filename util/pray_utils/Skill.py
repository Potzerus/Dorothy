class Skill:

    def __init__(self, char, **info):
        self.char = char
        self.name = info['name']
        self.level = info['level']
        # partial xp for this level
        self.xp = info['xp']
        # polynomial function for generating xp scaling
        self.scaling = info['scaling']

    def __iadd__(self, other):
        if isinstance(other, Skill):
            if other.name == self.name:
                if self.level > other.level:
                    high, low = self, other
                else:
                    high, low = other, self

                high += low.calc_total_xp()
                self.level = high.level
                return self
        if isinstance(other, int):
            self.xp += other
            next_level = self.calc_req_xp_for_lvl(self.level + 1)
            while self.xp > next_level and self.level != 10:
                self.level += 1
                self.xp -= next_level
                next_level = self.calc_req_xp_for_lvl(self.level + 1)
            return self
        raise ValueError("Other is not of type 'Skill' or 'int'")

    def calc_total_xp(self) -> int:
        total_xp = self.xp
        for i in range(self.level):
            total_xp += self.calc_req_xp_for_lvl(i + 1)
        return total_xp

    def calc_req_xp_for_lvl(self, level) -> int:
        req_xp = 0
        for expo, coeff in dict(zip(range(len(self.scaling), self.scaling))).items():
            req_xp += coeff * level ** expo
        return req_xp
