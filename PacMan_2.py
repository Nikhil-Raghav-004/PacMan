# # for i in d:
# #     print(i)
#
# # for i,j in d.items():
# #     print(i,j)
#
# #
# # l = ["Blinky","Inky","Pinky","Clyde"]
#
#
# # for i in l:
# #     print(i)
#
#
# #
# # for i,j in enumerate(l):
# #     print(i,j)
#
# # print(enumerate(l))
#
#
# # d = {"name": "Nikhil","standard" : 7}
#
#
#
#
# # starting position                ending position
#
#
# from pathfinding.core.grid import Grid
#
# from pathfinding.finder.breadth_first import BreadthFirstFinder as BFF
# from pathfinding.core.diagonal_movement import DiagonalMovement
#
# from pathfinding.finder.a_star import AStarFinder
#
# # 0 ---> free   1 ---> blocke
#
# maze = [
#     [0, 0, 1, 1, 0],
#     [1, 0, 1, 0, 0],
#     [1, 0, 1, 1, 0],
#     [1, 0, 0, 0, 0], #r : 3, c : 4
# ]
#
# #step 1 : convert the 2d list into a grid
# gr = Grid(matrix = maze)
#
# # print(gr)
#
# # step2 : define the starting and ending positions
# start = gr.node(0,0)
# end = gr.node(4,3)
#
#
# # step3 : disable the diagonal movement
# # finder = BFF(diagonal_movement=DiagonalMovement.never)
#
# finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
#
# # step4 : find the path
# path,runs = finder.find_path(start,end,gr)
#
# #step5 : print the path
# print("Path:",path)
# print("runs:",runs)
#
#
#
#
#
#


# from pathfinding.core.diagonal_movement import DiagonalMovement
# from pathfinding.core.grid import Grid
# from pathfinding.finder.a_star import AStarFinder
#
#
# matrix = [
#     [0, 0, 0, 0, 0],
#     [1, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [0, 1, 1, 0, 0],
# ]
#
# grid = Grid(matrix=matrix)
#
# start = grid.node(0, 0)
# end = grid.node(4, 3)
#
# finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
# path, runs = finder.find_path(start, end, grid)
#
# print("Path:", path)
# print("Total steps:", len(path))


import pygame

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import random
import sys

pygame.init()

width = 700
height = 575
tile_size = 25

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame basics")

Blinky = pygame.image.load("pacman_assets/ghosts/blinky.png")
Blinky = pygame.transform.scale(Blinky, (20, 20))

Dots_Food = pygame.image.load("pacman_assets/other/dot.png")
Dots_Food = pygame.transform.scale(Dots_Food, (25, 25))

font = pygame.font.SysFont("Arial", 24, bold=True)
big_font = pygame.font.SysFont("Arial Black", 60, bold=True)
mid_font = pygame.font.SysFont("Arial Black", 35, bold=True)


Maze = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "######.## ######## ##.######",
    ".......   #      #   .      ",
    "######.## ######## ##.######",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "############################"
]

pacman_imgs = {
    "right": pygame.transform.scale(pygame.image.load("pacman_assets/pacman-right/1.png"), (20, 20)),
    "left": pygame.transform.scale(pygame.image.load("pacman_assets/pacman-left/1.png"), (20, 20)),
    "down": pygame.transform.scale(pygame.image.load("pacman_assets/pacman-down/1.png"), (20, 20)),
    "up": pygame.transform.scale(pygame.image.load("pacman_assets/pacman-up/1.png"), (20, 20)),
}
Score = 0
Rows = len(Maze)
Cols = len(Maze[5])
pac_tile_x,pac_tile_y = 1,1

pac_dir = (0,0)

next_dir = (1,0)

pac_speed = 4
pac_offset_x, pac_offset_y = 0, 0

pacman_di = 'right'

# (1,0) : right
# (-1,0) : left
# (0,-1) : up
# (0,1) : down

