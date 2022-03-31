#-*-coding:utf-8 -*-
import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# Variables
s_width = 800
s_height = 700
play_width = 300  # 300 // 10 = 30 de largeur par bloc
play_height = 600  # 600 // 20 = 20 de hauteur par bloc
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# Formats briques
S = [['.....',
    '......',
    '..00..',
    '.00...',
    '.....' 
    ],

    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....'
    ]]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],

    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],

    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],

    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],

    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],

    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],

    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],

    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],

    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],

    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],

    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],

    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

# Briques et couleurs briques
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(20, 235, 20), (235, 20, 20), (20, 235, 235), (235, 20, 20), (235, 165, 20), (20, 20, 235), (128, 20, 128)]


# Classe Pièce
class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # nombre de 0 à 3


# Grille
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


# Forme de la brique
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


# Validation brique
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
        
    return False


# Nouvelle brique
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


# Texte
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))


# Grille
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    
    for i in range(row):
        pygame.draw.line(surface, (58,58,58), (sx, sy + i*30), (sx + play_width, sy + i * 30)) # lignes horizontales
        for j in range(col):
            pygame.draw.line(surface, (58,58,58), (sx + j * 30, sy), (sx + j * 30, sy + play_height)) # lignes verticales


# Effacement ligne(s) (toutes les cases de la (ou les) ligne(s) sont occupées).
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # position verrouillée
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    # Textes
    font = pygame.font.SysFont('comicsans', 20)
    font2 = pygame.font.SysFont('comicsans', 30)
    font3 = pygame.font.SysFont('comicsans', 25)
    label = font3.render('Prochaine brique', 1, (235,235,235))
    label2 = font2.render('Touches', 1, (235,235,235))
    label3 = font.render('< > : déplacement', 1, (235,235,235))
    label4 = font.render('^ : rotation', 1, (235,235,235))
    label5 = font.render('Espace : bas', 1, (235,235,235))

    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx, sy - 40))
    surface.blit(label2, (sx - 520, sy - 60))
    surface.blit(label3, (sx - 540, sy - 10))
    surface.blit(label4, (sx - 530, sy + 30))
    surface.blit(label5, (sx - 530, sy + 70))
    

def draw_window(surface):
    surface.fill((0,0,0))
    # titre TETRIS
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (235,235,235))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 25))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # dessin grille et bordure
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (25, 30, 140), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()


def main():
    global grid

    locked_positions = {}  # (x,y):(235,20,20)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.4 # vitesse déplacement vers le bas briques

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Progression de la brique
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            # Touches
            if event.type == pygame.KEYDOWN:
                
                # Touche gauche
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                # Touche droite
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                        
                # Touche haut
                elif event.key == pygame.K_UP:
                    # Rotation brique
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                # Touche bas
                if event.key == pygame.K_DOWN:
                    # Accentuation de la pièce vers le bas
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                # Touche espace
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    print(convert_shape_format(current_piece)) # todo fix

        shape_pos = convert_shape_format(current_piece)

        # Ajout pièce à la grille pour dessin
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Quand la pièce atteint la base
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Si le joueur a perdu
        if check_lost(locked_positions):
            run = False

    draw_text_middle("Tu as perdu !", 40, (235,235,235), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Tapez sur une touche pour commencer.', 40, (235, 235, 235), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
    

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu() # début jeu

