import pygame as pg
import time
class Token(pg.sprite.Sprite):
    def __init__(self, color, x=0, y=0, start_space=None, spaces_moved=0, space_occupied=None, is_safe=False, is_home=False, screen=None, home_track={}, draw=None) -> None:
        """Creates a token object

        Args:
            color (str): _description_
            spaces_moved (int): _description_
            space_occupied (Space): _description_
            is_safe (bool): _description_
            home (bool): _description_
            id (str): _description_
        """
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.xi, self.yi = x, y
        self.image = pg.image.load(color+".png").convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (40,40))
        # self.id = id Implement later
        self.start_space = start_space
        self.spaces_moved = 0
        self.space_occupied = None  # Could also be 0 if using index
        self.is_safe = False
        self.is_home = False
        self.in_home_path = False
        self.screen=screen
        self.home_track = home_track
        self.draw = draw
        self.got_capture = False


    def can_move(self, roll):
        """Checks if a token can make a valid move
        Two cases where moves are not possible:
        1. If the token would move beyond the final home space (i.e. moves more than exactly 72 spaces total)
        2. In making the move, the token would come against a wall

        Args:
            roll (int): the value of the dice roll

        Returns:
            bool: _description_
        """
        if self.space_occupied == None: return False
        if self.spaces_moved + roll > 72:
            return False
        space = self.space_occupied
        for i in range(roll):
            space = space.next
            if space.has_wall:
                return False
        return True

    def start_token(self):
        """_summary_

        Args:
            start_space (Space): _description_
        """
        self.spaces_moved = 1
        self.space_occupied = self.start_space
        self.space_occupied.tokens.append(self)
        self.x, self.y = self.space_occupied.x, self.space_occupied.y
        self.is_safe = True
    
    def move(self, steps):
        """_summary_

        Args:
            steps (_type_): _description_
        """
        # self.spaces_moved += steps
        self.space_occupied.tokens.remove(self)
        for i in range(steps):
            self.draw(self)
            self.update_position(1)
            self.screen.blit(self.image, (self.x, self.y))
            pg.display.flip()
            time.sleep(.2)
        self.space_occupied.tokens.append(self)
        self.check_capture()
        self.check_safe()
        self.check_home()

    def update_position(self, steps):
        """_summary_

        Args:
            steps (_type_): _description_
        """
        self.spaces_moved += steps
        print(self.color)
        print("Spaces moved:",self.spaces_moved)
        if self.spaces_moved == 0:
            # Token is at the starting area
            self.space_occupied = None
        elif self.spaces_moved <= 64:
            # Token is on the main track
            for i in range(steps):
                self.space_occupied = self.space_occupied.next
                # TODO: Check walls each step
                self.x = self.space_occupied.x
                self.y = self.space_occupied.y
        elif self.spaces_moved <= 72:  # Spaces 64 to 72 are the home path
            # Token is on the home path specific to its color
            self.space_occupied = self.home_track[self.spaces_moved]
            print("Home Track:", self.color, self.home_track[self.spaces_moved].x, self.home_track[self.spaces_moved].y)
            self.x = self.space_occupied.x
            self.y = self.space_occupied.y
            if self.spaces_moved == 72:
                # Token has reached home
                print("You reached home!")
                self.space_occupied = "home"
                # TODO: Find better way of representing home space for line 131 in tokens.py
                self.is_home = True

    def is_clicked(self):
        if any(pg.mouse.get_pressed()):
            # Get mouse position
            x, y = pg.mouse.get_pos()
            dx = abs(self.x - x)
            dy = abs(self.y - y)
            pg.event.clear()

            return max(dx,dy) < 35
        
    def check_safe(self):
        """Checks to see if a token occupys a safe space and updates the is_safe attribute.
        """
        # safe_spaces = [5,12,17,22,29,34,39,46,51,56,63,68]
        if self.is_home or self.space_occupied.is_safe:
            self.is_safe = True
        else:
            self.is_safe = False

    def check_home(self):
        """ Checks to see if the token has made it into the home path
        """
        # Update home status if the token has reached the final destination
        if self.spaces_moved >= 64:
            self.in_home_path = True

    def reset(self):
        """Resets a token to its original position. This function is called in the event that a token is captured or a player rolls three sixes in a row.
        """
        # Reset token's attributes to initial state
        self.spaces_moved = 0
        self.space_occupied = None
        self.is_safe = False
        self.in_home_path = False
        self.x, self.y = self.xi, self.yi

    def check_capture(self):
            # Determine if this token can capture another token
            if len(self.space_occupied.tokens) == 2:
                other_token = self.space_occupied.tokens[0]
                if not other_token.is_safe and self.color != other_token.color:
                    self.space_occupied.tokens.remove(other_token)
                    other_token.reset()
                    self.got_capture = True
                else:
                    self.space_occupied.build_wall()

            # if (self.space_occupied == other_token.space_occupied and 
            #         not self.is_safe and not other_token.is_safe)