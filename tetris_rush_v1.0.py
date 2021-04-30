import pygame
import random
import traceback

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# COLORS
black = (0,0,0); grey = (128,128,128); white = (255,255,255)
invisible = (1,1,1,); silver = (211,211,211); brown = (150, 75, 0)
red = (255,0,0); green = (0,255,0); blue = (64, 64, 255)
yellow = (255,255,0); magenta = (255, 0, 255); cyan = (0,255,255)
orange = (255, 165, 0); gold = (255, 215, 0); pink = (255,105,180)
violet = (160, 0, 160); teal = (0, 128, 128); turquoise = (64, 200, 200);


# SHAPE FORMATS

S = [[".00",
      "00",
      "..."],
     
     [".0.",
      ".00",
      "..0"],

     ["...",
      ".00",
      "00."],
     
     ["0..",
      "00.",
      ".0."]]

Z = [["00.",
      ".00",
      "..."],
     
     ["..0",
      ".00",
      ".0."],

     ["...",
      "00.",
      ".00"],
     
     [".0.",
      "00.",
      "0.."]]

I = [["....",
      "0000",
      "....",
      "...."],
     
     ["..0.",
      "..0.",
      "..0.",
      "..0."],

     ["....",
      "....",
      "0000",
      "...."],
     
     [".0..",
      ".0..",
      ".0..",
      ".0.."]]

O = [['.00.',
      '.00.',
      '....']]

J = [["0..",
      "000",
      "..."],
     
     [".00",
      ".0.",
      ".0."],

     ["...",
      "000",
      "..0"],
     
     [".0.",
      ".0.",
      "00."]]

L = [["..0",
      "000",
      "..."],
     
     [".0.",
      ".0.",
      ".00"],

     ["...",
      "000",
      "0.."],
     
     ["00.",
      ".0.",
      ".0."]]

T = [[".0.",
      "000",
      "..."],
     
     [".0.",
      ".00",
      ".0."],

     ["...",
      "000",
      ".0."],
     
     [".0.",
      "00.",
      ".0."]]

modern_level_list = [3,8,15,24,35,48,63,80,99,120,144,170]
gravity_list = [48/60, 43/60, 38/60, 33/60, 28/60, 23/60, 18/60, 13/60, 8/60, 6/60,
                         5/60,  5/60,  5/60,  4/60,  4/60,  4/60,  3/60,  3/60, 3/60, 2/60,
                         2/60,  2/60,  2/60,  2/60,  2/60,  2/60,  2/60,  2/60, 2/60, 1/60]
tetris_shapes = [S, Z, I, O, J, L, T]
shape_strings = ["S", "Z", "I", "O", "J", "L", "T"]
easy_shapes = [O]
tetris_shapes = [I, J, L, O, S, T, Z]
shape_colors = [cyan, blue, orange, yellow, green, violet, red]
shape_strings = ["I", "J", "L", "O", "S", "T", "Z"]
# index 0 - 6 represent shape


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.name = shape_strings[tetris_shapes.index(shape)]
        self.color = shape_colors[tetris_shapes.index(shape)]
        self.rotation = 0  # number from 0-3
                    
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1 and (x >= 5 and x <= 6):
            return True
    return False


def check_rows(grid, locked):
    for i in range(len(grid)-1,-1,-1):
        row_colors = grid[i]
        if (0, 0, 0) not in row_colors and (255,105,180) not in row_colors:  # If there is no black in all col...
           return i
    return -1

                
def clear_rows(grid, locked, pink_index):
    for j in range(len(grid[pink_index])):
        try:
            del locked[(j,pink_index)]
        except:
            continue
    for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
        x, y = key
        if y < pink_index:
            newKey = (x, y + 1)
            locked[newKey] = locked.pop(key)
    # pygame.time.delay(100)
                        

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def create_pink_rows(clear, grid, locked, win, next_shape):
    pink_row_list = []
    if not clear: 
        return pink_row_list
    for i in range(4):
        pink_row = check_rows(grid, locked)
        if pink_row != -1:
            pink_row_list.append(pink_row) 
            for x in range(10):
                locked[x, pink_row] = (255,105,180)
            grid = create_grid(locked)
    return pink_row_list

def display_statistics(surface):
    construct_I = ["    ", "xxxx"]
    construct_J = [" x   ", " xxx "]
    construct_L = ["   x ", " xxx "]
    construct_O = ["  xx ", "  xx "]
    construct_S = ["   xx", " xx  "]
    construct_T = ["   x  ", " xxx "]
    construct_Z = [" xx  ", "   xx"]
    constructs = [construct_I, construct_J, construct_L, construct_O,
                  construct_S, construct_T, construct_Z]
    global shape_stats, total_piece_count, most_spawns, least_spawns
    font = pygame.font.SysFont('comicsans', 50)
    small_font = pygame.font.SysFont("comicsans", 30)
    x_position_modifier = 0
    total_label = font.render(str(total_piece_count), 1, silver)
    surface.blit(total_label, (120,120))
    for i in range(7):
        for line in range(2):
            adjust = 75*i
            if i == 3:
                adjust -= 7
            if i > 3:
                adjust = adjust * .95
            stat_label = small_font.render(constructs[i][line], 1, shape_colors[i])
            surface.blit(stat_label, (30,180 + 20*line + adjust))
        label_color = black
        if shape_stats[shape_strings[i]]["shape_count"] == most_spawns:
            label_color = gold
        elif shape_stats[shape_strings[i]]["shape_count"] == least_spawns and total_piece_count > 5:
            label_color = red
        else:
            label_color = white
        # print(shape_stats[shape_strings[i]]["shape_count"], most_spawns)
        piece_count = font.render(str("{:02.0f}".format(shape_stats[shape_strings[i]]["shape_count"])), 1, label_color)
        surface.blit(piece_count, (80 + top_left_x - 355 + play_width/2 - (piece_count.get_width()/ 2),
                                70*i + top_left_y + play_height/2 - 190 - piece_count.get_height()/2))
        if shape_stats[shape_strings[i]]["percentage"] < 10:
            x_position_modifier = 10
        else:
            x_position_modifier = 0
        percentage_label = font.render(str(shape_stats[shape_strings[i]]["percentage"]) + "%", 1, (label_color))
        surface.blit(percentage_label, (x_position_modifier + 160 + top_left_x - 355 + play_width/2 - (percentage_label.get_width()/ 2),
                                70*i + top_left_y + play_height/2 - 190 - percentage_label.get_height()/2))
