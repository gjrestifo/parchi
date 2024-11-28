import pygame
from pygame.locals import QUIT
from players import Player
from spaces import Space
from tokens import Token
from dice import Dice

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
BOARD_IMAGE_PATH = 'parchi.png'
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
filename = 'spaces.csv'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Parcheesi Game')
clock = pygame.time.Clock()

background_image = pygame.image.load(BOARD_IMAGE_PATH).convert()

colors = ['yellow', 'red', 'green', 'blue']
color_start = [ [700,700], [100,100], [100,700],[700, 100]]
start_spaces = {}
player_list = []
space_list, yellow_home, red_home, green_home, blue_home = {},{},{},{},{}
home_tracks = [yellow_home, red_home, green_home, blue_home]

def start_game(num_players):
    """Generate players and token lists

    Args:
        num_players (int): Number of players, either 2 or 4
    """
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
    """Reads in a .csv file with the coordinates for each space 

    Args:
        filename (str): string containing the file name of the board coordinates
        space_list (dict): dict that contains the number on the board as the keys and the space objects created at each position as values
    """
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
    """Generates the home_tracks for each player in the game by calling the generates 

    Args:
        player_list (list): list containing the active players as created by start_game()
    """
    for i in range(len(home_tracks)):
        filename = colors[i]+".csv"
        generate_board(filename, home_tracks[i])
    for j in range(len(player_list)):
        for token in player_list[j].token_list:
            token.home_track = home_tracks[j]



def generate_start_spaces():
    """Defines start spaces for each player
    """
    l = [5, 39, 56, 22]
    for i in range(len(colors)):
        start_spaces[colors[i]] = space_list[l[i]]

def generate_safe_spaces():
    """Set appropriate spaces to be marked as safe
    """
    safe_spaces = [5,12,17,22,29,34,39,46,51,56,63,68]
    for id in safe_spaces:
        space_list[id].is_safe = True
     

def draw_game_state(exclude=None):
    """ Draw method to be passed into different objects to allow for updating frames in object methods

    Args:
        exclude (_type_, optional): Object not to be redrawn i.e. singular token that moves on a turn. Defaults to None.
    """
    screen.blit(background_image, (0, 0))
    for p in player_list:
        for t in p.token_list:
            if t != exclude:
                screen.blit(t.image, (t.x,t.y))


def test_home_bonus(player_list):
    player_list[0].token_list[0].start_token()
    player_list[0].token_list[1].start_token()
    player_list[0].token_list[0].move(66)
def test_captures(player_list):
    player_list[0].token_list[0].start_token()
    player_list[0].token_list[1].start_token()
    player_list[0].token_list[0].move(39)
    player_list[1].token_list[0].start_token()
    player_list[1].token_list[1].start_token()
    player_list[1].token_list[1].move(7)

def test_walls(player_list):
    player_list[0].token_list[0].start_token()
    player_list[0].token_list[1].start_token()
    player_list[0].token_list[0].move(5)
    player_list[0].token_list[1].move(5)
    player_list[1].token_list[0].start_token()
    player_list[1].token_list[1].start_token()
    player_list[1].token_list[0].move(5)
    player_list[1].token_list[1].move(5)

        
d = Dice(draw_game_state, screen)

_timeron = False
_timerfps = 0
def game_loop(callback, fps):
    global _timeron, _timerfps
    keys = set([])
    if fps > 1000: fps = 1000
    _timerfps = fps
    _timeron = True
    pygame.time.set_timer(pygame.USEREVENT, int(1000/fps))
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: break
        if event.type == pygame.KEYDOWN:
            keys.add(event.key)
        if event.type == pygame.KEYUP and event.key in keys:
            keys.remove(event.key)
        if event.type == pygame.USEREVENT:
            pygame.event.clear(pygame.USEREVENT)
            callback(keys)
    pygame.time.set_timer(pygame.USEREVENT, 0)
    _timeron = False



game_on = False
draw_game_state()
def main(keys):
    global game_on
    if pygame.K_SPACE in keys:
        game_on = True
    while game_on:
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
                # if pygame.K_1 in keys:
                player_list[i].turn(d)
                player_list[i].your_turn = False
                player_list[(i+1) % len(player_list)].your_turn = True

    # if event.type == pygame.KEYDOWN:
    #     pygame.event.clear(pygame.KEYDOWN)
    #     p1.turn(d)

    # Update display
    pygame.display.flip()
    clock.tick(FPS)


# main()
running = True
generate_board(filename, space_list)
generate_start_spaces()
generate_safe_spaces()
start_game(2)
generate_home_tracks(player_list)
# test_home_bonus(player_list)
# test_captures(player_list)
test_walls(player_list)
player_list[0].your_turn = True
# space_list[13].has_wall = True
game_loop(main, 60)

# while running:
#     event = pygame.event.wait()
#     if event.type == pygame.QUIT: break
#     if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: break
#     # if event.type == pygame.QUIT:
#     #     running = False
#     for player in player_list:
#                 for token in player.token_list:
#                         if token.is_clicked():
#                             print(token,id(token),"was clicked!")
#     # Draw board and tokens
#     draw_game_state()
#     screen.blit(d.image, (d.x, d.y))
#     # draw_board(screen)
#     # draw_tokens(screen, tokens)
    
#     p1 = player_list[0]
#     # p1.token_list[0].start_token(space_list[1])
#     for i in range(len(player_list)):
#         if player_list[i].your_turn:
#             player_list[i].turn(d)
#             player_list[i].your_turn = False
#             player_list[(i+1) % len(player_list)].your_turn = True

#     # if event.type == pygame.KEYDOWN:
#     #     pygame.event.clear(pygame.KEYDOWN)
#     #     p1.turn(d)

#     # Update display
#     pygame.display.flip()
#     clock.tick(FPS)

pygame.quit()

