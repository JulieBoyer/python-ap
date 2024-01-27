import argparse
import logging
import os
import pygame

# Constants
MIN_WND_SIZE = 200 # Minimum for window height or width.
MIN_TILE_SIZE = 10 # Minimum for tile size.
MIN_NB_ROWS = 12
MIN_NB_COLS = 20
FPS = 5
WIDTH = 50
HEIGHT = 50
BLACK = '#000000'
WHITE = '#ffffff'
STEPS = 20
INPUT_FILE = os.path.join(os.environ['HOME'], 'my_input_file.txt')
OUPUT_FILE = os.path.join(os.environ['HOME'], 'my_output_file.txt')
TILE_SIZE = 20
DEAD = 0 # One of the the cell state
LIVING = 1 # The other cell state

def read_args():
    # Define parser
    parser = argparse.ArgumentParser(
            description='An implementation of Game of Life.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # Define all the arguments
    parser.add_argument('-i', help='To set the path to the initial pattern file.', default=INPUT_FILE)
    parser.add_argument('-o', help='To set the path to the output file.', default=OUPUT_FILE)
    parser.add_argument('-m', help='To set the number of steps to run, when display is off.', type=int, default=STEPS)
    parser.add_argument('-d', help=' When enabled, pygame is enabled and we display each step of the simulation.', action='store_true')
    parser.add_argument('-f', help='The number of frames per second to use with pygame.', type=int, default=FPS)
    parser.add_argument('--width', help='The initial width of the pygame screen.', type = int, default=WIDTH)
    parser.add_argument('--height', help='The initial height of the pygame screen.', type =int, default = HEIGHT)
    parser.add_argument('--tile-size', help='Tile size', type=int, default=TILE_SIZE)
    parser.add_argument('-g', '--debug', help='Set debug mode.', action='store_true')
    
    # Parse arguments
    args = parser.parse_args()

    # Enable debug
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Input file : " + args.i)
        logger.debug("Output file : " + args.o)
        logger.debug("Number of step (disp off) : " + str(args.m))
        logger.debug("Display : " + str(args.d))
        logger.debug("Frame rate : " + str(args.f))
        logger.debug("Width : " + str(args.width))
        logger.debug("Height : " + str(args.height))
        logger.debug("Tiel size : " + str(args.tile_size))
    return args

class Cell:
    # Class definition for a cell
    def __init__(self, row, col, alive=False):
        self._row = row
        self._col = col
        self._alive = alive
    
    # Functions to have access to internal data without being able to change it 
    def getRow(self):
        return self._row
    
    def getCol(self):
        return self._col
    
    def isAlive(self):
        return self._alive

class SetOfCells:
    # Class definition for a set of cells
    def __init__(self, width, height, inputFile, outputFile):

        # Size of the simulation
        self._width = width
        self._height = height

        # Sets of cells
        self._cells = [[None for i in range(self._width)]for j in range(self._height)]
        self._former_cells = self._cells

        # Files path
        self._inputFile = inputFile
        self._outputFile = outputFile
        
    def get_set(self):
        return self._cells
   
    def add_cell(self,cell,x,y):
        self._cells[x][y] = cell
    
    def clear_cells(self):
        self._cells = [[None for i in range(self._width)]for j in range(self._height)]
    
    def is_anyone_alive(self):
        return any(any(cell.isAlive() for cell in cell_line) for cell_line in self._cells)
    
    def get_cell_values(self):
        return [[cell.isAlive() for cell in cell_line] for cell_line in self._cells]

    def load_cells(self):
        # Clear previous cells
        self.clear_cells()

        # Test if file exists
        if os.path.exists(self._inputFile):
            # Open file for reading
            with open(self._inputFile, 'r') as file:
                for row, line in enumerate(file):
                    for col, char in enumerate(line.strip()):
                        if char == '1':
                            self.add_cell(Cell(row, col, alive=True),row,col)
                        if char == '0':
                            self.add_cell(Cell(row, col, alive=False),row,col)

        # Complete the set if the text file is not full
        for i in range(self._height):
            for j in range(self._width):
                if self._cells[i][j] == None:
                    self.add_cell(Cell(i, j, alive=False),i,j)

    def save_cells(self):
        # Open file for writing
        with open(self._outputFile, 'w') as file:
            for cell_line in self._cells:
                line = ""
                for cell in cell_line:
                    line += str(1 if cell.isAlive() else 0)
                print(line,file=file)
    
    def update_cells(self):
        # Save the former state
        self._former_cells = self._cells
        self.clear_cells()

        # Compute the calculation for each cell
        for cell_line in self._former_cells:
            for cell in cell_line:
                num_neighbors = self.count_neighbors(cell)
                if not(cell.isAlive()):
                    if (num_neighbors == 3):
                # Dead with 3 neighbors -> Alive
                        self.add_cell(Cell(cell.getRow(), cell.getCol(), alive=True),cell.getRow(),cell.getCol())
                    else:
                # Dead any other case -> Dead
                        self.add_cell(Cell(cell.getRow(), cell.getCol(), alive=False),cell.getRow(),cell.getCol())
                elif (num_neighbors < 2) or (num_neighbors > 3):
                # Alive and wrong neighbors num -> Dead
                    self.add_cell(Cell(cell.getRow(), cell.getCol(), alive=False),cell.getRow(),cell.getCol())
                else:
                # Alive with good neighbors num -> Alive
                    self.add_cell(Cell(cell.getRow(), cell.getCol(), alive=True),cell.getRow(),cell.getCol())

    def count_neighbors(self,cell):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):

                # Avoid the cell itself
                if i == 0 and j == 0:
                    continue
                
                # Tor surface index
                neighbor_row = (cell.getRow()+ i + self._height) % self._height
                neighbor_col = (cell.getCol() + j + self._width) % self._width

                # Check if neighbor is alive
                if self._former_cells[neighbor_row][neighbor_col].isAlive():
                    count += 1
                    
        return count