#"{:06.0f}"
        


def display_hud(surface, score, total_clears, tetris_rate, gravity, buffer_color):
    global fall_time
    global green_score
    global Fbu
    global go
    global begin
    global leveled_up
    global level_color
    global minutes
    global seconds
    global buffer
    show_level_up = False
    big_font = pygame.font.SysFont('comicsans', 40)
    font = pygame.font.SysFont('comicsans', 30)
    x_position_modifier = 0
    if game_type == "classic":
        x_position_modifier = 560   # If classic, move some elements to other side of grid  
        display_statistics(surface)
    if not go:
        if fall_time > 1500: draw_text_middle("GO!", 50, (211,211,211),surface)
        elif fall_time > 1000: draw_text_middle(str(1), 50, (211,211,211),surface)
        elif fall_time > 500: draw_text_middle(str(2), 50, (211,211,211),surface)
        else: draw_text_middle(str(3), 50, (211,211,211),surface)

    # level_color = (255, 0, 128)
    # if level > 28:
    #     level_color = (128,0,128)
    # elif level > 18:
    #     level_color = (255,0,255)
    # elif level > 15:
    #     level_color = (255,0,128)
    # elif level > 12:
    #     level_color = (255,0, 0)
    # elif level > 7:
    #     level_color = (255, 128, 0)  
    # elif level > 3:
    #     level_color = (0, 255, 255)
    # else:
    #     level_color = (0, 255, 0)    

    score_label = font.render("SCORE", 1, (255, 255, 255))
    surface.blit(score_label, (x_position_modifier + top_left_x -290 + play_width/2 - (score_label.get_width()/ 2),
                         top_left_y + play_height/2 - 60 - score_label.get_height()/2))
    player_score = font.render("{:06.0f}".format(int(score)), 1, brown)
    surface.blit(player_score, (x_position_modifier + top_left_x -290 + play_width/2 - (player_score.get_width()/ 2),
                         top_left_y + play_height/2 - 20 - player_score.get_height()/2))
    
    if green_score > 0:
        if leveled_up:
            draw_text_middle("Level Up!", 80, gold, surface)
        else:
            draw_text_middle("+" + str(int(green_score)), 80, green, surface)
    
    lines_label  = font.render("LINES", 1, white)
    surface.blit(lines_label, (x_position_modifier + top_left_x - 290 + play_width/2 - (lines_label.get_width()/ 2),
                               top_left_y + play_height/2 + 20 - lines_label.get_height()/2))    
    player_lines = font.render("{:03.0f}".format(total_clears), 1, brown)
    surface.blit(player_lines, (x_position_modifier + top_left_x - 290 + play_width/2 - (player_lines.get_width()/ 2),
                               top_left_y + play_height/2 + 60 - player_lines.get_height()/2))           
    
    level_label  = font.render("LEVEL", 1, white)
    surface.blit(level_label, (x_position_modifier + top_left_x - 290 + play_width/2 - (level_label.get_width()/ 2),
                            top_left_y + play_height/2 + 100 - level_label.get_height()/2))      
    player_level = font.render(("{:02.0f}").format(level), 1, level_color)
    surface.blit(player_level, (x_position_modifier + top_left_x - 290 + play_width/2 - (player_level.get_width()/ 2),
                                top_left_y + play_height/2 + 140 - player_level.get_height()/2))
    
    if game_type == "classic":
        tr_label = font.render("TETRIS RATE", 1, white)
    else:
        tr_label = font.render("SAFE BUFFER", 1, white)
    surface.blit(tr_label, (x_position_modifier + top_left_x - 290 + play_width/2 - (tr_label.get_width()/ 2),
                            top_left_y + play_height/2 + 180 - tr_label.get_height()/2))
    if game_type == "classic":
        player_tr = font.render(str(int(tetris_rate)) + "%", 1, brown)
    else:
        player_tr = font.render(str(buffer), 1, buffer_color)
    surface.blit(player_tr, (x_position_modifier + top_left_x - 290 + play_width/2 - (player_tr.get_width()/ 2),
                                top_left_y + 220 + play_height/2 - player_tr.get_height()/2))
    
    time_label  = font.render("TIME", 1, white)
    surface.blit(time_label, (x_position_modifier + top_left_x - 290 + play_width/2 - (time_label.get_width()/ 2),
                            top_left_y + play_height/2 + 270 - time_label.get_height()/2))    
    play_time = font.render("{0:0>2}".format(minutes) + ":" + "{0:0>2}".format(seconds), 1, brown)
    surface.blit(play_time, (x_position_modifier + top_left_x - 290 + play_width/2 - (play_time.get_width()/ 2),
                                top_left_y + 310 + play_height/2 - play_time.get_height()/2))
    


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
            
