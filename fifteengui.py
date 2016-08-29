"""
GUI for the Fifteen puzzle
"""

import os, sys, random
import pygame
from pygame.locals import *

#initialize pygame
pygame.init()

#image and screen constants
TILE_SIZE = 100
BORDER_SIZE = 50

def load_image(name, colorkey=None, alpha=False):
    """
    image load function, exits if resources fail to load
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class FifteenGUI:
    """
    Main GUI class
    """

    def __init__(self, puzzle):
        """
        Create screen 
        """
        self._puzzle = puzzle
        self._puzzle_height = puzzle.get_height()
        self._puzzle_width = puzzle.get_width()
        self._width = self._puzzle_width * TILE_SIZE + BORDER_SIZE * 2
        self._height = self._puzzle_height * TILE_SIZE + BORDER_SIZE * 2
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._screen_rect = self._screen.get_rect()
        pygame.display.set_caption('Fifteen')
        self._background, dummy_rect = load_image('bg.png', alpha=True)
        self._loadscreen, dummy_rect = load_image('loadscreen.png', True)
        self._tiles_sprite, dummy_rect = load_image('fifteen.png', alpha=True)
        self._tiles = []
        self.make_tiles()
        self._possible_moves = 'udlr'
        self._solution = ""
        self._jumblestr = ""
        self._current_moves = ""
        self._just_loaded = True
        self.main()

    def make_tiles(self):
        """
        create list tiles by making subsurface for each tile
        in tiles sprite sheet
        """
        num_tiles = self._puzzle_height * self._puzzle_width
        #subsurface is a ract(left, top, width, height
        
        for idx in xrange(num_tiles):
            self._tiles.append(self._tiles_sprite.subsurface(
                (idx * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)))

    def solve(self):
        """
        Event handler to generate solution string for given configuration
        """
        new_puzzle = self._puzzle.clone()
        self._solution = new_puzzle.solve_puzzle()

    def jumble(self):
        """
        jumble puzzle tiles
        """
        jumble_str = ""

        for idx in xrange(100):
            jumble_str += random.choice(self._possible_moves)

        self._jumblestr = jumble_str
    
    def print_moves(self):
        """
        Event handler to print and reset current move string
        """
        print self._current_moves
        self._current_moves = ""

    def enter_moves(self, txt):
        """
        Event handler to enter move string
        """
        self._solution = txt

    def keydown(self, event):
        """
        Keydown handler that allows updates of puzzle using arrow keys
        """
        key = event.key
        if key == K_ESCAPE:
            sys.exit()
        if key == K_UP:
            try:
                self._puzzle.update_puzzle("u")
                self._current_moves += "u"
            except:
                print "invalid move: up"
        elif key == K_DOWN:
            try:
                self._puzzle.update_puzzle("d")
                self._current_moves += "d"
            except:
                print "invalid move: down"
        elif key == K_LEFT:
            try:
                self._puzzle.update_puzzle("l")
                self._current_moves += "l"
            except:
                print "invalid move: left"
        elif key == K_RIGHT:
            try:
                self._puzzle.update_puzzle("r")
                self._current_moves += "r"
            except:
                print "invalid move: right"
        elif key == K_s:
            self.solve()

        elif key == K_j:
            self.jumble()

        if self._just_loaded:
            if key == K_RETURN:
                self._just_loaded = False
                

    def update(self):
        """
        Blit current puzzle state
        """
        for row in range(self._puzzle_height):
            for col in range(self._puzzle_width):
                tile_num = self._puzzle.get_number(row, col)
                self._screen.blit(self._tiles[tile_num],
                                 (col * TILE_SIZE + BORDER_SIZE,
                                  row * TILE_SIZE + BORDER_SIZE))
                                  
            
    def main(self):
        """
        main game loop
        """

        clock = pygame.time.Clock()
        while 1:
            clock.tick(30)
            self._screen.blit(self._background, self._screen_rect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.keydown(event)
            #redraw game in new tile positions
            self.update()

            #draw load screen if game just loaded
            if self._just_loaded:
                self._screen.blit(self._loadscreen, (BORDER_SIZE, BORDER_SIZE))

            #draw through solution if s key pressed    
            while self._solution:
                self._puzzle.update_puzzle(self._solution[0])
                self._solution = self._solution[1:]
                self.update()
                pygame.display.flip()
                pygame.time.wait(250)

            #jumble puzzle if j key pressed    
            while self._jumblestr:
                try:
                    self._puzzle.update_puzzle(self._jumblestr[0])
                except AssertionError:
                    #jumble is random and returns some off grid moves
                    #ignore move remove from string
                    self._jumblestr = self._jumblestr[1:]
                    break
                self._jumblestr = self._jumblestr[1:]
                self.update()
                pygame.display.flip()
                pygame.time.wait(125)
            pygame.display.flip()
