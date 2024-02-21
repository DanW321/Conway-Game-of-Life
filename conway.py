# imports
import pygame, sys
from pygame.locals import *
import numpy as np
import sys
import random
import math
from presets import glider
from presets import pulsar_p3
from presets import spaceship
from presets import glider_machine
from presets import pulsar_p15


class Cell(object):
    """ A class representing a grid cell

    These cells make up Conway's Game of Life, and they can 
    be in one of three states. The two main states are
    dead (0) and alive (1). The third state is 
    draggable (2) and does not affect the simulation.

    :param x: the x pixel location of the grid cell 
    :param y: the y pixel location of the grid cell
    :param state: 0, 1 or 2 depending on the state of the cell
    """
    def __init__(self, x: int, y: int, state: int):
        # initializes variables
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
    def flipState(self):
        # flips the state of the cell
        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 0
    def getState(self):
        # returns the state of the cell
        return self.state
    def draw(self):
        # draws the cell based on its state
        color = None
        if self.state == 0:
            color = white
        elif self.state == 1:
            color = blue
        elif self.state == 2:
            color = red
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, cell_size, cell_size))
        pygame.draw.rect(display, gray, pygame.Rect(self.x, self.y, cell_size, cell_size), cell_border)


class Draggable(object):
    """ A class representing a draggable object

    This is a wrapper class for the five preset draggable 
    objects supported by this program. The arrays representing 
    the objects are imported from the presets.py file.

    :param type: a string indicating the type of object
    """
    def __init__(self, type: str):
        # initializes variables
        super().__init__()
        self.box = None
        self.setBox(type)
    def setBox(self, type: str):
        # sets the type of the object
        if type == "glider":
            self.box = glider
        elif type == "pulsar_p3":
            self.box = pulsar_p3
        elif type == "spaceship":
            self.box = spaceship
        elif type == "glider_machine":
            self.box = glider_machine
        elif type == "pulsar_p15":
            self.box = pulsar_p15
    def getBox(self) -> np.ndarray:
        # returns the array containing the object
        return self.box


def check_flip(row: int, col: int) -> bool:
    """ Checks if the state of a shell should be flipped

    This function checks the eight neighbors around a cell 
    and, based on a set of rules, determines whether its 
    condition should be flipped.

    :param row: the row of the cell to be checked
    :param col: the column of the cell to be checked
    :return: a boolean, should the cell be flipped?
    """
    # loops through the eight neighbors and counts alive cells
    counter = 0
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i == row and j == col:
                continue
            if cells[i % num_cells, j % num_cells].getState() == 1:
                counter += 1
    # checks if the cell should be flipped based on neighborhood
    if cells[row, col].getState() == 0:
        if counter == 3:
            return True
        return False
    elif cells[row, col].getState() == 1:
        if counter < 2 or counter > 3:
            return True
        return False


def flip_handler():
    """ Handles flipping cells

    This function loops through the game board and calls
    check_flip() on each cell to determine which cells
    should be flipped, then flips those cells.
    """
    # loops through the gameboard to determine flips
    global timestep
    flips = np.ndarray((num_cells, num_cells), dtype = bool)
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            flips[i, j] = check_flip(i, j)
    # flips cells
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            if flips[i ,j]:
                cells[i, j].flipState()
    timestep += 1


def cell_handler():
    """ Handles drawing cells
    
    This function loops through the board and draws each cell.
    """
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            cells[i, j].draw()


def display_text(text: str, num: int):
    """ Displays text 
    
    A helper function that displays the passed in text
    at a certain location on the screen.

    :param text: the text to display
    :param int: the location of the text
    """
    display.blit(font.render(text, True, white), (text_x_offset, text_y_offset + num * text_buffer))


def text_handler():
    """ Handles program text
    
    This function handles the text of the program. Depending
    on if the user is dragging an object, or if the program
    is paused, different text will display.
    """
    if not dragging:
        pause_text = ""
        if paused:
            pause_text = "Play"
            display_text("L-Click Cells to Toggle", 4)
            display_text("R-Click Cells to Draw", 5)
            display_text("Press R to Randomize", 6)
            display_text("Press C to Clear", 7)
            display_text("-" * num_dashes, 8)
            display_text("Press 1 for Glider", 9)
            display_text("Press 2 for Pulsar (p3)", 10)
            display_text("Press 3 for Spaceship", 11)
            display_text("Press 4 for Glider Machine", 12)
            display_text("Press 5 for Pulsar (p15)", 13)
        elif not paused:
            pause_text = "Pause"
        display_text("Press SPACE to " + pause_text, 0)
        display_text("Timestep: " + str(timestep), 1)
        display_text("FPS: " + str(display_fps), 2)
        display_text("Use ARROWS to Adjust FPS", 3)
    elif dragging:
        display_text("Click to Drop", 0)
        display_text("Press ESC to Exit Drag", 1)


