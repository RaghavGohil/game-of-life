# this project needs performance updates because I suck at programming shi* (also I am too lazy for encapsultion)
# imports
import threading # for the simulation
import pygame
import time
import pygame_gui
from math_functions import *

# pygame settings
pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH,WINDOW_HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
TITLE = "John Conway's Game Of Life Simulator"
pygame.display.set_caption(TITLE)
CLOCK = pygame.time.Clock()
RUNNING = True
FPS = 144 

# gui settings
GUI_MANAGER = pygame_gui.UIManager(WINDOW_SIZE)
TIME_DELTA = 0

# game settings
background_color = (19,19,19)
#simulation
has_begin_simulation = False 
simulation_update_time = 2
#ui
clear_button =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-120,-100), (100,40)),text='clear',anchors={'right':'right','bottom':'bottom'},manager=GUI_MANAGER)
begin_simulation_button =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-220, -220), (200, 40)),text='begin_simulation',anchors={'right':'right','bottom':'bottom'},manager=GUI_MANAGER)
stop_simulation_button =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-220, -160), (200, 40)),text='stop_simulation',anchors={'right':'right','bottom':'bottom'},manager=GUI_MANAGER)
stop_simulation_button.disable()
cursor_on_button = False
#grid
grid_width = 2000
grid_height = 2000 
grid_color = (71,71,71)
grid_line_width = 1
#camera
camera_prev_pos = [-grid_width/2,-grid_height/2]
camera_pos = [-grid_width/2,-grid_height/2] # go to the center of the grid 
clicked_pos = [0,0]
# cell is the actual cell which will perform different actions
can_edit_cells = True
cell_size = 20
cell_color = (196,196,196)
cell_positions = []
# selector the cursor pointing to a cell which will help in the placement of the cell
selector_color = (222,187,133)
selector_position = [0,0]

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
       
def delete_cell(position:list)->None:
    global cell_positions
    pop_index = cell_positions.index(position)
    cell_positions.pop(pop_index)

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
        if not cursor_on_button and can_edit_cells:
            cell_positions.append(selector_position[:])
    elif mouse_press[2] and selector_position in cell_positions:
        if not cursor_on_button and can_edit_cells:
            delete_cell(selector_position)

def simulate()->None: #supported multithreading!!!
    global has_begin_simulation,cell_positions
    #cells
    neighbours = [None]*8 # create an empty list of lists (total count 8)
    print(neighbours) # apparently without this the initialization is not working lol (don't remove this unless you want to break things up.
    neighbour_count = 0
    while True:
        if has_begin_simulation:
            for position in cell_positions:
                # initialize potential neighbours
                neighbours[0] = [position[0]-cell_size,position[1]]
                neighbours[1] = [position[0]+cell_size,position[1]]
                neighbours[2] = [position[0],position[1]-cell_size]
                neighbours[3] = [position[0],position[1]+cell_size]
                neighbours[4] = [position[0]-cell_size,position[1]-cell_size]
                neighbours[5] = [position[0]+cell_size,position[1]-cell_size]
                neighbours[6] = [position[0]-cell_size,position[1]+cell_size]
                neighbours[7] = [position[0]+cell_size,position[1]+cell_size]
                neighbour_count = 0
                # Any live cell with fewer than two live neighbours dies (referred to as underpopulation).
                for neighbour in neighbours: # count the number of neighbours
                    if neighbour in cell_positions:
                        neighbour_count += 1 # yay! we have a new neighbour!
                if neighbour_count < 2 or neighbour_count > 3: # if there are less than two neighbours or grreater than to the current cell it dies.
                    delete_cell(position)
                # Any empty or dead cell can come to life if it has precisely 3 neighbours as if by reproduction.
            time.sleep(simulation_update_time)
        else:
            return #close the thread.

# game loop
while RUNNING:
    # for deltatime calcuation
    TIME_DELTA = CLOCK.tick(FPS)
    # handle the events
    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    #event handling (game+ui)
    for e in events:
        if e.type == pygame.QUIT:
            has_begin_simulation = False
            RUNNING = False
        if e.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            cursor_on_button = True 
        if e.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            cursor_on_button = False 
        if e.type == pygame_gui.UI_BUTTON_PRESSED:
            if e.ui_element == clear_button:
                cell_positions.clear()
            if e.ui_element == begin_simulation_button:
                # simulation
                simulation_thread = threading.Thread(target=simulate)
                simulation_thread.start()
                has_begin_simulation = True
                begin_simulation_button.disable()
                stop_simulation_button.enable()
                clear_button.disable()
                can_edit_cells = False
            if e.ui_element == stop_simulation_button:
                begin_simulation_button.enable()
                stop_simulation_button.disable()
                clear_button.enable()
                can_edit_cells = True
                has_begin_simulation = False
        GUI_MANAGER.process_events(e)
    # update the background
    WINDOW.fill(background_color)
    # camera movement
    move_camera(events,keys,mouse_press)
    #all the rendering goes here
    render_grid()
    render_cells(mouse_press,mouse_pos)
    # gui
    GUI_MANAGER.update(TIME_DELTA)
    GUI_MANAGER.draw_ui(WINDOW)
    # update the frame
    pygame.display.flip()

pygame.quit()
exit()
