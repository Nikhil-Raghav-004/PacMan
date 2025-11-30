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
Score = 0

font = pygame.font.SysFont("Arial", 24, bold=True)
big_font = pygame.font.SysFont("Papyrus", 60, bold=True)
mid_font = pygame.font.SysFont("Papyrus", 35, bold=True)



clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame basics")

Blinky = pygame.image.load("pacman_assets/ghosts/blinky.png")
Blinky = pygame.transform.scale(Blinky,(20,20))

Dots_Food = pygame.image.load("pacman_assets/other/dot.png")
Dots_Food = pygame.transform.scale(Dots_Food,(25,25))

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
    "      .##          ##.      ",
    "######.## ######## ##.######",
    "      .   #          .      ",
    "######.## ######## ##.######",
    "     #.##          ##.#     ",
    "      .## ######## ##.      ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#...##................##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "############################"
]

pacman_imgs = {
                "right" : pygame.transform.scale(pygame.image.load("pacman_assets/pacman-right/1.png"), (20,20)),
                "left"  : pygame.transform.scale(pygame.image.load("pacman_assets/pacman-left/1.png"), (20, 20)),
                "down"  : pygame.transform.scale(pygame.image.load("pacman_assets/pacman-down/1.png"), (20,20)),
                "up"    :  pygame.transform.scale(pygame.image.load("pacman_assets/pacman-up/1.png"), (20,20))  ,
}

Dots = []

for y, row in enumerate(Maze):
    for x, col in enumerate(row):
        if col == ".":
            rect = pygame.Rect(x * tile_size + 5, y * tile_size + 5, 14, 14)
            Dots.append(rect)


pac_tile_x,pac_tile_y = 1,1
pac_Dir= (0,0)
next_dir = (1,0)
pac_speed  =  8
pac_offset_X,pac_offset_Y = 0,0
pacmaN_Di = 'right'

def can_Move(grid_x,grid_y):

    if 0 <= grid_x < Cols and 0 <= grid_y < Rows:
        if Maze[grid_y][grid_x] != "#":
            return True

    return False

def reset_pos():
    global pac_tile_x,pac_tile_y,pac_offset_X,pac_offset_Y, ghost_x, ghost_y

    pac_tile_x, pac_tile_y = 1,1
    pac_offset_X,pac_offset_Y = 0,0

    new_tile = find_tiles()
    ghost_x = new_tile[0] * tile_size
    ghost_y = new_tile[1] * tile_size


lives = 3

