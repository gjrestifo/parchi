import pygame as pg
class Player:
    def __init__(self, color, token_list=[], tokens_out=0, tokens_home=0, sixes=0, your_turn=False, moveable_tokens=[]):
        self.color = color
        self.token_list = token_list
        self.tokens_out = tokens_out
        self.tokens_home = tokens_home
        self.sixes = sixes
        self.your_turn = your_turn
        self.moveable_tokens = moveable_tokens

    def turn(self, dice):
        self.check_tokens()
        # roll dice
        roll = dice.roll()
        self.can_move(roll)
        self.your_turn = True
        while self.your_turn:
            event = pg.event.wait()
            if event.type == pg.QUIT: break
            if self.sixes == 2 and roll == 6: 
                print("GO HOME!") # Reset token
                break
            if self.tokens_out < (4 - self.tokens_home) and roll == 5:
                # pg.event.wait()
                for token in self.token_list:
                    if token.space_occupied == None and token.is_clicked():
                        token.start_token()
                        self.end_turn(dice, roll)
                        break
                for token in self.moveable_tokens:
                    if token.space_occupied != None and token.is_clicked() and token.can_move(roll):
                        token.move(roll)
                        self.end_turn(dice, roll)
                        break
            elif self.tokens_out == 0 or len(self.moveable_tokens) == 0:
                self.end_turn(dice, roll)
            #TODO: Fix 6 rolls
            # elif roll == 6:
            #     if self.sixes < 3:
            #         for token in self.moveable_tokens:
            #             if token.is_clicked():
            #                 token.move(roll)
            #                 self.turn(dice)
            #                 break
            #     else:
            #         print("GO HOME") # reset a token
            #         self.end_turn()
            else:
                for token in self.moveable_tokens:
                    if token.space_occupied != None and token.is_clicked() and token.can_move(roll):
                        token.move(roll)
                        self.end_turn(dice, roll)
                        break

    def end_turn(self, dice, roll):
        if roll == 6:
            self.sixes += 1
            if self.sixes < 3:
                self.turn(dice)
        else:
            self.sixes = 0
        self.your_turn = False

    def check_tokens(self):
        tokens_out = 0 # temp solution
        for token in self.token_list:
            if token.space_occupied != None: tokens_out += 1
        self.tokens_out = tokens_out

    def can_move(self, roll):
        self.moveable_tokens = []
        for token in self.token_list:
            if token.can_move(roll): self.moveable_tokens.append(token)
            
            
