import pygame as pg
from pygame.locals import QUIT
import gamebox
from players import Player
from spaces import Space
from tokens import Token
from dice import Dice

pg.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
BOARD_IMAGE_PATH = 'parchi.png'
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
filename = 'spaces.csv'

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Parcheesi Game')
clock = pg.time.Clock()

background_image = pg.image.load(BOARD_IMAGE_PATH).convert()

colors = ['yellow', 'red', 'green', 'blue']
color_start = [ [700,700], [100,100], [100,700],[700, 100]]
start_spaces = {}
player_list = []
space_list, yellow_home, red_home, green_home, blue_home = {},{},{},{},{}
home_tracks = [yellow_home, red_home, green_home, blue_home]

def start_game(num_players):
    for i in range(num_players):
        t = []
        for j in range(4):
            x, y = color_start[i]
            t.append(Token(colors[i], x, y, start_space=start_spaces[colors[i]],screen=screen, draw=draw_game_state))
            if j == 0:
                color_start[i][0] += 80
            elif j == 1:
                color_start[i][1] += 80
            else:
                color_start[i][0] -= 80

        player_list.append(Player(colors[i], t))

def generate_board(filename, space_list):
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            c = line.strip().split(',')
            space_list[int(c[0])] = Space(int(c[0]), float(c[1]), float(c[2]))
    first_id = None
    for space in space_list.values():
        if first_id == None:
            first_id = space.id
        try:
            space.next = space_list[space.id + 1]
        except:
            space.next = space_list[first_id]




def generate_home_tracks(player_list):
    for i in range(len(home_tracks)):
        filename = colors[i]+".csv"
        generate_board(filename, home_tracks[i])
    for j in range(len(player_list)):
        for token in player_list[j].token_list:
            token.home_track = home_tracks[j]



def generate_start_spaces():
    l = [5, 39, 56, 22]
    for i in range(len(colors)):
        start_spaces[colors[i]] = space_list[l[i]]
     

def draw_game_state(exclude=None):
    screen.blit(background_image, (0, 0))
    for p in player_list:
        for t in p.token_list:
            if t != exclude:
                screen.blit(t.image, (t.x,t.y))
        
d = Dice(draw_game_state, screen)






# def main():
#     num_players = int(input("Would you like to play with two players or four players? "))
#     start_game(num_players)
    

#     winstyle = 0  # |FULLSCREEN
#     bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
#     screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

# main()
running = True
generate_board(filename, space_list)
generate_start_spaces()
start_game(2)
generate_home_tracks(player_list)
player_list[0].your_turn = True
# space_list[13].has_wall = True

while running:
    event = pg.event.wait()
    if event.type == pg.QUIT:
        running = False
    for player in player_list:
                for token in player.token_list:
                        if token.is_clicked():
                            print(token,id(token),"was clicked!")
    # Draw board and tokens
    draw_game_state()
    screen.blit(d.image, (d.x, d.y))
    # draw_board(screen)
    # draw_tokens(screen, tokens)
    
    p1 = player_list[0]
    # p1.token_list[0].start_token(space_list[1])
    for i in range(len(player_list)):
        if player_list[i].your_turn:
            player_list[i].turn(d)
            player_list[i].your_turn = False
            player_list[(i+1) % len(player_list)].your_turn = True

    # if event.type == pg.KEYDOWN:
    #     pg.event.clear(pg.KEYDOWN)
    #     p1.turn(d)

    # Update display
    pg.display.flip()
    clock.tick(FPS)

pg.quit()

