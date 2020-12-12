def move(entity, x_cord: int, y_cord: int):
    def predicate():
        entity.x += x_cord
        entity.y += y_cord

    return predicate


instructions = {
    "move": move,

}
