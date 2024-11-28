import pygame as pg
import time
class Player:
    def __init__(self, color, token_list=[], tokens_out=0, tokens_home=0, sixes=0, your_turn=False, moveable_tokens=[]):
        self.color = color
        self.token_list = token_list
        self.tokens_out = tokens_out
        self.tokens_home = tokens_home
        self.sixes = sixes
        self.your_turn = your_turn
        self.moveable_tokens = moveable_tokens

    def turn(self, dice, bonus=None):
        """_summary_

        Args:
            dice (_type_): _description_
        """
        print("It is now "+self.color+"'s turn")
        self.check_tokens()
        # roll dice
        if not bonus:
            roll = dice.roll()
            time.sleep(0.2)
        else: roll = bonus
        self.can_move(roll)
        self.your_turn = True
        while self.your_turn:
            event = pg.event.wait()
            if event.type == pg.QUIT: pg.quit()
            if self.sixes == 2 and roll == 6: 
                self.go_home()
                self.sixes = 0
                break
            if self.tokens_out < (4 - self.tokens_home) and roll == 5:
                for token in self.token_list:
                    if token.space_occupied == None and token.is_clicked():
                        token.start_token()
                        self.end_turn(dice, roll, token)
                        break
                for token in self.moveable_tokens:
                    if token.space_occupied != None and token.is_clicked() and token.can_move(roll):
                        token.move(roll)
                        self.end_turn(dice, roll, token)
                        break
            elif self.tokens_out == 0 or len(self.moveable_tokens) == 0:
                self.end_turn(dice, roll)
            else:
                for token in self.moveable_tokens:
                    if token.space_occupied != None and token.is_clicked() and token.can_move(roll): # is can_move redundant
                        token.move(roll)
                        self.end_turn(dice, roll, token)
                        break

    def end_turn(self, dice, roll, token=None):
        """_summary_

        Args:
            dice (_type_): _description_
            roll (_type_): _description_
        """
        if token and token.got_capture:
            print("captured")
            token.got_capture = False
            self.turn(dice, bonus=20)
        if self.got_home():
            self.turn(dice, bonus=10)
        if roll == 6:
            self.sixes += 1
            if self.sixes < 3:
                self.turn(dice)
        else:
            self.sixes = 0
        self.your_turn = False
        

    def check_tokens(self):
        """_summary_
        """
        tokens_out = 0 # temp solution
        for token in self.token_list:
            if token.space_occupied != None: tokens_out += 1
        self.tokens_out = tokens_out

    def can_move(self, roll):
        """Updates list of moveable tokens

        Args:
            roll (int): integer representing the roll of the dice on the player's turn
        """
        self.moveable_tokens = []
        for token in self.token_list:
            if token.can_move(roll): self.moveable_tokens.append(token)

    def go_home(self):
        """Determines which token will be sent home in the event that a player rolls a 6 three times in a row. 
        This will be the furthest token that is both outside of the home path and not occupying a safe space. If no tokens meet these conditions, then the player does not lose a token
        """
        furthest_token = None
        for token in self.token_list:
            if not furthest_token and not token.is_safe and not token.in_home_path: 
                furthest_token = token
            if furthest_token and token.spaces_moved > furthest_token.spaces_moved and not token.is_safe and not token.in_home_path:
                furthest_token = token
        if furthest_token:
            furthest_token.reset()

    def got_home(self):
        count = 0
        for token in self.token_list:
            if token.is_home: count += 1
        if count > self.tokens_home:
            self.tokens_home = count
            return True
        return False
            

    

            