def drag_handler():
    """ Handles draggable objects

    This function handles draggable objects as they are 
    moved around the screen by the user and possibly placed.
    """
    # gets the row and column of the mouse
    global dragging
    point = pygame.mouse.get_pos()
    row = math.floor(point[0]/cell_size)
    col = math.floor(point[1]/cell_size)
    # gets the shape of the draggable object
    box = draggable.getBox()
    shape_x = np.shape(box)[0]
    shape_y = np.shape(box)[1]
    # prevents the object from being dragged offscreen
    if row + shape_x > num_cells:
        row = num_cells - shape_x
    if col + shape_y > num_cells:
        col = num_cells - shape_y
    # draws the draggable object
    for i in range(shape_x):
        for j in range(shape_y):
            state = box[i, j]
            cell = Cell((row + i) * cell_size, (col + j) * cell_size, state)
            cell.draw()
    border = pygame.Rect(row * cell_size, col * cell_size, shape_x * cell_size, shape_y * cell_size)
    pygame.draw.rect(display, black, border, drag_border)
    # if the mouse is clicked, places the draggable object
    if pygame.mouse.get_pressed()[0]:
        for i in range(shape_x):
            for j in range(shape_y):
                current = cells[row + i, col + j].getState()
                desired = box[i, j]
                if (current == 0 and desired == 2) or (current == 1 and desired == 0):
                    cells[row + i, col + j].flipState()
        dragging = False
    

def mouse_handler(lr: str):
    """ Handles mouse clicks

    This function calls flipState() on cells that were 
    clicked. For left-clicks, the state of a cell is
    toggled. For right-clicks, the state of a cell can
    only switched to alive.

    :param lr: was the click left or right?
    """
    # gets the row and column of the mouse
    point = pygame.mouse.get_pos()
    row = math.floor(point[0]/cell_size)
    col = math.floor(point[1]/cell_size)
    # checks if a cell's state should be flipped
    if (row < num_cells and paused):
        if lr == "left":
            cells[row, col].flipState()
        elif lr == "right":
            if cells[row, col].getState() == 0:
                cells[row, col].flipState()


def key_handler():
    """ Handles key presses

    This function handles what happens when a key is
    pressed. Certain keys only function when the user
    is dragging / not dragging an object, or when the 
    program is paused.
    """
    global paused
    global timestep
    global display_fps
    global dragging
    global draggable
    if not dragging:
        if pygame.key.get_pressed()[K_SPACE]:
            if paused:
                paused = False
            elif not paused:
                paused = True
        if pygame.key.get_pressed()[K_LEFT] and display_fps > fps_min:
            display_fps -= fps_delta
        if pygame.key.get_pressed()[K_RIGHT] and display_fps < fps_max:
            display_fps += fps_delta
        if paused:
            if pygame.key.get_pressed()[K_r]:
                timestep = 0
                initiate("random")
            if pygame.key.get_pressed()[K_c]:
                timestep = 0
                initiate("clear")
            if pygame.key.get_pressed()[K_1]:
                dragging = True
                draggable = Draggable("glider")
            if pygame.key.get_pressed()[K_2]:
                dragging = True
                draggable = Draggable("pulsar_p3")
            if pygame.key.get_pressed()[K_3]:
                dragging = True
                draggable = Draggable("spaceship")
            if pygame.key.get_pressed()[K_4]:
                dragging = True
                draggable = Draggable("glider_machine")
            if pygame.key.get_pressed()[K_5]:
                dragging = True
                draggable = Draggable("pulsar_p15")
    else:
        if pygame.key.get_pressed()[K_ESCAPE]:
            dragging = False


def main_handler(click: bool):
    """ Main handler of program

    This function handles the logistics of the program
    and calls other handler methods when appropriate.

    :param flag: a boolean, was the mouse pressed?
    """
    global previous_time
    display.fill(black)
    if not dragging:
        if pygame.mouse.get_pressed()[0] and click:
            mouse_handler("left")
        elif pygame.mouse.get_pressed()[2]:
            mouse_handler("right")
        current_time = pygame.time.get_ticks()
        if not paused and current_time - previous_time >= msecs / display_fps:
            flip_handler()
            previous_time = current_time
    text_handler()
    cell_handler()
    if dragging:
        drag_handler()


def initiate(action: str):
    """ Creates the game board

    This function initializes the gameboard empty
    or randomized based on the input parameter.

    :param action: create board empty or randomized?
    """
    for i in range(num_cells):
        for j in range(num_cells):
            state = None
            if action == "random":
                state = random.randint(0, 1)
            if action == "clear":
                state = 0
            cell = Cell(i * cell_size, j * cell_size, state)
            cells[i, j] = cell


# global variables used throughout the program
start = True
paused = True
width = 875
height = 600
cell_size = 8
num_cells = int(height / cell_size)
cell_border = 1
drag_border = 2
black = [0, 0, 0]
gray = [150, 150, 150]
white = [255, 255, 255]
red = [168, 20, 0]
blue = [0, 84, 163]
num_dashes = 42
system_fps = 60
display_fps = 5.0
timestep = 0
fps_min = 0.5
fps_max = 15
fps_delta = 0.5
previous_time = 0
msecs = 1000
text_x_offset = 610
text_y_offset = 10
text_buffer = 40
font_size = 18
dragging = False
draggable = None
cells = np.ndarray((num_cells, num_cells), dtype = Cell)


# initializes pygame
pygame.init()
framePerSec = pygame.time.Clock()
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.SysFont('Calibri', font_size)


# main loop of the program
while True:
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            key_handler()
        if event.type == MOUSEBUTTONDOWN:
            click = True
    if start:
        initiate("clear")
        main_handler(click)
        start = False
    main_handler(click)
    pygame.display.update()
    framePerSec.tick(system_fps)