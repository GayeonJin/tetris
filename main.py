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

def draw_score(score) :
    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render('Score : %d'%score, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.left = BOARD_XOFFSET
    text_rect.top = 5
    gctrl.surface.blit(text_suf, text_rect)

def draw_message(str) :
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_suf = font.render(str, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))

    gctrl.surface.blit(text_suf, text_rect)
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

    tick = 0
    block_down = False
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP :
                    block.rotate_right(board)
                if event.key == pygame.K_DOWN :
                    block_down = True
                elif event.key == pygame.K_LEFT :
                    block.move_left(board) 
                elif event.key == pygame.K_RIGHT :
                        block.move_right(board) 
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
                block = block_object(board.rows, board.cols)
                if block.check_gameover(board) == True :
                    edit_exit = True
                state = STATE_CHECK_ALL
            tick = 0

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw board
        board.draw()

        # Draw block
        if edit_exit == False :
            block.draw(board)

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

    tick = 0
    edit_exit = False
    while not edit_exit :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                edit_exit = True

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

    font = pygame.font.Font('freesansbold.ttf', 20)
    text_suf = font.render(TITLE_STR, True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    gctrl.surface.blit(text_suf, text_rect)

    help_str = ['r : run game',
                't : test game',
                'x : exit']

    font1 = pygame.font.SysFont(None, 25)
    for i, help in enumerate(help_str) :
        text_suf1 = font1.render(help, True, COLOR_BLUE)
        text_rect1 = text_suf1.get_rect()
        text_rect1.top = text_rect.bottom + 50 + i * 25
        text_rect1.centerx = gctrl.width / 2
        gctrl.surface.blit(text_suf1, text_rect1)

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
