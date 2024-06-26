
def square (r, c):
    if r <= 2 and c <= 2:
        R = 0
        C = 0
        B = 0
    elif r <= 2 and (c > 2 and c <= 5):
        R = 0
        C = size // 3
        B = 1
    elif r <= 2 and c > 5:
        R = 0 
        C = (size // 3)*2
        B = 2
    elif (r > 2 and r <= 5) and c <= 2:
        R = size // 3
        C = 0
        B = 3
    elif (r > 2 and r <= 5) and (c > 2 and c <= 5):
        R = size // 3 
        C = size // 3
        B = 4
    elif (r > 2 and r <= 5) and c > 5:
        R = size // 3
        C = (size // 3)*2
        B = 5
    elif r > 5 and c <= 2:
        R = (size // 3)*2
        C = 0
        B = 6
    elif r > 5 and (c > 2 and c <= 5):
        R = (size // 3)*2
        C = size // 3
        B = 7
    elif r > 5 and c > 5:
        R = (size // 3)*2
        C = (size // 3)*2
        B = 8
    return R, C, B

class Grid:
    def __init__ (self, grid):
        self.grid = grid

    def is_full (self):         #vrátí False, jestli existuje nevyplněné pole. Vrátí True, pokud je tabulka plně vyplněná
        for row in range (size):
            for col in range (size):
                if self.grid[row][col] < 0:
                    return False
        return True
    
    
size = 9
REPEAT_CONS = 5000
g = [0]*size
for i in range (size):
    g[i] = [-1]*size 
g = Grid(g)

DIFF_CONST = 10         #konstanta při určení volných míst pro tabuku dané obtížnosti
dif_input = int(input("CHOOSE DIFFICULTY (1-5): "))  #určení obtížnosti -> 1 až 5

class TimeError(Exception):
    "raised when given data takes too long to process"
    pass

while True:
    try:
        values_rows = [0]*size      #tabulka, kde pro každý řádek je inverzní pole označující hodnoty, které se v řádku ještě nevyskytují
        for j in range (size):      
            values_rows[j] = [True]*(size + 1)      #index = vhodná hodnota 

        values_cols = [0]*size
        for k in range (size):
            values_cols[k] = [True]*(size + 1)

        values_boxes = [0]*size     #pro čtverce, kde jsou seřazeny - levý horní roh až pravý horní roh, prostřední pás zleva do prava a stejně i dolní pás
        for l in range (size):
            values_boxes[l] = [True]*(size + 1)

        import random
        def random_list (start, end): #vrací seznam hodnot od start do end (oba včetně) v náhodném pořadí
            l = [None]*(end - start + 1)
            for index in range (len(l)):
                n = random.randint(start, end)
                while n in l:
                    n = random.randint(start, end)
                l[index] = n
            return l

        from collections import deque
        list_rows = random_list(0,size-1).copy()
        list_cols = random_list(0,size-1).copy()
        a = [(i,j) for i in list_rows for j in list_cols]
        empty_spaces = deque(a)

        values = random_list(1,9).copy()

        count = 0                      
        repeat = 0
        def solve (wanted_sol):       #vrátí True, pokud našla tolik řešení, kolik bylo požadováno. Proměnná g potom je jedním z řešeních. Pokud neexistuje funkce skončí a vypíše False, proměnná g je původní tabulka.    #wanted_sol - kolik řešení chci, aby funkce určila 
            global g, values_rows, values_cols, values_boxes, empty_spaces, count, repeat
            repeat += 1
            if repeat > REPEAT_CONS:
                raise TimeError
            if len(empty_spaces) == 0:
                return
            r, c = empty_spaces.popleft()
            empty_spaces.appendleft((r,c))
            for value in values:
                _, z, b = square (r,c)
                if values_rows[r][value] and values_cols[c][value] and values_boxes[b][value]:
                    g.grid[r][c] = value
                    values_rows[r][value] = False
                    values_cols[c][value] = False
                    values_boxes[b][value] = False
                    empty_spaces.popleft()
                    if len(empty_spaces) == 0:
                        count += 1
                        if wanted_sol == count:
                            return True
                    else:
                        if solve(wanted_sol):
                            return True
                    g.grid[r][c] = -1
                    values_rows[r][value] = True
                    values_cols[c][value] = True
                    values_boxes[b][value] = True
                    empty_spaces.appendleft((r,c))
            return False

        def generate():
            global g, count, values_rows, values_cols, values_boxes, empty_spaces
            solve(1)
            count = 0
            solution = [[0]*size for _ in range (size)]
            for i in range (size):
                for j in range (size):
                    solution [i][j] = g.grid[i][j]
            difficulty_value = random.randint(((DIFF_CONST*dif_input) + 1), (DIFF_CONST*dif_input) + 10)
            emptied = 0
            while emptied < difficulty_value:
                row = random.randint(0, size-1)
                col = random.randint(0, size-1)
                if g.grid[row][col] > 0:
                    hold = g.grid[row][col]
                    hold_grid = [[0]*size for _ in range (size)]
                    for i in range (size):
                        for j in range (size):
                            hold_grid [i][j] = g.grid[i][j]
                    hold_empty_spaces = (list(empty_spaces)).copy()
                    hold_values_rows = values_rows.copy()
                    hold_values_cols = values_cols.copy()
                    hold_values_boxes = values_boxes.copy()
                    g.grid[row][col] = -1
                    empty_spaces.appendleft((row, col))
                    _, xz, box = square(row, col)
                    values_rows[row][hold] = True
                    values_cols[col][hold] = True
                    values_boxes[box][hold] = True
                    if not solve(2):
                        emptied += 1
                    else:
                        g.grid = hold_grid
                        empty_spaces = deque(hold_empty_spaces)
                        values_rows = hold_values_rows
                        values_cols = hold_values_cols
                        values_boxes = hold_values_boxes
                    count = 0
            return(solution)

        sol = generate()
        break
    except TimeError:
        pass

g_grid_copy = [[0]*size for _ in range (size)]
for i in range (size):
    for j in range (size):
        g_grid_copy [i][j] = g.grid[i][j]

import pygame
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font2 = pygame.font.Font('freesansbold.ttf', 25)
font3 = pygame.font.Font('freesansbold.ttf', 17)

def draw_grid(grid_d):
    for i in range (1, 11):
        if (i - 1) % 3 == 0:
            width = 2
        else:
            width = 1
        pygame.draw.line(screen, (0,0,0), pygame.math.Vector2(50, 50*i), pygame.math.Vector2(500, 50*i), width)
        pygame.draw.line(screen, (0,0,0), pygame.math.Vector2(50*i, 50), pygame.math.Vector2(50*i, 500), width)
        for i in range (len(grid_d)):
            for j in range (len(grid_d)):
                num = grid_d[i][j]
                if num > 0:
                    text_num = font2.render(str(num), True, (0, 0, 255))
                    screen.blit(text_num ,pygame.Rect(50*(j + 1) + 20, 50*(i + 1) + 15, 50, 50))

        for i in range (len(g_grid_copy)):
            for j in range (len(g_grid_copy)):
                num = g_grid_copy[i][j]
                if num > 0:
                    text_num = font2.render(str(num), True, (0, 0, 0))
                    screen.blit(text_num ,pygame.Rect(50*(j + 1) + 20, 50*(i + 1) + 15, 50, 50))
                

def draw_button():
    BORDER_WIDTH = 3
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(508 - BORDER_WIDTH, 500 - BORDER_WIDTH, 72 + 2*BORDER_WIDTH, 28 + 2*BORDER_WIDTH))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(508, 500, 72, 28))
    text_border = font3.render("CHECK", True, (255, 255, 255))
    screen.blit(text_border,pygame.Rect(513, 505, 10, 10))

def insert(screen, position):
    global g
    i, j = position[1], position[0]     # nabývají hodnot 0-8 
    width = 2
    if g_grid_copy [i][j] > 0:
        return
    pygame.draw.line(screen, (0,255,0), pygame.math.Vector2(50*(j+1), 50*(i+1)), pygame.math.Vector2(50*(j+2), 50*(i+1)), width)
    pygame.draw.line(screen, (0,255,0), pygame.math.Vector2(50*(j+1), 50*(i+2)), pygame.math.Vector2(50*(j+2), 50*(i+2)), width)
    pygame.draw.line(screen, (0,255,0), pygame.math.Vector2(50*(j+1), 50*(i+1)), pygame.math.Vector2(50*(j+1), 50*(i+2)), width)
    pygame.draw.line(screen, (0,255,0), pygame.math.Vector2(50*(j+2), 50*(i+1)), pygame.math.Vector2(50*(j+2), 50*(i+2)), width)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                return
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_BACKSPACE):
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(50*(j + 1) + 5, 50*(i + 1) + 5, 45, 45))
                    g.grid[i][j] = -1
                    pygame.display.update()
                    return
                if (event.key - 48) >= 1 and (event.key - 48) < 10 :
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(50*(j + 1) + 5, 50*(i + 1) + 5, 45, 45))
                    text = font2.render(str(event.key - 48), True, (0, 50, 255))
                    screen.blit(text ,pygame.Rect(50*(j + 1) + 20, 50*(i + 1) + 15, 50, 50))
                    g.grid[i][j] = event.key - 48
                    pygame.display.update()
                return

def check(screen):
    global g
    font_end = pygame.font.Font('freesansbold.ttf', 25)
    if not g.is_full():
        return
    if g.grid == sol:
        BORDER_WIDTH = 3
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10 - BORDER_WIDTH, 225 - BORDER_WIDTH , 582 + 2*BORDER_WIDTH ,50 + 2*BORDER_WIDTH))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 225 , 582 ,50))
        text_correct = font_end.render("CONGRATULATIONS, THAT IS CORRECT!", True, (0, 0, 0))
        screen.blit(text_correct,pygame.Rect(50, 238 ,590 , 50))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
    else:
        BORDER_WIDTH = 3
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10 - BORDER_WIDTH, 225 - BORDER_WIDTH , 582 + 2*BORDER_WIDTH ,50 + 2*BORDER_WIDTH))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 225 , 582 ,50))
        text_wrong = font_end.render("THAT IS NOT CORRECT!", True, (0, 0, 0))
        screen.blit(text_wrong,pygame.Rect(145, 238 ,590 , 50))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(210 - BORDER_WIDTH, 300 - BORDER_WIDTH, 160 + 2*BORDER_WIDTH, 30 + 2*BORDER_WIDTH))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(210, 300, 160, 30))
        text_try = font3.render("TRY AGAIN", True, (0, 0, 0))
        screen.blit(text_try,pygame.Rect(241, 307, 20, 30))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(210 - BORDER_WIDTH, 350 - BORDER_WIDTH, 160 + 2*BORDER_WIDTH, 30 + 2*BORDER_WIDTH))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(210, 350, 160, 30))
        text_try = font3.render("RESUME", True, (0, 0, 0))
        screen.blit(text_try,pygame.Rect(252, 357, 20, 30))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos1, pos2 = pygame.mouse.get_pos()
                    if pos1 > 210 and pos1 < 370 and pos2 > 300 and pos2 < 330:
                        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(1, 1, 600, 550))
                        for i in range (size):
                            for j in range (size):
                                g.grid [i][j] = g_grid_copy[i][j]
                        draw_grid(g.grid)
                        draw_button()
                        pygame.display.update()
                    if pos1 > 210 and pos1 < 370 and pos2 > 350 and pos2 < 380:
                        return
                    return


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos1, pos2 = pygame.mouse.get_pos()
            pos = ((pos1 // 50) - 1, (pos2 // 50) - 1)
            if pos1 > 508 and pos1 < 780 and pos2 > 500 and pos2 < 528:
                check(screen)
            if pos[0] >= 0 and pos[0] < 9 and pos[1] >= 0 and pos[1] < 9:
                insert(screen, pos)
                
    screen.fill((255,255,255))

    draw_grid(g.grid)
    draw_button()


    pygame.display.flip()


pygame.quit()
