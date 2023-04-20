#imports
import pygame
from math_functions import *

# pygame settings
pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
TITLE = "John Conway's Game Of Life Editor"
pygame.display.set_caption(TITLE)
CLOCK = pygame.time.Clock()
RUNNING = True
FPS = 144 

# game settings
background_color = (19,19,19)
#grid
grid_width = 2000
grid_height = 2000 
grid_color = (71,71,71)
grid_line_width = 1
#camera
camera_prev_pos = [0,0]
camera_pos = [-grid_width/2,-grid_height/2] # first two are the current pos and the other two are for calculating 
# cell is the actual cell which will perform different actions
cell_size = 20
cell_color = (196,196,196)
cell_positions = []
# selector the cursor pointing to a cell which will help in the placement of the cell
selector_color = (222,187,133)
selector_position = [0,0]

# other variables
clicked_pos = [0,0]

def move_camera(events:pygame.event.Event,keys:tuple,mouse_press:tuple)->None:
    global cell_positions,camera_pos,clicked_pos,camera_prev_pos,cell_size
    # camera scale and translate1 
    # if mouse middle button is pressed and moved, the camera will move
    for e in events:
        #if e.type == pygame.MOUSEWHEEL:
        #    if e.y == 1:
        #        cell_size += 1
        #    if e.y == -1 and cell_size > 20:
        #        cell_size -= 1
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 2: # middle mouse button
                clicked_pos = [mouse_pos[0],mouse_pos[1]] 
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 2:
                camera_prev_pos = camera_pos
        if mouse_press[1] and e.type == pygame.MOUSEMOTION:
            camera_pos = [(mouse_pos[0] - clicked_pos[0]) + camera_prev_pos[0],(mouse_pos[1] - clicked_pos[1]) + camera_prev_pos[1]]

# this function renders the grid
def render_grid()->None:
    global camera_pos
    #render the actual grid
    for x in range(int(grid_width/cell_size)):
        pygame.draw.line(WINDOW,(grid_color),((x*cell_size)+camera_pos[0],0),((x*cell_size)+camera_pos[0],WINDOW_HEIGHT),grid_line_width)
    for y in range(int(grid_height/cell_size)):
        pygame.draw.line(WINDOW,(grid_color),(0,(y*cell_size)+camera_pos[1]),(WINDOW_HEIGHT,(y*cell_size)+camera_pos[1]),grid_line_width)

#this function draws a single cell according to what cell you want to render
def draw_cell(which:int,position:tuple)->None:
    if which == 0:
        pygame.draw.rect(WINDOW,selector_color,(position[0],position[1],cell_size,cell_size))
    if which == 1:
        pygame.draw.rect(WINDOW,cell_color,(position[0],position[1],cell_size,cell_size))
       
# this function renders all the different types of cells
def render_cells(mouse_press:tuple,mouse_pos:tuple)->None:
    global cell_positions
    draw_cell(0,vec2add(selector_position,camera_pos))
    for position in cell_positions:
        draw_cell(1,vec2add(position,camera_pos))

    # render the selector
    for x in range(int(((grid_width-cell_size)/(cell_size)))):
        for y in range(int(((grid_height-cell_size)/(cell_size)))):
            if mouse_pos[0] > x*cell_size+camera_pos[0]:
                selector_position[0] = x*cell_size
            if mouse_pos[1] > y*cell_size+camera_pos[1]:
                selector_position[1] = y*cell_size
    # if mouse is pressed, place a cell, and don't place a cell if it is already present
    if mouse_press[0] and selector_position not in cell_positions:
        cell_positions.append(selector_position[:])
    elif mouse_press[2] and selector_position in cell_positions:
        pop_index = cell_positions.index(selector_position)
        cell_positions.pop(pop_index)
                
# game loop
while RUNNING:
    # handle the events
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            RUNNING = False
    # update the background
    WINDOW.fill(background_color)
    # camera movement
    move_camera(events,keys,mouse_press)
    #all the rendering goes here
    render_grid()
    render_cells(mouse_press,mouse_pos)
    # update the frame
    pygame.display.flip()
    # for deltatime calcuation
    CLOCK.tick(FPS)

pygame.quit()
