import argparse
import datetime
import logging
import operator
import os
import pygame
import random
import re

# Constants
MIN_WND_SIZE = 200 # Minimum for window height or width.
MIN_TILE_SIZE = 10 # Minimum for tile size.
MIN_NB_ROWS = 12
MIN_NB_COLS = 20
FPS = 10
WIDTH = 800
HEIGHT = 600
BLACK = '#000000'
WHITE = '#ffffff'
STEPS = 20
INPUT_FILE = os.path.join(os.environ['HOME'], 'my_input_file.txt')
OUPUT_FILE = os.path.join(os.environ['HOME'], 'my_output_file.txt')
TILE_SIZE = 20
DEAD = 0 # One of the the cell state
LIVING = 1 # The other cell state

def read_args():
    """Read command line arguments."""

    # Define parser
    parser = argparse.ArgumentParser(
            description='An implementation of Game of Life.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', help='To set the path to the initial pattern file.',
            default=INPUT_FILE)
    parser.add_argument('-o', help='To set the path to the output file.',
            default=OUPUT_FILE)
    parser.add_argument('-m', help='To set the number of steps to run, when display is off.', type=int,
            default=STEPS)
    parser.add_argument('-d',
            help=' When enabled, pygame is enabled and we display each step of the simulation.', action='store_true')
    parser.add_argument('-f', help='The number of frames per second to use with pygame.', type=int, default=FPS)
    parser.add_argument('--width', help='The initial width of the pygame screen.', type = int,
            default=WIDTH)
    parser.add_argument('--height', help='The initial height of the pygame screen.', type =int, default = HEIGHT)
    parser.add_argument('--tile-size', help='Tile size', type=int, default=TILE_SIZE)
    # Parse arguments
    args = parser.parse_args()

    # Enable debug messages
    if args.debug:
        logger.setLevel(logging.DEBUG)

    return args

# Game over exception
class GameOver(Exception):
    pass

