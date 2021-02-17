# coding=utf-8

# version 1.0.0
# Sudoku generation and resolution by some methods
# Does not work yet
# 

import pygame as pg, threading as threading
from copy import deepcopy

pg.init()
screensize = 750,750
screen = pg.display.set_mode(screensize)
font = pg.font.SysFont(None,80)


def cmd():
    while True:
        x = input("r c n> ")
        x = x.split(' ')
        for i in x:
            if int(i) < 1 or int(i) > 9:
                print("Invalid number.")
                pass
        put_number(int(x[0])-1,int(x[1])-1,int(x[2]))
        blacklist.clear()

threading.Thread(target = cmd).start()


base_grid = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 0 free | 1 wrong | 2 lock
rule_grid = [    
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

number_grid = deepcopy(base_grid)


def put_number(row,col,number):
    if number < 1 or number > 9:
        print("Invalid number.")
        return

    if rule_grid[row][col] == 2:
        print(base_grid[row][col])
        print("This number cannot be changed.")
        return

    number_grid[row][col] = number
    checknumber(row,col,number)

    #3n_text = font.render(str(number), True, pg.Color('Black'))
    #screen.blit(n_text, pg.Vector2((col*80)+40, (row*80)+33))

blacklist=[]
def checknumber(row,col,number):
    ver = 0
    ver_grid = []
    ver_grid.clear()
    blacklist.append([row,col])
    for i in range(0,9):

        if number_grid[row][i] == number:
            if i != col:
                ver =  1
            rule_grid[row][i] = 1
            rule_grid[row][col] = 1
            if [row,i] not in blacklist:
                ver_grid.append([row,i])

        if number_grid[i][col] == number:
            if i != row:
                ver = 1
            rule_grid[i][col] = 1
            rule_grid[row][col] = 1
            if [i,col] not in blacklist:
                ver_grid.append([i,col])

    if ver == 0:
        rule_grid[row][col] = 0
    
    if len(ver_grid) != 0:
        for a,b in ver_grid:
            print(a,b,number_grid[a][b])
            checknumber(a,b,number_grid[a][b])
    

def draw_background():
    screen.fill(pg.Color("White"))
    
    i = 1
    while (i * 80) < 720:
        if(i%3)>0:
            line_width = 5 
            line_color = pg.Color("Black")
            pg.draw.line(screen, line_color, pg.Vector2((i*80)+15, 15), pg.Vector2((i*80)+15, 735),line_width)
            pg.draw.line(screen, line_color, pg.Vector2(15, (i*80)+15), pg.Vector2(735, (i*80)+15),line_width)
            i+=1
        else:
            i+=1
    i=3
    while (i * 80) < 720:
        line_width = 10
        line_color = pg.Color("Blue")
        pg.draw.line(screen, line_color, pg.Vector2((i*80)+15, 15), pg.Vector2((i*80)+15, 735),line_width)
        pg.draw.line(screen, line_color, pg.Vector2(15, (i*80)+15), pg.Vector2(735, (i*80)+15),line_width)
        i+=3
    pg.draw.rect(screen, pg.Color("Black"), pg.Rect(15, 15,720,720),10)


def draw_base():
    row = 0
    while row < 9:
        col = 0

        while col <9:
            output = number_grid[row][col]
            
            if (rule_grid[row][col] == 2):
                textcolor = pg.Color("Blue") 
            elif (rule_grid[row][col] == 1):
                textcolor = pg.Color("Red")
            elif (rule_grid[row][col] == 0):
                textcolor = pg.Color("Black")
            else:
                print("Rule error")
                return

            if (output != 0):
                n_text = font.render(str(output), True, textcolor)
                screen.blit(n_text, pg.Vector2((col*80)+40, (row*80)+33))
            col +=1

        row +=1


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT: exit()
    
    draw_background()
    draw_base()
    pg.display.flip()

while 1:
    game_loop()