def draw_hold_shape(shape,surface):
    global first_hold
    global unlock_hold
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('HOLD SHAPE', 1, white)
    sx = top_left_x + play_width - 500
    sy = top_left_y + play_height/2 - 245
    format = shape.shape[shape.rotation % len(shape.shape)]
    if first_hold == False:
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    if shape.name == "O":
                            if unlock_hold:
                                pygame.draw.rect(surface, shape.color, (sx + j*30 -7, sy + i*30 + 50, 30, 30), 0)
                            else:
                                pygame.draw.rect(surface, grey, (sx + j*30 + -7, sy + i*30 + 50, 30, 30), 0)
                    elif shape.name == "I":
                        if unlock_hold:
                            pygame.draw.rect(surface, shape.color, (sx + j*30 + -5, sy + i*30 + 20, 30, 30), 0)
                        else:
                            pygame.draw.rect(surface, grey, (sx + j*30 + -5, sy + i*30 + 20, 30, 30), 0)
                    else:
                        if unlock_hold:
                            pygame.draw.rect(surface, shape.color, (sx + j*30 + 10, sy + i*30 + 35, 30, 30), 0)
                        else:
                            pygame.draw.rect(surface, grey, (sx + j*30 + 10, sy + i*30 + 35, 30, 30), 0)
    if game_type == "modern": surface.blit(label, (sx-10, sy-10))
    
def draw_next_shape(shape, surface):  # Used to show "next shape"
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('NEXT SHAPE', 1, white)
    sx = top_left_x + play_width + 55
    sy = top_left_y + play_height/2 - 245
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if shape.name == "O":
                if column == "0":
                    pygame.draw.rect(surface, shape.color, (sx + j*30 + 10, sy + i*30 + 50, 30, 30), 0)
            elif shape.name == "I":
                if column == "0":
                    pygame.draw.rect(surface, shape.color, (sx + j*30 + 10, sy + i*30 + 20, 30, 30), 0)
            else:
                if column == "0":
                    pygame.draw.rect(surface, shape.color, (sx + j*30 + 25, sy + i*30 + 50, 30, 30), 0)
    surface.blit(label, (sx-20, sy-10))


def draw_five_shapes(shapes, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('NEXT SHAPES', 1, white)
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 300
    surface.blit(label, (sx+15, sy+43))  
    for i in range(5):
        format = shapes[i].shape[shapes[i].rotation % len(shapes[i].shape)]
        for y, line in enumerate(format):
            row = list(line)
            for x, column in enumerate(row):
                if shapes[i].name == "O":
                    if column == "0":
                        pygame.draw.rect(surface, shapes[i].color, (sx + x*30 + 25, sy + y*30 + 100*i + 91, 30, 30), 0)
                elif shapes[i].name == "I":
                    if column == "0":
                        pygame.draw.rect(surface, shapes[i].color, (sx + x*30 + 25, sy + y*30 + 100*i + 76, 30, 30), 0)
                else:
                    if column == '0':
                        pygame.draw.rect(surface, shapes[i].color, (sx + x*30 + 40, sy + y*30 + 100*i + 91, 30, 30), 0)        


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
    
def draw_grid_text(text, size, color, surface):
    pass
    # font = pygame.font.SysFont('comicsans', size, bold=True)
    # label = font.render(text, 1, color)

    # surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))


def draw_window(surface, shape):
    global go
    global leveled_up
    global lines_cleared
    global game_type
    global buffer
    buffer_color = red
    
    gold_list = [red,gold]
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, white)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    if leveled_up or lines_cleared == 4:
        pygame.draw.rect(surface, blue, (top_left_x, top_left_y, play_width, play_height), 5)
    
    if game_type == "classic":
        buffer_color = red
    elif run_time <= 15000:
        buffer_color = blue
    else:
        if buffer > 4:
            buffer_color = green
        elif buffer > 2:
            buffer_color = yellow
        elif buffer == 2:
            buffer_color = red
        elif buffer == 1: 
            if run_time % 500 <= 250:  # blink twice per second
                buffer_color = red
            else:
                buffer_color = (32,32,32)
        else: 
            if run_time % 250 <= 125:  # blink four times per second
                buffer_color = red
            else:
                buffer_color = (32,32,32)
    pygame.draw.rect(surface, buffer_color, (top_left_x, top_left_y, play_width, play_height), 5)
    display_hud(surface, score, total_clears, tetris_rate, gravity, buffer_color)
    if game_type == "classic": display_statistics(surface)

