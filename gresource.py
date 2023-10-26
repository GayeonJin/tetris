#!/usr/bin/python

import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (200, 200, 200)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_MAGENTA = (255, 0, 255)
COLOR_PURPLE = (128, 0, 128)

resource_path = ''

resource_img_item = {
    'id_background' : 'image/background.png',
    'id_boom' : 'image/boom.png'
}

resource_sound = {
    'snd_shot' : 'sound/shot.wav',
    'snd_explosion' : 'sound/explosion.wav'
}

def get_img_resource(resource_id) :
    return resource_path + resource_img_item[resource_id]

def get_snd_resource(resource_id) :
    return resource_path + resource_sound[resource_id]

if __name__ == '__main__' :
    print('game resoure')