def show_life_lost():
    screen.fill("black")

    t = big_font.render("YOU LOST A LIFE!", True,'white')

    info = mid_font.render("Get Ready For A CHANCE", True, ' yellow')

    t_width = t.get_width() // 2
    info_width = info.get_width() // 2

    screen.blit(t, (width //2  - t_width, 200))
    screen.blit(info, (width // 2 - info_width, 300))

    pygame.display.flip()
    pygame.time.delay(1500)


def game_Over_screen():
    while True:
        screen.fill('black')
        t = big_font.render("GAME OVER", True, 'white')
        screen.blit(t,(width // 2 - 200,200))

        exit_text = mid_font.render('Exit', True,'red')
        exit_Rext = exit_text.get_rect(center = (width / 2, 340))
        pygame.draw.rect(screen,'brown', exit_Rext)
        screen.blit(exit_text,exit_Rext)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.quit():
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_Rext.collidepoint(event.pos):
                pygame.quit()
                sys.exit()


def check_ghost_collision():
    global lives

    pac_rect = pygame.Rect(pac_tile_x * tile_size + pac_offset_X, pac_tile_y * tile_size + pac_offset_Y,20,20)

    ghost_rect = pygame.Rect(ghost_x,ghost_y,20,20)

    if pac_rect.colliderect(ghost_rect):
        lives -= 1
        show_life_lost()
        reset_pos()
        if lives <= 0 :
            game_Over_screen()




def path__Finding_New_step(start,goal):
    #convert maze into a grid
    # 1--> Path, 0 --> Wall
    matrix = []

    for row in Maze:
        line = [] # Empty List
        for col in row:
            if col == "#":
                line.append(0)
            else:
                line.append(1)
        matrix.append(line)

    grid = Grid(matrix = matrix)

    start_node = grid.node(start[0],start[1])
    end_node = grid.node(goal[0],goal[1])

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

    path,sme = finder.find_path(start_node,end_node,grid)

    if len(path) >1:
        var = tuple(path[1])
        return var
    return start

def find_tiles():
    free_tiles = []
    for y,row in enumerate(Maze):
        for x,col in enumerate(row):
            if col in ('.',' '):
                free_tiles.append((x,y))

    return random.choice(free_tiles)


ghost_speed = 5
ghost_tile = find_tiles()
ghost_x,ghost_y = ghost_tile[0] * tile_size , ghost_tile[1] * tile_size

def move_DaGhost():
    global ghost_x,ghost_y,ghost_target_tile

    pgrid = (pac_tile_x,pac_tile_y)
    ggrid = (ghost_x // tile_size,  ghost_y // tile_size)

    if (ghost_x % tile_size == 0) and (ghost_y % tile_size == 0):
        #ggrid = (ghost_x // tile_size,  ghost_y // tile_size)
        ghost_target_tile = path__Finding_New_step(ggrid,pgrid)

    target_x,target_Y = ghost_target_tile[0]* tile_size, ghost_target_tile[1] * tile_size

    if ghost_x < target_x :
        ghost_x += ghost_speed
    elif ghost_x > target_x :
        ghost_x -= ghost_speed

    if ghost_y < target_Y:
        ghost_y += ghost_speed
    elif ghost_y > target_Y:
        ghost_y -= ghost_speed

    if abs(ghost_x - target_x) < ghost_speed:
        ghost_x = target_x

    if abs(ghost_y - target_Y) < ghost_speed:
        ghost_y = target_Y


    screen.blit(Blinky, (ghost_x,ghost_y))


def Move_Pacman():
    global next_dir,pac_Dir,pac_tile_x,pac_tile_y,pac_speed,running,pac_offset_X,pac_offset_Y, pacmaN_Di, Score
    #Check Direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        next_dir = (0,-1)
        pacmaN_Di = 'up'
        # path = pacman_imgs['up']
        # screen.blit(path,(10,10))

    elif keys[pygame.K_DOWN]:
            next_dir = (0,1)
            pacmaN_Di = 'down'
            # path = pacman_imgs['down']
            # screen.blit(path,(10,10))

    elif keys[pygame.K_RIGHT]:
            next_dir = (1,0)
            pacmaN_Di = 'right'
            # path = pacman_imgs['right']
            # screen.blit(path,(10,10))

    elif keys[pygame.K_LEFT]:
            next_dir = (-1,0)
            pacmaN_Di = 'left'
            # path = pacman_imgs['left']
            # screen.blit(path,(10,10))
    #To check if pacman ca move

    if pac_offset_X == 0 and pac_offset_Y == 0:
        if can_Move(pac_tile_x+next_dir[0], pac_tile_y+next_dir[1]):
            pac_Dir = next_dir

        if not can_Move(pac_tile_x+ pac_Dir[0], pac_tile_y+pac_Dir[1]):
            pac_Dir = (0,0)

    #Moving da pacman along x and direction
    pac_offset_X += pac_Dir[0] * pac_speed
    pac_offset_Y += pac_Dir[1] * pac_speed

    if pac_offset_X >= tile_size:
        pac_tile_x += 1
        pac_offset_X = 0

    if pac_offset_X <= -tile_size:
        pac_tile_x-=1
        pac_offset_X = 0

    if pac_offset_Y >= tile_size:
        pac_tile_y += 1
        pac_offset_Y = 0

    if pac_offset_Y <= -tile_size:
        pac_tile_y -=1
        pac_offset_Y = 0

    pac_rect = pygame.Rect(pac_tile_x * tile_size + pac_offset_X, pac_tile_y * tile_size + pac_offset_Y,20,20)

    px = pac_tile_x * tile_size + pac_offset_X
    py = pac_tile_y * tile_size + pac_offset_Y

    screen.blit(pacman_imgs[pacmaN_Di],(px,py))

    for d in Dots[:]:
        if pac_rect.colliderect(d):
            Dots.remove(d)
            Score += 1


Rows = len(Maze)
Cols = len(Maze[5])


def draw_maze():
    for y, row in enumerate(Maze):
        for x, col in enumerate(row):

            if col == "#":
                pygame.draw.rect(screen,'blue',(x * tile_size,y * tile_size,tile_size,tile_size))
        for d in Dots:
            screen.blit(Dots_Food, d.topleft)

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
    Move_Pacman()
    move_DaGhost()
    Dis_Score(Score)
    # show_life_lost()
    check_ghost_collision()
    # Dis_Lives(lives)
    pygame.display.flip()
    clock.tick(50)