def game_over_grid(locked_positions={}):
    grid = [[white for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
    
def game_over_part_1(grid, locked, win, next_shape):
    for i in locked:
        locked[i] = (255,0,0)                   


def game_over_part_2(grid, locked, win, color, iteration):
    for x in range(10):
        locked[x, iteration] = color
    
    
def get_shape():
    global bag, tetris_shapes, shape_colors, game_type, num_pieces
    if game_type == "classic":
        random_shape = random.choice(bag + [random.choice(bag)])
    else:
        random_shape = random.choice(bag)
        bag.remove(random_shape)
        if len(bag) == 0:
            bag = tetris_shapes.copy()
    get_piece = Piece(6,4, random_shape)
    add_stat(get_piece.name)
    if get_piece.name == "O" or get_piece.name == "I":  
        get_piece.x -= 1
        if get_piece.name == "I": get_piece.y -= 1
    return get_piece #easy_shapes is I and O pieces


def move(current_piece, grid, locked, direction):
    current_piece.x += direction
    grid = create_grid(locked)
    if not valid_space(current_piece, grid):
        current_piece.x -= direction
        return False
    elif current_piece.y == 2:  # This checks that upside down L and J pieces do not exit the grid.
        if current_piece.x == 0 and direction == -1:	# If piece is at top left going left...
            if current_piece.name == "L" and current_piece.rotation % 4 == 1:	#and is an upside down L...
                current_piece.x -= direction	# Don't let it hang off the board
                return False
                
        if current_piece.x == 9 and direction == 1:	# If piece is at top right going right...
            if current_piece.name == "J" and current_piece.rotation % 4 == 3:	#and is an upside down L...
                # Don't let it hang off the board
                current_piece.x -= direction
                return False
    return True

def pause(error=False, is_debug_on=0):   
    paused = True
    if is_debug_on == 0:
        win.fill((0,0,0))
    if error == True:
        draw_text_middle('Error!', 60, orange, win)
    else:
        draw_text_middle('Pause', 60, white, win)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False    
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.display.quit()
                    quit()
                                       
def rotate(current_piece, grid, locked, direction): #direction is -1 or +1
    # print()
    global game_type, left_press, right_press
    global debug_count
    success = False
    debug_count = 0
    x = 0; y = 0
    def attempt_rotation(current_piece, grid, locked, direction, x, y):
        global debug_count
        debug_answer = (current_piece.name,current_piece.rotation%4, "to", (current_piece.rotation+direction)%4, "", x, y)
        debug_count += 1
        current_piece.rotation = current_piece.rotation + direction % len(current_piece.shape)
        current_piece.x += x*direction
        current_piece.y += y*direction
        grid = create_grid(locked)
        if not valid_space(current_piece, grid):
            # print(debug_answer," ", debug_count, False)
            current_piece.y -= y*direction
            current_piece.x -= x*direction
            current_piece.rotation = current_piece.rotation - direction % len(current_piece.shape)
            grid = create_grid(locked)
            return False
        else:
            grid = create_grid(locked)
            # print(debug_answer, " ", debug_count, True)
            return True

    # print("First Attempt")
    success = attempt_rotation(current_piece, grid, locked, direction, 0, 0)
    if success: return True # Universal First attempt (0,0)
    if game_type == "classic": 
        return False #NES does not use wall-kick system
    for i in range(2,6):
        if current_piece.rotation%4 == 0:
            if i == 2:
                if current_piece.name == "I": x = -2; y =  0
                else:                         x = -1; y =  0
            if i == 3:
                if current_piece.name == "I": x =  1; y =  0
                else:                         x = -1; y =  -1
            if i == 4:
                if current_piece.name == "I": x = -2; y = 1
                else:                         x =  0; y = 2
            if i == 5:
                if current_piece.name == "I": x =  1; y =  -2
                else:                         x = -1; y = 2
        if current_piece.rotation%4 == 1:
            if i == 2:
                if current_piece.name == "I": x = -1; y =  0
                else:                         x =  1; y =  0
            if i == 3:
                if current_piece.name == "I": x =  2; y =  0
                else:                         x =  1; y = 1
            if i == 4:
                if current_piece.name == "I": x = -1; y =  -2
                else:                         x =  0; y =  -2
            if i == 5:
                if current_piece.name == "I": x =  2; y = 1
                else:                         x =  1; y =  -2
        if current_piece.rotation%4 == 2:
            if i == 2:
                if current_piece.name == "I": x =  2; y =  0
                else:                         x =  1; y =  0
            if i == 3:
                if current_piece.name == "I": x = -1; y =  0
                else:                         x =  1; y =  -1
            if i == 4:
                if current_piece.name == "I": x =  2; y =  -1
                else:                         x =  0; y = 2
            if i == 5:
                if current_piece.name == "I": x = -1; y = 2
                else:                         x =  1; y = 2
        if current_piece.rotation%4 == 3:
            if i == 2:
                if current_piece.name == "I": x =  1; y =  0
                else:                         x = -1; y =  0
            if i == 3:
                if current_piece.name == "I": x = -2; y =  0
                else:                         x = -1; y = 1
            if i == 4:
                if current_piece.name == "I": x =  1; y = 2
                else:                         x =  0; y =  -2
            if i == 5:
                if current_piece.name == "I": x = -2; y =  -1
                else:                         x = -1; y =  -2
        success = attempt_rotation(current_piece, grid, locked, direction, x, y)
        if success: return True
    return False # Everything failed

def select_level(game):
    global level
    global level_color
    level = 9
    r = 128; g = 0; b = 128
    level_color = yellow
    gravity = gravity_list[level] # Default gravity
    change = False 
    win.fill((0,0,0))
    draw_text_middle(("Level " + "{:02.0f}".format(level)), 60, level_color, win) 
    pygame.display.update()

    while True:
        if change:
            win.fill((0,0,0))
            if level < 2: level_color = violet
            elif level < 5: level_color = blue
            elif level < 8: level_color = green
            elif level < 10: level_color = yellow
            elif level < 13: level_color = orange
            elif level < 16: level_color = pink
            elif level < 19: level_color = red
            elif level < 28: level_color = violet
            else: level_color = white
            
            gravity = gravity_list[level]
            draw_text_middle("Level " + "{:02.0f}".format(level),
                             60, level_color, win)                
            pygame.display.update()
            change = False
        for event in pygame.event.get():
            press = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE
                or event.key == pygame.K_c or event.key == pygame.K_m):
                    change = False
                    return level, gravity
                elif event.key == pygame.K_LEFT:
                    level -= 1
                    change = True
                elif event.key == pygame.K_RIGHT:
                    level += 1
                    change = True
                elif event.key == pygame.K_UP:
                    level += 5
                    change = True
                elif event.key == pygame.K_DOWN:
                    level -= 5
                    change = True
                elif event.key == pygame.K_0: level = 0; change = True
                elif event.key == pygame.K_1: level = 1; change = True
                elif event.key == pygame.K_2: level = 2; change = True
                elif event.key == pygame.K_3: level = 3; change = True
                elif event.key == pygame.K_4: level = 4; change = True
                elif event.key == pygame.K_5: level = 5; change = True
                elif event.key == pygame.K_6: level = 6; change = True
                elif event.key == pygame.K_7: level = 7; change = True
                elif event.key == pygame.K_8: level = 8; change = True
                elif event.key == pygame.K_9: level = 9; change = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    quit()
                if press[pygame.K_LSHIFT] and level + 10 < 20:
                    level += 10
                    change = True
        if game == "modern":
            if level < 1: level = 1
        if level < 0: level = 0
        if level > 29: level = 29

def select_game_type():
    def game_info():
        win.fill(black)
        font = pygame.font.SysFont('comicsans', 40)
        line1 = font.render('Classic Tetris Mode:  pieces are random and', 1, (orange))
        line2 = font.render('floor locking is instant. Moving pieces left and', 1, (orange))
        line3 = font.render('right is slow, and there is no rotation correction.', 1, (orange))
        line4 = font.render('', 1, white)
        line5 = font.render('', 1, white)
        line6 = font.render('Modern Tetris Mode:  Battle rising garbage', 1, blue)
        line7 = font.render('as long as possible. Clear lines to slow it down.', 1, blue)
        line8 = font.render('You have 15 seconds to set up your play field', 1, teal)
        line9 = font.render('before the game begins.  Modern Tetris physics', 1, teal)
        line10 = font.render('apply, including hold piece, random 7-piece bags,', 1, teal)
        line11 = font.render('delayed floor locking, and more.', 1, teal)
        lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11]
        for i in range(len(lines)):
            win.blit(lines[i], 
                         (top_left_x + play_width/2 - 325, 
                          top_left_y + play_height/2 - lines[i].get_height()/2 - 250 + 50*i))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    return
    def draw_state1(cursor):
        win.blit(prompt, (sx - 200, sy - prompt.get_height()/2 - 200))
        win.blit(select1, (sx - 300, sy - select1.get_height()/2))
        win.blit(select2, (sx + 100, sy - select2.get_height()/2))
        if cursor: win.blit(selection, (sx - 350, sy - selection.get_height() + 15))
        pygame.display.update()

    def draw_state2(cursor):
        win.blit(prompt, (sx - 200, sy - prompt.get_height()/2 - 200))
        win.blit(select1, (sx - 300, sy - select1.get_height()/2))
        win.blit(select2, (sx + 100, sy - select2.get_height()/2))
        if cursor: win.blit(selection, (sx + 50, sy - selection.get_height() + 15))
        pygame.display.update()
        
    def confirm(game):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_y or event.key == pygame.K_c 
                        or event.key == pygame.K_m or event.key == pygame.K_SPACE):
                        return True
                    elif event.key == pygame.K_n or event.key == pygame.K_BACKSPACE:
                        return False
    game_info()
    cursor = True    
    win.fill((0,0,0))
    sx = top_left_x + play_width/2
    sy = top_left_y + play_height/2
    font = pygame.font.SysFont('comicsans', 60)
    prompt = font.render('Select Game Type', 1, white)
    select1 = font.render("Classic", 1, white)
    select2 = font.render("Modern", 1, white)
    confirmation = font.render("Confirm? Y/N", 1, (255,128,0))
    selection = font.render(">", 1, (255,0,0))
    
    game = "classic" # Default
    draw_state1(cursor) # Default
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game = "classic"
                    win.fill((0,0,0))
                    draw_state1(cursor)
                elif event.key == pygame.K_RIGHT:
                    game = "modern"
                    win.fill((0,0,0))
                    draw_state2(cursor)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_y or event.key == pygame.K_RETURN:
                    cursor = False
                    win.blit(confirmation, (sx - 150, sy - confirmation.get_height()/2 + 200))
                    if game == "classic":
                        select1 = font.render("Classic", 1, (0,255,0))
                        draw_state1(cursor)
                        if confirm(game) == False:
                            cursor = True
                            select1 = font.render("Classic", 1, white)
                            win.fill((0,0,0))
                            draw_state1(cursor)
                        else: return game
                    elif game == "modern":
                        select2 = font.render("Modern", 1, (0,255,0))
                        draw_state1(cursor)
                        pygame.display.update()
                        if confirm(game) == False:
                            cursor = True
                            select2 = font.render("Modern", 1, white)
                            win.fill((0,0,0))
                            draw_state2(cursor)
                        else: return game
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    quit()
                elif event.key == pygame.K_c:
                    return "classic"
                elif event.key == pygame.K_m:
                    return "modern"

