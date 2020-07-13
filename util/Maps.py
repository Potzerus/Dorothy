import json


class Tile:
    tile_dict = {}

    def __init__(self, map, arg):
        self.map = map

    @classmethod
    def generate(cls, map, gen_code: str):
        return cls.tile_dict[gen_code[0:1]](map, gen_code[1:])

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
resources = json.loads(open("Resources.json").read())


class ResourceTile(Tile):

    def __init__(self, map, arg: str):
        super().__init__(map, arg)
        if not arg:
            self.resource = "Er"
            self.amount = 0
        else:
            self.resource = arg[0:2]
            self.amount = int(arg[2:])

    def __repr__(self):
        return "R"

    def export(self):
        output = "R"
        output += self.resource
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
                self.grid[y][x] = Tile.generate(self, self.grid[y][x])
        self.entities = []

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
                output += self.grid[y][x].export() + ","
            output = output[:-1] + "\n"
        return output

    def get_entities(self, x: int, y: int):
        def predicate(entity):
            return entity.x == x and entity.y == y

        return filter(predicate, self.entities)

    def get_tile(self, x, y):
        return self.grid[y][x]

    def get_dimensions(self):
        if not self.grid:
            return 0, 0
        return len(self.grid[0]), len(self.grid)

    def get_cords(self, x: int, y: int, radius):
        cords = []
        max_dims = self.get_dimensions()

        def rec_add(_x, _y, _radius):
            if _radius >= 0:  # and 0 <= _x < max_dims[0] and 0 <= _y < max_dims[1]:
                cord = (_x % max_dims[0], _y % max_dims[1])
                if cord not in cords:
                    cords.append(cord)
                    rec_add(_x + 1, _y, _radius - 1)
                    rec_add(_x - 1, _y, _radius - 1)
                    rec_add(_x, _y + 1, _radius - 1)
                    rec_add(_x, _y - 1, _radius - 1)

        rec_add(x, y, radius)
        return cords

    def get_tiles(self, cords):
        tiles = []
        for x, y in cords:
            tiles.append(self.get_tile(x, y))
        return tiles

    def get_mass_entities(self, cords):
        entities = []
        for x, y in cords:
            entities.extend(self.get_entities(x, y))
        return entities

    def tick(self):
        for entity in self.entities:
            entity.tick()
