class Space:
    def __init__(self, id, x, y, next=None, is_safe=False, has_wall=False) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.next = next
        self.is_safe = is_safe
        self.has_wall = has_wall
        self.tokens = []


    def build_wall(self):
        #TODO: move token 2, has_wall
        self.has_wall = True
        if self.id in range(52,60) or self.id in range(9,17):
            self.tokens[1].y += 50
        elif self.id in range(43,51) or self.id in range(18,26):
            self.tokens[1].y -= 50
        elif self.id in range(1,9) or self.id in range(26,34):
            self.tokens[1].x += 50
        else:
            self.tokens[1].x -= 50