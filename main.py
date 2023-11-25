#!/usr/bin/python

import os
import sys

import pygame
import random
from time import sleep

from gresource import *

from board import *

TITLE_STR = 'Tetris'

STATE_IDLE = 0
STATE_CHECK_ALL = 1
STATE_REMOVE = 2
STATE_MOVE_DOWN = 3

DOWN_SPEED = 20

NEXT_BLOCK_WIDTH = 30*5

def draw_score(score) :
    gctrl.draw_string("Score : " + str(score), BOARD_XOFFSET, 10, ALIGN_LEFT, 25, COLOR_BLACK)

def draw_message(str) :
    gctrl.draw_string(str, 0, 0, ALIGN_CENTER, 40, COLOR_BLACK)

    pygame.display.update()
    sleep(2)

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global clock
    global board

    state = STATE_IDLE
    board.clear()

    block = block_object(board.rows, board.cols)
    block.move_start()
    next_block = block_object(board.rows, board.cols)

    tick = 0
    block_down = False
    game_exit = False
    while not game_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                game_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    block.rotate_right(board)
                if event.key == pygame.K_DOWN :
                    block_down = True
                elif event.key == pygame.K_LEFT :
                    block.move_left(board) 
                elif event.key == pygame.K_RIGHT :
                    block.move_right(board)
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)
                elif event.key == pygame.K_x :
                    return

        if state == STATE_CHECK_ALL :
            # clear item and make effect
            remove_rows = board.check_full()
            if len(remove_rows) > 0 :
                state = STATE_REMOVE 
            else :
                state = STATE_IDLE
        elif state == STATE_REMOVE :
            # remove item
            board.remove(remove_rows)
            state = STATE_MOVE_DOWN
        elif state == STATE_MOVE_DOWN :
            # move down block
            # board.move_down()
            board.move_down_all(remove_rows)
            state = STATE_CHECK_ALL

        tick += 1
        if tick > DOWN_SPEED or block_down == True:
            if block.move_down(board) == False :
                block_down = False

                board.fill_block(block)
                block = next_block
                block.move_start()
                next_block = block_object(board.rows, board.cols)
                if block.check_gameover(board) == True :
                    game_exit = True
                state = STATE_CHECK_ALL
            tick = 0

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw board
        board.draw()

        # Draw block
        if game_exit == False :
            block.draw(board)
            next_block.draw(board)

        # Draw Score
        draw_score(board.score)

        pygame.display.update()
        clock.tick(60)

    draw_message('Game Over')

def test_game() :
    global clock
    global board

    state = STATE_IDLE
    block = block_object(board.rows, board.cols)
    block.move_start()

    tick = 0
    game_exit = False
    while not game_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                game_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    block.rotate_right(board)
                if event.key == pygame.K_DOWN :
                    if block.move_down(board) == False :
                        board.fill_block(block)
                        block = block_object(board.rows, board.cols)
                elif event.key == pygame.K_LEFT :
                    block.move_left(board) 
                elif event.key == pygame.K_RIGHT :
                    block.move_right(board) 
                elif event.key == pygame.K_1 :
                    state = STATE_CHECK_ALL
                elif event.key == pygame.K_2 :
                    state = STATE_REMOVE
                elif event.key == pygame.K_3 :
                    state = STATE_MOVE_DOWN
                elif event.key == pygame.K_x :
                    return

        if state == STATE_CHECK_ALL :
            # clear item and make effect
            remove_rows = board.check_full()        
        if state == STATE_REMOVE :
            # remove item
            board.remove(remove_rows)
        elif state == STATE_MOVE_DOWN :
            # move down block
            board.move_down()

        state = 0

        tick += 1
        if tick > DOWN_SPEED :
            if block.move_down(board) == False :
                board.fill_block(block)
                block = block_object(board.rows, board.cols)
                block.move_start()
            tick = 0

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw board
        board.draw()

        # Draw block
        block.draw(board)

        pygame.display.update()
        clock.tick(60)

def start_game() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    gctrl.draw_string(TITLE_STR, 0, 0, ALIGN_CENTER, 60, COLOR_BLACK)

    help_str = ['r : run game',
                't : test game',
                'x : exit']

    for i, help in enumerate(help_str) :
        y_offset = 150 - i * 25
        gctrl.draw_string(help, 0, y_offset, ALIGN_CENTER | ALIGN_BOTTOM, 25, COLOR_BLUE)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_r :
                    return 'run'
                elif event.key == pygame.K_t :
                    return 'test'
                elif event.key == pygame.K_x :
                    terminate()

        pygame.display.update()
        clock.tick(60)    
       
def init_game() :
    global clock
    global board

    pygame.init()
    clock = pygame.time.Clock()

    # board
    board = game_board(MAX_ROWS, MAX_COLS)

    (pad_width, pad_height) = board.get_padsize()
    pad_width += NEXT_BLOCK_WIDTH

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

if __name__ == '__main__' :
    init_game()

    while True :
        mode = start_game()
        print(mode)
        if mode == 'run' :
            run_game()
        elif mode == 'test' :
            test_game()
