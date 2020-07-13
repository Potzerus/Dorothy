from util.Entities import Entity

class DronePart:



class Drone(Entity):
    def __init__(self, name, x, y, parts):
        super().__init__(name, x, y)
        for name in parts:
