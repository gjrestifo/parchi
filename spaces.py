class Space:
    def __init__(self, id, x, y, next=None, isSafe=False, has_wall=False) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.next = next
        self.isSafe = isSafe
        self.has_wall = has_wall