# coding=utf-8

# version 1.0.0
# Sudoku generation and resolution by some methods
# Does not work yet v2
# 

import pygame as pg, threading as threading
from copy import deepcopy
from numpy import array,delete, argwhere as where

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



        put_number(int(x[0])-1,int(x[1])-1,int(x[2]))
        blacklist.clear()

threading.Thread(target = cmd).start()

#generated grid
base_grid = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# 0 free | 1 ROW WRONG | 3 COL WRONG | 5 GROUP WRONG | 10 LOCKED
rule_grid = [    
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#group 3x3 grid
group_grid = [
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
]

group_grid = array(group_grid)
number_grid = deepcopy(base_grid)
number_grid = array(number_grid)


def put_number(row,col,number):
    
    if number < 1 or number > 9:
        print("Invalid number.")
        return

    if rule_grid[row][col] == 2:
        print(base_grid[row][col])
        print("This number cannot be changed.")
        return

    old_number = number_grid[row][col]
    number_grid[row][col] = number
    
    if number_grid[row][col] == old_number:
        return
    else:
        checknumber(row,col,old_number,sub=False)
    

blacklist=[] # 0 free | 1 ROW WRONG | 3 COL WRONG | 5 GROUP WRONG | 10 LOCKED
             #           [1,4,6,9]     [3,4,8,9]       [5,6,8,9]
             
def checknumber(row,col,old_number=0,sub=False):  #All types of number-check
    print("Checking: ",row,col)
    samenumber = where(number_grid == number_grid[row][col])

    if len(samenumber) == 1 and rule_grid[row][col] == 0:
        return

    x = 0
    y = []
    for A,B in samenumber:
        if A != row and B!=col or rule_grid[A][B] == 10:
            y.append(x)
        x +=1
    samenumber = delete(samenumber,y,0)

    rows_sn = samenumber[:, 0]
    columns_sn = samenumber[:, 1]

    if len(rows_sn) > 1 and rule_grid[row][col] not in [1,4,6,9]:
        rule_grid[row][col] += 1
    
    elif len(rows_sn) == 1 and rule_grid[row][col] in [1,4,6,9]:
        rule_grid[row][col] -= 1

    if len(columns_sn) > 1 and rule_grid[row][col] not in [3,4,8,9]:
        rule_grid[row][col] += 3

    elif len(columns_sn) == 1 and rule_grid[row][col] in [3,4,8,9]:
        rule_grid[row][col] -= 3

    blacklist.append([row,col])
    
    if rule_grid[row][col] != 0:
        for A,B in samenumber:
            if A == row and B == col:
                pass
            elif [A,B] not in blacklist:
                checknumber(A,B,sub=True)

    if old_number != 0:
        print("Test")
        oldnumber_array = where(number_grid == old_number)

        y.clear()2 
        x=0
        for A,B in oldnumber_array:
            if A != row and B!=col or rule_grid[A][B] == 10:
                y.append(x)
            x +=1
        oldnumber_array = delete(oldnumber_array,y,0)

        for A,B in oldnumber_array:
            if A == row and B == col:
                pass
            elif [A,B] not in blacklist:
                checknumber(A,B,sub=True)
    
        
            


   
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
            
            if (rule_grid[row][col] == 10):
                textcolor = pg.Color("Blue") 
            elif (rule_grid[row][col] > 0 and rule_grid[row][col] < 10):
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
