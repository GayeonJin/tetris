#!/usr/bin/python

import sys

import pygame
import random

from gresource import *
from gobject import *

MAX_ROWS = 20
MAX_COLS = 12

BOARD_XOFFSET = 10
BOARD_YOFFSET = 30

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30

SOUND = False

debug_ctrl = {
    'check_area' : True,
    'remove' : True,
    'move_down' : True,
}

block_data = [
    [2, 0, [(0, 0), (1, 0), (2, 0), (3, 0)], COLOR_RED],
    [1, 0, [(0, 0), (1, 0), (1, 1), (0, 1)], COLOR_BLUE],
    [1, 0, [(0, 0), (1, 0), (2, 0), (2, 1)], COLOR_YELLOW],
    [1, 0, [(0, 1), (0, 0), (1, 0), (2, 0)], COLOR_ORANGE],
    [1, 0, [(0, 0), (1, 0), (1, 1), (2, 1)], COLOR_GREEN],
    [1, 0, [(0, 1), (1, 1), (1, 0), (2, 0)], COLOR_MAGENTA],
    [1, 0, [(0, 1), (1, 1), (2, 1), (1, 0)], COLOR_PURPLE],                        
]

class block_object :
    def __init__(self, rows, cols) :
        self.datum = []
        
        id = random.randrange(0, len(block_data))
        self.center_x = block_data[id][0]
        self.center_y = block_data[id][1]
        for (x, y) in block_data[id][2] :
            self.datum.append((x, y))
        self.color = block_data[id][3]

        self.rows = rows
        self.cols = cols

        # move center
        x = int(self.cols / 2 - self.center_x)
        self.move_right(None, x) 

    def rotate_right(self, board) :
        next_block = []

        for i, (x, y) in enumerate(self.datum) :
            # rotation matrix (90 deg)
            x1 = -(y - self.center_y) + self.center_x
            y1 = (x - self.center_x) + self.center_y
            
            if x1 < 0 or x1 >= self.cols :
                return False
            
            if y1 < 0 or y1 >= self.rows :
                return False 
             
            next_block.append((x1, y1))

        if self.update_block(next_block, board) == False :
            return False
      
        return True

    def move_left(self, board, movement = 1) :
        next_block = []

        for (x, y) in self.datum :
            if x == 0 :
                return
                    
        for i, (x, y) in enumerate(self.datum) :
            x -= movement
            next_block.append((x, y))

        if self.update_block(next_block, board) == False :
            return False

        self.center_x -= movement
        return True

    def move_right(self, board, movement = 1) :
        next_block = []

        for (x, y) in self.datum :
            if x == self.cols - 1 :
                return
                    
        for i, (x, y) in enumerate(self.datum) :
            x += movement
            next_block.append((x, y))

        if self.update_block(next_block, board) == False :
            return False

        self.center_x += movement
        return True
        
    def move_down(self, board) :
        next_block = []

        for (x, y) in self.datum :
            if y == self.rows - 1 :
                return False
                    
        for i, (x, y) in enumerate(self.datum) :
            y += 1
            next_block.append((x, y))

        if self.update_block(next_block, board) == False :
            return False
        
        self.center_y += 1        
        return True

    def check_gameover(self, board) :
        return self.check_conflict(self.datum, board)

    def check_conflict(self, datum, board) :
        conflict = False

        for (x, y) in datum :
            if board.map[x][y] != 0 :
                conflict = True
                break
        
        return conflict

    def update_block(self, next_block, board) :
        if board != None :
            if self.check_conflict(next_block, board) == True :
                return False

        for i, (x, y) in enumerate(next_block) :
            self.datum[i] = (x, y)   

        return True     

    def draw(self, board) :
        for i, (x, y) in enumerate(self.datum) :        
            if x != -1 and y != -1 :
                rect = board.get_map_rect(x, y)
                pygame.draw.rect(gctrl.gamepad, self.color, rect, 0, 1)
                pygame.draw.rect(gctrl.gamepad, COLOR_WHITE, rect, 1, 1)

class game_board :
    def __init__(self, rows, cols) :
        self.map = []

        self.rows = rows
        self.cols = cols
        
        for x in range(cols) :
            self.map.append([])
            for y in range(rows) :
                self.map[x].append(0)

        self.x_offset = BOARD_XOFFSET
        self.y_offset = BOARD_YOFFSET
        self.obj_width = BLOCK_WIDTH
        self.obj_height = BLOCK_HEIGHT

        self.score = 0

        # effect resource
        self.effect_boot = pygame.image.load(get_img_resource('id_boom'))

        # sound resource
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))

    def clear(self) :
        for x in range(self.cols) :
            for y in range(self.rows) :
                self.map[x][y] = 0

        self.score = 0

    def get_size(self) :
        return self.rows, self.cols

    def get_padsize(self) :
        pad_width = 2 * self.x_offset + self.cols * self.obj_width 
        pad_height = 2 * self.y_offset + self.rows * self.obj_height
        return (pad_width, pad_height) 

    def get_pos(self, screen_xy) :
        for y in range(self.rows) :
            for x in range(self.cols) :
                rect = self.get_map_rect(x, y)
                if screen_xy[0] > rect.left and screen_xy[0] < rect.right :
                    if screen_xy[1] > rect.top and screen_xy[1] < rect.bottom :      
                        return (x, y)
                    
        return (None, None)

    def get_map_rect(self, x, y) :
        rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width , self.obj_height)

        # map[0][0] is left and top
        rect.x += x * self.obj_width
        rect.y += y * self.obj_height  
        return rect        
    
    def fill_block(self, block) :
        rows = []

        for (x, y) in block.datum :
            self.map[x][y] = block.color

            if y not in rows :
                rows.append(y)
        return rows

    def check_full(self, rows = None) :
        if rows == None :
            rows = range(self.rows)

        erase_rows = []
        for y in rows :
            count = 0
            for x in range(self.cols) :
                if self.map[x][y] != 0 :
                    count += 1

            if count == self.cols :
                erase_rows.append(y)

        return erase_rows

    def remove(self, rows) :
        for row in rows :
            for x in range(self.cols) :
                self.map[x][row] = 0
       
    def move_down_all(self, rows) :
        for row in rows :
            for y in range(row, 0, -1) :
                for x in range(self.cols) :
                    self.map[x][y] = self.map[x][y-1]

    def move_down(self) :
        for x in range(self.cols) :        
            empty_y = []
            for y in range(self.rows-1, -1, -1) :
                if self.map[x][y] == 0 :
                    empty_y.append(y)
                else :
                    if len(empty_y) > 0 :
                        y1 = empty_y.pop(0)
                        self.map[x][y1] = self.map[x][y]
                        self.map[x][y] = 0
                        empty_y.append(y)

    def draw(self) :
        rect = pygame.Rect(self.x_offset, self.y_offset, self.obj_width, self.obj_height)

        # map[0][0] is left and top
        for y in range(self.rows) :
            for x in range(self.cols) :
                if self.map[x][y] != 0 :
                    pygame.draw.rect(gctrl.gamepad, self.map[x][y], rect, 0, 1)
                else :
                    pygame.draw.rect(gctrl.gamepad, COLOR_GRAY, rect, 0, 1)
                
                pygame.draw.rect(gctrl.gamepad, COLOR_WHITE, rect, 1, 1)

                rect.x += self.obj_width
            rect.y += self.obj_height
            rect.x = self.x_offset

if __name__ == '__main__' :
    print('game board object')