class game_of_life():
    def __init__(self, width, height, initial_cells, output_file, display, nb_gen, screen):
        # Size of the simulation
        self._width = width
        self._height = height
        
        # Files to consider
        self._output_file = output_file
        self._input_file = initial_cells

        # Display
        self._display = display
        self._screen = screen

        # Simulation init
        self._nb_gen = nb_gen
        self._gen = 0
        self._set_of_cells = SetOfCells(width, height, initial_cells, output_file)

        # Read the set of cells from the file
        self.read_initial_cells()
        
    def read_initial_cells(self):
        self._set_of_cells.load_cells()

    def save_final_cells(self):
        self._set_of_cells.save_cells()

    def update_cells(self):
        self._set_of_cells.update_cells()
    
    def is_anyone_alive(self):
        return self._set_of_cells.is_anyone_alive()
    
    def update_display(self):
        self._screen.update(self._set_of_cells.get_cell_values())

    def start(self):
        while (self._gen < self._nb_gen) or (self._display):

            # Update the state of cells
            self.update_cells()
            self._gen +=1
            
            # Display handling if necessary
            if self._display:
                # Watch out to pygame close event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_final_cells()
                        pygame.quit()
                        quit(0)
                self.update_display()

            # Check for the end of the game
            if not self.is_anyone_alive():
                logger.info("No live cells remaining. Exiting the simulation.")
                self.save_final_cells()
                # Close only if no display
                if not(self._display):
                    quit(0)
            
            # Write the last state
            self.save_final_cells()

class PYGAME_DISPLAY():
    def __init__(self,width, height, fps, tile_size):

        # Grid size
        self._width = width
        self._height = height

        # Frame per sec
        self._fps = fps

        # Screen settings
        self._tile_size = tile_size
        self._screen = pygame.display.set_mode((width*self._tile_size, height*self._tile_size))

    def update(self,cell_values):

        # For each cell
        for i in range(self._height):
            for j in range(self._width):
                # Draw a square 
                cell_rect = pygame.Rect(j * self._tile_size, i * self._tile_size, self._tile_size, self._tile_size)
                pygame.draw.rect(self._screen, pygame.Color(WHITE) if cell_values[i][j] else pygame.Color(BLACK), cell_rect)

        # Reverse the screen
        pygame.display.flip()

        # Wait for the next tick
        pygame.time.delay(int(1/self._fps*1000))

def main():
    # Read command line arguments
    args = read_args()

    logger.debug("#### Start main function ####")

    # Initialize Pygame if display is enabled
    if args.d:
        pygame.init()
        display = PYGAME_DISPLAY(args.width, args.height, args.f, args.tile_size)
    else:
        display = None

    # Create the game instance
    logger.debug("#### Create Game instance ####")

    game = game_of_life(
        width=args.width,
        height=args.height,
        initial_cells=args.i,
        output_file=args.o,
        display=args.d,
        nb_gen=args.m,
        screen = display
    )
    # Run the game
    logger.debug("#### Start Game instance ####")
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