class Board:

    def __init__(self, width, height, tile_size):
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._objects = []
        self._removed_objects = []

        # Check arguments
        if self._height < MIN_WND_SIZE or self._width < MIN_WND_SIZE:
            raise ValueError(("Window height and width must be greater or " +
                "equal to %d.") % MIN_WND_SIZE)
        if self._tile_size < MIN_TILE_SIZE:
            raise ValueError("Tile size must be greater or equal to %d."
                    % MIN_TILE_SIZE)
        if (self._height % self._tile_size != 0 or
                self._width % self._tile_size != 0):
            raise ValueError(("Window width (%d) and window height (%d) must" +
                " be dividable by the tile size (%d).") % (self._width,
                    self._height, self._tile_size))
        if self._width // self._tile_size < MIN_NB_COLS:
            raise ValueError(("Number of columns must be greater or equal to" + 
                " %d, but width / tile_size = %d / %d = %d.") % (MIN_NB_COLS,
                    self._width, self._tile_size,
                    self._width // self._tile_size))
        if self._height // self._tile_size < MIN_NB_ROWS:
            raise ValueError(("Number of rows must be greater or equal to" + 
                " %d, but height / tile_size = %d / %d = %d.") % (MIN_NB_ROWS,
                    self._height, self._tile_size,
                    self._height // self._tile_size))

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getNbCols(self):
        return self._width // self._tile_size

    def getNbRows(self):
        return self._height // self._tile_size
    
    def drawTiles(self, screen, tiles):
        
        # Loop on all tiles
        for tile in tiles:

            # Is tile inside board?
            if (tile.getCol() >= 0 and tile.getCol() < self.getNbCols()
                    and tile.getRow() >= 0
                    and tile.getRow() < self.getNbRows()):

                # Compute rectangle
                tile_rect = pygame.Rect(tile.getCol() * self._tile_size,
                        tile.getRow() * self._tile_size,
                        self._tile_size, self._tile_size)
                
                # Draw tile
                pygame.draw.rect(screen, tile.getColor(), tile_rect)
class Tile:
    
    def __init__(self, col, row, color=None):
        self._row = row
        self._col = col
        self._color = None if color is None else pygame.Color(color)

    def getCol(self):
        return self._col

    def getRow(self):
        return self._row

    def setCol(self, col):
        self._col = col

    def setRow(self, row):
        self._row = row

    def getColor(self):
        return self._color
    
class Factory:

    def __init__(self,board):
        self._board = board

    def declareCell(self,)

    def createSetOfCells(self,): #TODO create the cell from the input file
        pass

class GameObject:

    def __init__(self, board, tiles=None):
        self._board = board
        self._tiles = None if tiles is None else tiles.copy()

    def getTiles(self):
        return self._tiles.copy()

    def draw(self, screen):
        if self._tiles is not None:
            self._board.drawTiles(screen, self._tiles)  

class BackgroundObject(GameObject):
    pass

class CheckerBackground(BackgroundObject):

    def __init__(self, board, color_background=WHITE):
    
        # Create tiles
        tiles = []
        # Loop on all rows and columns
        for i in range(board.getNbCols()):
            for j in range(board.getNbRows()):
                
                # New tile
                tiles.append(Tile(col=i, row=j, color=color_background))

        # Call super class
        super().__init__(board, tiles)
    
class Cell :

    def __init__(self,board, state,tile):
        super().__init__(board, [tile]) #useful ?
        self._state = state
        """self._x = place [0]
        self._y = place [1]"""

    def getState(self):
        return(self._state)
    
    def getPlace(self):
        return(self._x,self._y)
    
class Set_of_Cells :
    
    def __init__(self,listCells,file) :
        self._listCells = listCells
        self._file = file
    
    def load(self):
        
        # Test if file exists
        if os.path.exists(self._file):

            # Open file for reading
            with open(self._file, 'r') as f:
                i = 0 #number of line
                # Loop on all lines
                for line in f:
                    line = line.rstrip() # Get rid of new line character
                    for row, state in enumerate(line):
                        if state == '1':
                            self._listCells.append(Cell 1 (line,row)) # Add to list
                        if state == '0':
                            self._listCells.append(Cell 0 (line,row)) # Add to list
                i = i + 1

    def save(self):
        
        # Open file for writing
        with open(self._file, 'w') as f:

            # Loop on all scores
            for cell in self._listCells:
                print(getState(cell), file=f)
    #TODO : functions to save and load state ?
        
class Game :

    def __init__(self,width=WIDTH,height=HEIGHT,fps=FPS):
        self._fps = fps
        # Initialize the Pygame library.
        # This is a special step needed by Pygame. Most (99%) libraries do not
        # need an initialization step.
        logger.debug("Initialize Pygame.")
        pygame.init()
        
        # Create a screen for display, choosing its size (width x height).
        logger.debug("Create Pygame screen.")
        self._screen = pygame.display.set_mode((width, height))

        # Create a clock object that we will use to control the speed of our
        # game.
        logger.debug("Create Pygame clock.")
        self._clock = pygame.time.Clock()

        # Create the board
        logger.debug("Create Board instance.")
        self._board = Board(width=width, height=height, tile_size=tile_size) #TODO create Board 
        
        # Create the checkerboard background
        logger.debug("Create background instance.")
        self._board.addObject(CheckerBackground(self._board, color_1=bg_color_1,
                color_2=bg_color_2))
        
    def _process_events(self):
        """Process new events (keyboard, mouse)."""

        for event in pygame.event.get():
            
            # Catch selection of exit icon (Window "cross" icon)
            if event.type == pygame.QUIT:
                raise GameOver()

            # Catch a key press
            elif event.type == pygame.KEYDOWN:
                
                # "Q" key has been pressed
                if event.key == pygame.K_q:
                    raise GameOver()
    
    def _update_display(self):
        
        # Draw all objects
        self._board.drawObjects(self._screen)

        # Display the display
        pygame.display.update()    

    def start(self):

        # Loop forever
        logger.debug("Start main loop.")
        try:
            while True:
                
                # Wait 1/FPS of a second, starting from last display or now
                self._clock.tick(self._fps)
                
                self._process_events()
                self._update_objects()
                self._update_display()

        except GameOver:
            pass

        logger.info("\nGame over.")

        # Terminate Pygame
        pygame.quit()
        self._process_score()


def main():

    logger.debug("Start main function.")
    # Read command line arguments
    args = read_args()

    # Create the game instance
    logger.debug("Create Game instance.")
    game = Game(**vars(args)) # vars() transforms mapping (args) into
                              # a dictionary

    # Run the game instance
    logger.debug("Start Game instance.")
    game.start()

# Create a logger for this module
logger = logging.getLogger(__name__)
        
if __name__ == "__main__":

    import sys

    # Setup the logger
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Call main function
    main()

    # Quit program properly
    quit(0)
