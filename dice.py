import random
import os.path, urllib
import pygame
import time
_known_images = {}
filename = 'dice1.png'
if 'urlretrieve' not in dir(urllib):
    from urllib.request import urlretrieve as _urlretrieve
else:
    _urlretrieve = urllib.urlretrieve
def _image_from_url(url):
    '''a method for loading images from urls by first saving them locally'''
    filename = os.path.basename(url)
    if not os.path.exists(filename):
        if '://' not in url: url = 'http://'+url
        _urlretrieve(url, filename)
    image, filename =_image_from_file(filename)
    return image, filename

def _image_from_file(filename):
    '''a method for loading images from files'''
    image = pygame.image.load(filename).convert_alpha()
    _known_images[filename] = image
    _known_images[(image.get_width(), image.get_height(), filename)] = image
    return image, filename

def _get_image(thing):
    '''a method for loading images from cache, then file, then url'''
    if thing in _known_images: return _known_images[thing], thing
    sid = '__id__'+str(id(thing))
    if sid in _known_images: return _known_images[sid], sid
    if type(thing) is str:
        if os.path.exists(thing): return _image_from_file(thing)
        return _image_from_url(thing)
    _known_images[sid] = thing
    _known_images[(thing.get_width(), thing.get_height(), sid)] = thing
    return thing, sid

def load_sprite_sheet(url_or_filename, rows, columns):
    '''Loads a sprite sheet. Assumes the sheet has rows-by-columns evenly-spaced images and returns a list of those images.'''
    sheet, key = _get_image(url_or_filename)
    height = sheet.get_height() / rows
    width = sheet.get_width() / columns
    frames = []
    for row in range(rows):
        for col in range(columns):
            clip = pygame.Rect( col*width, row*height, width, height )
            frame = sheet.subsurface(clip)
            frames.append(frame)
    return frames

class Dice(pygame.sprite.Sprite):
    def __init__(self, draw, screen=None) -> None:
        super().__init__()
        self.faces = []
        self.draw = draw

        # Smaller sheet
        # self.sprite_sheet = load_sprite_sheet('dice.png', 2, 3)
        # self.faces = self.sprite_sheet

        # Larger sheet
        self.sprite_sheet = load_sprite_sheet(filename, 4, 4) + load_sprite_sheet('dice2.png',4 , 4)

        for i in range(len(self.sprite_sheet)):
            self.sprite_sheet[i] = pygame.transform.smoothscale(self.sprite_sheet[i], (50,50))
        for face in [15,3,27,19,11,23]:
            self.faces.append(self.sprite_sheet[face])
        self.sprite_sheet = self.sprite_sheet[:24]
        self.image = self.faces[0]
        self.x , self.y = 425, 425
        self.screen = screen
    def roll(self):
        self.rolling_animation()
        x = random.randint(5,6)
        self.image = self.faces[x-1]
        self.draw()
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
        print("You rolled a",x)
        return x
    def rolling_animation(self):
        for i in range(1):
            for image in self.sprite_sheet:
                self.draw()
                self.image = image
                self.screen.blit(self.image, (self.x, self.y))
                pygame.display.flip()
                time.sleep(0.05)