def settings():
    game_type = select_game_type()
    level, gravity = select_level(game_type)
    return level, gravity, game_type

def garbage(grid, locked, prev):
    random_x = random.randint(0,9)
    chosen = random.choice([random_x, random_x, random_x, random_x, prev]) # Give 20% extra chance of prev x location
    # print("Previous Value:", prev,",", "Rolled Value:", random_x, ",", "Selected:", chosen)
    for key in sorted(list(locked), key=lambda x: x[-1]):
        x, y = key
        newKey = (x, y - 1)
        locked[newKey] = locked.pop(key)
    for x in range(10):
        locked[x,19] = white
    locked[chosen, 19] = black
    create_grid(locked)
    return chosen

                
def to_color(color, grid, locked, win, next_shape, pink_row_list):
    for i in range(len(pink_row_list)):
        for x in range(10):
            locked[x, pink_row_list[i]] = (color)

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == 
                           (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True    

def add_stat(shape_name):
    global shape_stats, total_piece_count, most_spawns, least_spawns
    most_spawns = 1
    least_spawns = 0
    spawn_list = list((shape_stats.values()))
    counter_list = []
    total_piece_count += 1
    shape_stats[shape_name]["shape_count"] += 1
    for i in shape_stats:
        shape_stats[i]["percentage"] = (
            int(100 *shape_stats[i]["shape_count"]/total_piece_count)
            )
        if shape_stats[i]["percentage"] == 100:
            shape_stats[i]["percentage"] = 99
    for i in range(7): 
       counter_list.append(spawn_list[i]["shape_count"])
    most_spawns = max(counter_list)
    least_spawns = min(counter_list)
    # print(shape_stats)


#################################################################

def main():
    global gravity
    global fall_time
    global grid
    global score
    global num_pieces
    global green_score
    global total_clears
    global tetris_rate
    global first_hold
    global unlock_hold
    global level
    global leveled_up
    global bag
    global go
    global begin
    global lines_cleared
    global level_color
    global game_type
    global left_press
    global right_press
    global shape_stats
    global total_piece_count
    level, gravity, game_type = settings()
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    change_piece = False
    intervention = False
    run = True
    bag = tetris_shapes.copy()
    fall_time = 0
    begin = True
    go = False
    changed = False
    left_press = False
    right_press = False
    down_press = False
    press_time = 0
    down_press_time = 0
    repeat_time = 0
    enabled = False
    clock = pygame.time.Clock()
    check_level = False
    leveled_up = False
    first_hold = True
    unlock_hold = True
    reset_time = False
    prev = random.randint(0,9)
    shape_stats = {}
    for shape in shape_strings:
        shape_stats[shape] = {"shape_count": 0, "percentage": 0}
    lines_cleared = 0
    green_score = 0
    score = 0
    total_piece_count = 0     # piece total count
    tetris_count = 0
    tetris_rate = 0
    total_clears = 0
    starting_gravity = gravity
    level_gravity = gravity
    lock_time = 0
    movements = 0
    rotations = 0
    starting_level = level
    line_clear_threshold = min((starting_level*10 + 10), max(100, starting_level*10 -50))
    global run_time; run_time = -2000
    global game_time; game_time = -2000
    global buffer; buffer = 5
    global seconds; seconds = 0
    global minutes; minutes = 0
    rows_dropped = 0
    current_piece = get_shape()
    ghost_piece = Piece(current_piece.x, current_piece.y, current_piece.shape)
    hold_piece = current_piece
    switch_piece = hold_piece
    old_color = current_piece.color
    if game_type =="classic":
        shape_list = [get_shape()]
    else:
        shape_list = [get_shape(), get_shape(), get_shape(), 
                    get_shape(), get_shape()]
    old_next_color = shape_list[0].color
    pink_row_list = []
    debug = 0
    # debug_gravity = 1.5
    clear = True

    num_pieces = 0
    while run:
        run_time += clock.get_rawtime()
        game_time += clock.get_rawtime()
        if game_time >= 1000:
            seconds += 1
            game_time = 0
        if seconds == 60:
            minutes += 1
            seconds = 0
        ## Code for repeating
        if game_type == "classic" and (left_press or right_press or down_press):
            if changed and down_press: down_press_time = -.2
            if left_press or right_press: press_time += clock.get_rawtime()
            if down_press: down_press_time += clock.get_rawtime()
            if down_press_time > 400 and down_press: gravity = 1/30
            if press_time > 250:
                repeat_time += clock.get_rawtime()
                if repeat_time >= 100:
                    repeat_time = 0
                    if enabled:
                        if left_press and right_press: 0+0
                        elif left_press: move(current_piece, grid, locked_positions, -1)
                        elif right_press: move(current_piece, grid, locked_positions, 1)
            else:
                repeat_time = 0
                
        if game_type == "modern" and (left_press or right_press or down_press):
            if left_press or right_press: press_time += clock.get_rawtime()
            if down_press: down_press_time += clock.get_rawtime()
            if down_press_time > 400 and down_press: gravity = 1/30
            if press_time > 167:
                repeat_time += clock.get_rawtime()
                if repeat_time >= 33:
                    repeat_time = 0
                    if enabled:
                        if left_press and right_press: 0+0
                        elif left_press:
                            if move(current_piece, grid, locked_positions, -1):
                                movements += 1
                                lock_time = 0
                        elif right_press: 
                            if move(current_piece, grid, locked_positions, 1):
                                movements += 1
                                lock_time = 0
            else:
                repeat_time = 0

        grid = create_grid(locked_positions)
        for event in pygame.event.get(): # Controls
            press = pygame.key.get_pressed()

            if event.type == pygame.QUIT or press[pygame.K_ESCAPE]:
                run = False
                pygame.display.quit()
                quit()
            if press[pygame.K_q]: run = False
            if enabled:
                if event.type == pygame.KEYDOWN:
                    if press[pygame.K_LEFT]:
                        left_press = True
                        if move(current_piece, grid, locked_positions, -1):
                            movements += 1
                            reset_time = True
                    if press[pygame.K_RIGHT]:
                        right_press = True
                        if move(current_piece, grid, locked_positions, 1):
                            movements += 1
                            reset_time = True
                    if press[pygame.K_DOWN]:
                        current_piece.y += 1; down_press = True
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                            if game_type == "modern": change_piece = True
                        score += 1
                    if event.key == pygame.K_UP and game_type == "modern":
                        while (valid_space(current_piece, grid)): 
                            current_piece.y += 1
                        current_piece.y -= 1 
                        change_piece = True
                    if event.key == pygame.K_a:
                        rotate(current_piece, grid, locked_positions, -1)
                        rotations += 1
                        reset_time = True
                    if event.key == pygame.K_s: 
                        rotate(current_piece, grid, locked_positions, 1)
                        rotations += 1
                        reset_time = True
                    if event.key == pygame.K_e and unlock_hold and game_type == "modern":
                        intervention = True; change_piece = True
                    if event.key == pygame.K_p:
                        # print(current_piece.rotation%4, current_piece.x, current_piece.y, level, gravity, total_clears, tetris_rate, check_level)
                        pause(error=False, is_debug_on = debug)
                        fall_time = 0
                    if event.key == pygame.K_BACKSLASH: 
                        debug = (debug + 1) % 2
                        if debug == 1: print("Developer Mode ON")
                        else: print("Developer Mode OFF")
                    if event.key == pygame.K_n and level > 0 and debug:
                        level -= 1
                        if level == 0: gravity = 1.5
                        elif level == 1: gravity == .3815
                        else: gravity += .035
                        starting_gravity = gravity; 
                        # print(level, gravity)
                        total_clears = modern_level_list[level-2]
                    if event.key == pygame.K_m and level < 12 and debug:
                        level += 1
                        if level == 1: gravity = .3815
                        elif level > 1: gravity -= .035
                        total_clears = modern_level_list[level-2]
                        starting_gravity = gravity;
                        # print(level, gravity)
            elif not enabled:
                if event.type == pygame.KEYDOWN:
                    if press[pygame.K_LEFT]:
                        left_press = True
                    if press[pygame.K_RIGHT]:
                        right_press = True
                    if press[pygame.K_DOWN]:
                        down_press = True
            if not press[pygame.K_LEFT]: left_press = False
            if not press[pygame.K_RIGHT]: right_press = False
            if not press[pygame.K_DOWN]: down_press = False
            if not left_press and not right_press: press_time = 0
            if not down_press: down_press_time = 0
            

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        if game_type == "modern":
            current_piece.color = old_color
            changed = False
        if changed:
            gravity = .2
            if not unlock_hold:
                current_piece.color = old_color
            enabled = False
            current_piece.y -= 1
            clock.tick()
            pygame.display.update()
            changed = False
        if begin:
            pygame.display.update()
            gravity = 2
            begin = False
        # PIECE FALLING CODE

        if fall_time/1000 >= gravity:
            if not go or not enabled:
                gravity = level_gravity
                go = True
                enabled = True
            if not down_press:
                gravity = level_gravity
            else:
                score += 1
            current_piece.color = old_color
            shape_list[0].color = old_next_color
            fall_time = 0
            rows_dropped += 1
            # print(rows_dropped, movements, rotations, int(lock_time / 10)/100)
            if rows_dropped > 1:
                movements = 0
                rotations = 0
            # gravity = start_gravity
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                rows_dropped -= 1
                # print(int(fall_time/10)/100)
                if game_type == "classic":
                    changed = True
                    change_piece = True
            else:
                if game_type == "modern":
                    lock_time = 0
        if current_piece.y >= ghost_piece.y:
            rows_dropped = 0
            if reset_time:
                lock_time = 0
                reset_time = False
            # print(int(lock_time/10)/100, rows_dropped, movements, rotations)
            lock_time += clock.get_rawtime()
            if lock_time/1000 >= .5 or rotations > 14 or movements > 14:
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1
                changed = True
                change_piece = True
        else:
            lock_time = 0

        #start ghost piece
        ghost_piece.x = current_piece.x
        ghost_piece.y = current_piece.y
        ghost_piece.shape = current_piece.shape
        ghost_piece.rotation = current_piece.rotation
        while (valid_space(ghost_piece, grid)):
            ghost_piece.y += 1
        ghost_piece.y -= 1
        ghost_pos = convert_shape_format(ghost_piece)
        
        for i in range(len(ghost_pos)):
            x, y = ghost_pos[i]
            (r,g,b) = current_piece.color
            if y > -1:
                try:
                    grid[y][x] = (r/3, g/3, b/3)
                except:
                    print(x,y)
        #end ghost piece

        shape_pos = convert_shape_format(current_piece)
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # IF PIECE HIT GROUND
        if change_piece:
            if intervention:
                clear = False
                current_piece.x = 6; current_piece.y = 4
                current_piece.rotation = 0
                if current_piece.name == "O" or current_piece.name == "I":
                    current_piece.x -= 1
                    if current_piece.name == "I": current_piece.y -= 1
                if first_hold:
                    hold_piece = current_piece
                    hold_piece.rotation = 0     
                    current_piece = shape_list[0]
                    shape_list[0] = shape_list[1]
                    shape_list[1] = shape_list[2]
                    shape_list[2] = shape_list[3]
                    shape_list[3] = shape_list[4]
                    shape_list[4] = get_shape()
                    first_hold = False
                else:
                    switch_piece = current_piece
                    switch_piece.rotation = 0
                    current_piece = hold_piece
                    # current_piece.x = 6; current_piece.y = 4
                    # if current_piece.name == "O" or current_piece.name == "I":
                    #     current_piece.x -= 1
                    #     if current_piece.name == "I": switch_piece.y -= 1 
                    hold_piece = switch_piece
                # intervention = False
                unlock_hold = False
            else:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                # intervention = False
                current_piece = shape_list[0]
                if game_type == "classic":
                    shape_list[0] = get_shape()
                else:
                    shape_list[0] = shape_list[1]
                    shape_list[1] = shape_list[2]
                    shape_list[2] = shape_list[3]
                    shape_list[3] = shape_list[4]
                    shape_list[4] = get_shape()
                unlock_hold = True
            old_color = current_piece.color
            old_next_color = shape_list[0].color
            current_piece.color = invisible
            if game_type == "classic": shape_list[0].color = invisible
            pink_row_list = create_pink_rows(clear, grid, locked_positions, 
                                                win, shape_list[0])
            pink_row_list.sort()
            grid = create_grid(locked_positions)
            lines_cleared += len(pink_row_list)
            clear = True
            if lines_cleared > 0:
                if game_type == "classic":
                    if lines_cleared == 1: green_score = 40 * (level + 1)
                    elif lines_cleared == 2: green_score = 100 * (level + 1)
                    elif lines_cleared == 3: green_score = 300 * (level + 1)
                    else                   : green_score = 1200 * (level + 1)
                else:
                    if lines_cleared == 1: 
                        green_score = 100 * level
                        buffer += 1
                    elif lines_cleared == 2: 
                        green_score = 300 * level
                        buffer += 2
                    elif lines_cleared == 3: 
                        green_score = 500 * level
                        buffer += 4
                    elif lines_cleared == 4: 
                        green_score = 800 * level
                        buffer += 6
                    if buffer > 6:
                        buffer = 6
            else:
                if not intervention:
                    if run_time > 15000:
                        buffer -= 1
                if buffer < 0: 
                    buffer = 0
            # if not intervention: print("Buffer:", buffer) ###############
            for i in range (lines_cleared):
                total_clears += 1
                line_clear_threshold -= 1
                # print(line_clear_threshold)
                if game_type == "classic" or 0==0:
                    if line_clear_threshold <= 0 and total_clears % 10 == 0:
                        leveled_up = True
                        level+=1
                        level_gravity = gravity_list[level]
            if game_type == "classic" or 0==0:
                pygame.display.update()
                if lines_cleared > 0:
                    if leveled_up:
                        to_color((teal), grid, locked_positions, 
                                win, shape_list[0], pink_row_list)
                        grid = create_grid(locked_positions)
                        draw_window(win, -1)
                        draw_next_shape(shape_list[0], win)
                        draw_hold_shape(hold_piece, win)
                        pygame.display.update()          
                    elif lines_cleared == 4:
                        to_color((255,215,0), grid, locked_positions, 
                                win, shape_list[0], pink_row_list)
                        grid = create_grid(locked_positions)
                        draw_window(win, -1)
                        draw_next_shape(shape_list[0], win)
                        draw_hold_shape(hold_piece, win)
                        pygame.display.update()
                    for i in range(3):
                        to_color((1,1,1),grid, locked_positions,
                                            win, shape_list[0], pink_row_list)
                        grid = create_grid(locked_positions)
                        draw_window(win, -1)
                        draw_next_shape(shape_list[0], win)
                        draw_hold_shape(hold_piece, win)                    
                        pygame.display.update()
                        pygame.time.delay(65)
                        if leveled_up:
                            to_color(teal, grid, locked_positions, 
                                win, shape_list[0], pink_row_list)
                        elif lines_cleared == 4: ## gold
                            to_color(gold, grid, locked_positions, 
                                win, shape_list[0], pink_row_list)
                        else:
                            to_color(pink,grid, locked_positions,
                                            win, shape_list[0], pink_row_list)
                        grid = create_grid(locked_positions)
                        draw_window(win, -1)
                        draw_next_shape(shape_list[0], win)
                        draw_hold_shape(hold_piece, win)
                        pygame.display.update()
                        pygame.time.delay(65)
                    to_color(gold, grid, locked_positions,
                                win, shape_list[0], pink_row_list)
                elif (game_type == "modern" and not intervention 
                      and run_time > 15000 and buffer == 0):
                    prev = garbage(grid, locked_positions, prev)
            for i in range(lines_cleared):
                clear_rows(grid, locked_positions, pink_row_list[i])
                grid = create_grid(locked_positions)
                if game_type == "classic" or 0==0: 
                    pygame.time.delay(100)
                ## score
                if lines_cleared == 1:
                    if game_type == "classic":
                        score += 40 * (level + 1)
                    else:
                        score += 100 * level
                    green_score = 0
                elif lines_cleared == 2:
                    if game_type == "classic":
                        score += 50 * (level + 1)
                        green_score -= 50 * (level + 1)
                    else:
                        score += 150 * level
                        green_score -= 150 * level
                elif lines_cleared == 3:
                    if game_type == "classic":
                        score += 100 * (level + 1)
                        green_score -= 100 * (level + 1)
                    else:
                        score += 167 * level
                        green_score -= 167 * level
                        if i==2:
                            score -= 1 * level
                            green_score += 1 * level
                elif lines_cleared == 4:   
                    if game_type == "classic":
                        score += 300 * (level + 1)
                        tetris_count += 1
                        green_score -= 300 * (level + 1)
                    else:
                        score += 200*level
                        green_score -= 200*level
                tetris_rate = (tetris_count/total_clears) * 100
                draw_window(win, -1)
                draw_next_shape(shape_list[0], win)
                draw_hold_shape(hold_piece, win)
                pygame.display.update()
            lines_cleared = 0
            intervention = False
            changed = True
            change_piece = False
            if green_score <= 0: leveled_up = False
            fall_time = 0
            lock_time = 0
            movements = 0
            rotations = 0
        draw_window(win, current_piece)
        if game_type == "classic": 
            draw_next_shape(shape_list[0], win)
        else:
            draw_five_shapes(shape_list, win)
        draw_hold_shape(hold_piece, win)
        pygame.display.update()
        
       

        # Check if user lost
        if check_lost(locked_positions):
            enabled = False
            run = False
            pygame.time.delay(200)
            grid = game_over_grid(locked_positions)
            draw_window(win, current_piece)
            draw_next_shape(shape_list[0], win)
            draw_hold_shape(hold_piece, win)
            pygame.display.update()
            pygame.time.delay(800)            
            for i in range(20,-1,-1):
                game_over_part_2(grid, locked_positions, win, old_color, i)
                grid = game_over_grid(locked_positions)
                draw_window(win, current_piece)
                draw_next_shape(shape_list[0], win)
                draw_hold_shape(hold_piece, win)
                pygame.display.update()
                pygame.time.delay(33)
            
            grid = create_grid(locked_positions)
            draw_window(win, current_piece)
            draw_next_shape(shape_list[0], win)
            draw_hold_shape(hold_piece, win)
            pygame.display.update()
            pygame.time.delay(200)
            draw_text_middle("Final Score: " + str(int(score)), 40, white, win)
            # print(score)
            pygame.display.update()
            pygame.time.delay(2000)
            enabled = True
        
    
def main_menu():
    try:
        run = True
        while run:
            win.fill((0,0,0))
            font = pygame.font.SysFont('comicsans', 60)
            line1 = font.render('A -- Rotate Counterclockwise', 1, white)
            line2 = font.render('S -- Rotate Clockwise', 1, white)
            line3 = font.render('E -- Hold/Exchange Piece', 1, white)
            line4 = font.render('P -- Pause', 1, white)
            line5 = font.render('Press any key to continue.', 1, white)
            lines = [line1, line2, line3, line4, line5]
            for i in range(len(lines)):
                win.blit(lines[i], 
                             (top_left_x + play_width/2 - 300, 
                              top_left_y + play_height/2 - lines[i].get_height()/2 - 200 + 100*i))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        pygame.display.quit()
                        quit()
                    else:
                        # print("new game")
                        main()
        pygame.quit()
    except:
        str(traceback.print_exc())
        try:
            pause(error = True, is_debug_on = 1)
        except:
            run = False
            pygame.display.quit()
            pygame.quit()
        


win = pygame.display.set_mode((s_width, s_height + 70))
pygame.display.set_caption('Tetris')
main_menu()  # start game   