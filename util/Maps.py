from util.Resources import resources


class Tile:
    tile_dict = {}

    def __init__(self, arg):
        pass

    @classmethod
    def generate(cls, gen_code: str):
        return cls.tile_dict[gen_code[0:1]](gen_code[1:])

    def __repr__(self):
        return "X"

    def export(self):
        return self.__repr__()

    def tick(self):
        pass


class NeutralTile(Tile):

    def __repr__(self):
        return "O"

    def export(self):
        return ""


Tile.tile_dict['O'] = NeutralTile
Tile.tile_dict[''] = NeutralTile


class ErrorTile(Tile):
    pass


Tile.tile_dict['X'] = ErrorTile


class ResourceTile(Tile):

    def __init__(self, arg: str):
        if not arg:
            self.resource = "Error"
            self.amount = 0
        else:
            self.resource = resources[arg[0:2]]
            self.amount = int(arg[2:])

    def __repr__(self):
        return "R"

    def export(self):
        output = "R"
        output += list(resources.keys())[list(resources.values()).index(self.resource)]
        output += str(self.amount)
        return output


Tile.tile_dict['R'] = ResourceTile


class Map:
    def __init__(self, raw_map: str):
        temp_map = raw_map.split("\n")
        self.grid = []
        for y in temp_map:
            self.grid.append(y.split(","))

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x] = Tile.generate(self.grid[y][x])

    def __repr__(self):
        output = ""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                output += str(self.grid[y][x]) + " "
            output += "\n"
        return output

    def export(self):
        output = ""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                output += self.grid[y][x].export() + " "
            output += "\n"
        return output
