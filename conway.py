import pygame, sys
from pygame.locals import *
import numpy as np
import sys
import random
import math
        
class Cell(object):
    def __init__(self,x,y,state):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state
    def flipState(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
    def getState(self):
        return self.state
    def draw(self):
        color = None
        if self.state == 0:
            color = white
        elif self.state == 1:
            color = red
        else:
            color = light_red
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, cell_size, cell_size))
        pygame.draw.rect(display, black, pygame.Rect(self.x, self.y, cell_size, cell_size), cell_border)

class Draggable(object):
    def __init__(self, type):
        super().__init__()
        self.box = None
        self.setBox(type)
    def setBox(self, type):
        if type == "glider":
            self.box = np.zeros((3, 3))
            self.box[0,1] = 2
            self.box[1,2] = 2
            self.box[2,0] = 2
            self.box[2,1] = 2
            self.box[2,2] = 2
        if type == "pulsar":
            self.box = np.zeros((12, 3))
            
    def getBox(self):
        return self.box

def check_flip(x, y):
    counter = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            if cells[i % num_cells, j % num_cells].getState() == 1:
                counter += 1
    if cells[x, y].getState() == 0:
        if counter == 3:
            return True
        return False
    else:
        if counter < 2 or counter > 3:
            return True
        return False

def flip_handler():
    global timestep
    flips = np.ndarray((num_cells, num_cells), dtype = bool)
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            flips[i, j] = check_flip(i, j)
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            if flips[i ,j]:
                cells[i, j].flipState()
    timestep += 1

def cell_handler():
    for i in range(np.shape(cells)[0]):
        for j in range(np.shape(cells)[1]):
            cells[i ,j].draw()

def text_handler():
    if not dragging:
        pause_text = ""
        if paused:
            pause_text = "Play"
            display_text("Click Cells to Draw", 4)
            display_text("Press R to Randomize", 5)
            display_text("Press C to Clear", 6)
            display_text("Press 1 for Glider", 10)
        else:
            pause_text = "Pause"
        display_text("Press SPACE to " + pause_text, 0)
        display_text("Timestep: " + str(timestep), 1)
        display_text("FPS: " + str(display_fps), 2)
        display_text("Use ARROWS to Adjust FPS", 3)
    else:
        display_text("Click to Drop", 0)
        display_text("Press ESC to Exit Drag", 1)
    
def display_text(text, num):
    display.blit(font.render(text, True, white), (text_x_offset, text_y_offset + num * text_buffer))

def drag_handler():
    global dragging
    point = pygame.mouse.get_pos()
    row = math.floor(point[0]/cell_size)
    col = math.floor(point[1]/cell_size)
    box = draggable.getBox()
    shape_x = np.shape(box)[0]
    shape_y = np.shape(box)[1]
    if row + shape_x > num_cells:
        row = num_cells - shape_x
    if col + shape_y > num_cells:
        col = num_cells - shape_y
    for i in range(shape_x):
        for j in range(shape_y):
            state = box[i, j]
            cell = Cell((row + i) * cell_size, (col + j) * cell_size, state)
            cell.draw()
    if pygame.mouse.get_pressed()[0]:
        for i in range(shape_x):
            for j in range(shape_y):
                current_state = cells[row + i, col + j].getState()
                desired_state = box[i, j]
                if desired_state == 2:
                    desired_state = 1
                if current_state != desired_state:
                    cells[row + i, col + j].flipState()
        dragging = False

def main_handler(flag):
    global previous_time
    display.fill(black)
    if not dragging:
        if pygame.mouse.get_pressed()[0] and flag:
            mouse_handler("left")
        elif pygame.mouse.get_pressed()[2]:
            mouse_handler("right")
        current_time = pygame.time.get_ticks()
        if not paused and current_time - previous_time >= 1000/display_fps:
            flip_handler()
            previous_time = current_time
    text_handler()
    cell_handler()
    if dragging:
        drag_handler()
    
def mouse_handler(flag):
    point = pygame.mouse.get_pos()
    row = math.floor(point[0]/cell_size)
    col = math.floor(point[1]/cell_size)
    if (row < num_cells and paused):
        if flag == "left":
            cells[row, col].flipState()
        if flag == "right":
            if cells[row, col].getState() == 0:
                cells[row, col].flipState()

def key_handler():
    global paused
    global timestep
    global display_fps
    global dragging
    global draggable
    if not dragging:
        if pygame.key.get_pressed()[K_SPACE]:
            if paused:
                paused = False
            else:
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
    else:
        if pygame.key.get_pressed()[K_ESCAPE]:
            dragging = False

def initiate(action):
    for i in range(num_cells):
        for j in range(num_cells):
            state = None
            if action == "random":
                state = random.randint(0, 1)
            if action == "clear":
                state = 0
            cell = Cell(i * cell_size, j * cell_size, state)
            cells[i, j] = cell

paused = True
start = True
width = 875
height = 600
cell_size = 10
num_cells = int(height / cell_size)
cell_border = 1
black = [0,0,0]
white = [255,255,255]
red = [255,0,0]
light_red = [255, 153, 156]
system_fps = 60
text_x_offset = 610
text_y_offset = 10
text_buffer = 40
timestep = 0
display_fps = 5.0
fps_min = 0.5
fps_max = 15
fps_delta = 0.5
previous_time = 0
dragging = False
draggable = None
cells = np.ndarray((num_cells, num_cells), dtype = Cell)

pygame.init()
framePerSec = pygame.time.Clock()
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.SysFont('Calibri', 18, False, False)

while True:
    mouse_down = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            key_handler()
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
    if start:
        initiate("clear")
        main_handler(mouse_down)
        start = False
    main_handler(mouse_down)
    pygame.display.update()
    framePerSec.tick(system_fps)