# next_dir = (1,0)

# can_move() : tells if a position is moveable or not
dots = [] # empty list



for y, row in enumerate(Maze):
    for x, col in enumerate(row):
        if col == ".":
            rect = pygame.Rect(x * tile_size + 5, y * tile_size + 5, 14, 14)
            dots.append(rect)

def reset_positions():
    global  pac_tile_x, pac_tile_y, pac_offset_x, pac_offset_y, ghost_x,ghost_y

    pac_tile_x, pac_tile_y = 1,1
    pac_offset_x, pac_offset_y = 0,0

    new_tile = find_tiles()
    ghost_x = new_tile[0] * tile_size
    ghost_y = new_tile[1] * tile_size

lives = 3
def game_over_screen():
    while True:
        screen.fill('black')
        t = big_font.render("GAME OVER!!",True, 'white')
        screen.blit(t, (width // 2 -200,200))


        exit_text =mid_font.render("EXIT",True,'yellow')
        exit_rect =exit_text.get_rect(center = (width//2, 340))
        pygame.draw.rect(screen,'brown',exit_rect)
        screen.blit(exit_text,exit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

def show_life_lost():
    screen.fill("black")
    t = big_font.render("LIFE LOST!",True,'white')
    info = mid_font.render("Get Ready....",True, "yellow")

    t_width =t.get_width() // 2
    info_width = info.get_width() // 2

    screen.blit(t, (width // 2 - t_width, 200))
    screen.blit(info,(width//2 - info_width, 300))

    pygame.display.flip()
    pygame.time.delay(1500)

def check_ghost_collision():
    global lives

    pac_rect = pygame.Rect(pac_tile_x * tile_size + pac_offset_x, pac_tile_y * tile_size + pac_offset_y,20,20)

    ghost_rect = pygame.Rect(ghost_x,ghost_y,20,20)


    if pac_rect.colliderect(ghost_rect):
        lives -= 1
        show_life_lost()
        reset_positions()

        if lives <= 0 :
            game_over_screen()


def pathfinding_next_step(start,goal):
    #convert the maze into a grid
    # 1 path , 0 wall
    matrix = []
    for row in Maze:
        line = [] # empty list
        for col in row:
            if col == '#':
                line.append(0)
            else:
                line.append(1)

        matrix.append(line)

    grid = Grid(matrix = matrix)

    start_node = grid.node(start[0],start[1]) # position of ghost
    end_node = grid.node(goal[0],goal[1]) # position of pacman

    finder = AStarFinder(diagonal_movement= DiagonalMovement.never)

    path, sme = finder.find_path(start_node,end_node,grid)

    if len(path) > 1:
        var  = tuple(path[1])
        return var
    return start


def find_tiles():
    free_tiles = []
    for y,row in enumerate(Maze):
        for x,col in enumerate(row):
            if col in ('.',' '):
                free_tiles.append((x,y))

    return random.choice(free_tiles)


ghost_speed = 2
ghost_tile = find_tiles()
ghost_x,ghost_y = ghost_tile[0] * tile_size , ghost_tile[1] * tile_size

def move_ghost():
    global ghost_x, ghost_y, ghost_target_tile

    pgrid =(pac_tile_x,pac_tile_y)
    ggrid =(ghost_x // tile_size, ghost_y // tile_size)

    if ( ghost_x % tile_size == 0) and (ghost_y % tile_size == 0):
        # ggrid = (ghost_x // tile_size, ghost_y // tile_size)
        ghost_target_tile = pathfinding_next_step(ggrid,pgrid)

    target_x,target_y = ghost_target_tile[0]*tile_size, ghost_target_tile[1] * tile_size

    if ghost_x < target_x:
        ghost_x += ghost_speed

    elif ghost_x > target_x:
        ghost_x -= ghost_speed

    if ghost_y < target_y:
        ghost_y += ghost_speed

    elif ghost_y > target_y:
        ghost_y -= ghost_speed


    if abs(ghost_x - target_x) < ghost_speed :
        ghost_x = target_x

    if abs(ghost_y - target_y) < ghost_speed:
        ghost_y = target_y


    screen.blit(Blinky,(ghost_x,ghost_y))








def draw_maze():
    for y, row in enumerate(Maze):
        for x, col in enumerate(row):

            if col == "#":
                pygame.draw.rect(screen, 'blue', (x * tile_size, y * tile_size, tile_size, tile_size))
            # else:
            #     screen.blit(Dots_Food, (x * tile_size, y * tile_size))
    for d in dots:
        screen.blit(Dots_Food, d.topleft)


def can_move(grid_x,grid_y):
    if 0<=grid_x < Cols and 0 <= grid_y < Rows:
        if Maze[grid_y][grid_x] != '#':
            return True

    return False


def Move_Pacman():
    global next_dir,pac_dir,pac_tile_x,pac_tile_y,pac_speed,running,pac_offset_x, pac_offset_y, pacman_di
    keys =pygame.key.get_pressed()
    #check the direction
    if keys[pygame.K_UP]:
        next_dir = (0,-1)
        pacman_di ='up'

    elif keys[pygame.K_DOWN]:
        next_dir = (0, 1)
        pacman_di = 'down'

    elif keys[pygame.K_RIGHT]:
        next_dir = (1,0)
        pacman_di = 'right'

    elif keys[pygame.K_LEFT]:
        next_dir = (-1,0)
        pacman_di = 'left'

    #check if the pacman can move
    if pac_offset_x == 0 and pac_offset_y == 0:
        if can_move(pac_tile_x+next_dir[0], pac_tile_y + next_dir[1]):
            pac_dir =next_dir

        if not can_move(pac_tile_x + pac_dir[0], pac_tile_y + pac_dir[1]):
            pac_dir = (0,0)

    # moving the pacman along x and y direction
    pac_offset_x += pac_dir[0] * pac_speed
    pac_offset_y += pac_dir[1] * pac_speed



# smooth movement of the pacman

    if pac_offset_x >= tile_size:
        pac_tile_x += 1
        pac_offset_x = 0

    if pac_offset_x <= -tile_size:
        pac_tile_x -= 1
        pac_offset_x = 0

    if pac_offset_y >= tile_size:
        pac_tile_y += 1
        pac_offset_y = 0

    if pac_offset_y <= -tile_size:
        pac_tile_y -= 1
        pac_offset_y = 0


    # pacman collides with the dots, dots have to disappear , some point wil be gained

    #surround the pacman with a rect or hitbox

    pac_rect = pygame.Rect(pac_tile_x * tile_size + pac_offset_x, pac_tile_y * tile_size + pac_offset_y,20,20)

    for d in dots[:]:
        if pac_rect.colliderect(d):
            dots.remove(d)

    px = pac_tile_x * tile_size + pac_offset_x
    py  = pac_tile_y * tile_size + pac_offset_y

    screen.blit(pacman_imgs[pacman_di],(px,py))















# (10,15)
#
# (-1,0)
#
# (9,15)





def Dis_Score(Score):
    font = pygame.font.SysFont("Papyrus",30)
    text = font.render(f"Score: {Score}",True,'white')
    screen.blit(text,(540,-7))

def Dis_Lives(Lives):
    font = pygame.font.SysFont("Papyrus",30)
    text = font.render(f"Lives: {Lives}",True,'white')
    screen.blit(text,(0,-7))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    draw_maze()
    # screen.blit(Blinky,(100,100))
    # screen.blit(Dots_Food,(200,200))
    move_ghost()
    Move_Pacman()
    check_ghost_collision()
    Dis_Lives(lives)
    Dis_Score(Score)
    pygame.display.flip()
    clock.tick(50)















#
# every time the ghost moves on its own
# 1. it has to move only in the path
# 2. the path has to lead to the pacman
