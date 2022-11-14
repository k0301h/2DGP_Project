from pico2d import *
import play_state

import game_framework
from map_floor import WIDTH, HEIGHT, mode, ROUND

PIXEL_PER_METER = (10 / 0.5)

ROTATION_SPEED_KMPH = 0.5
ROTATION_SPEED_MPM = (ROTATION_SPEED_KMPH * 1000.0 / 60.0)
ROTATION_SPEED_MPS = (ROTATION_SPEED_MPM / 60.0)
ROTATION_SPEED_PPS = (ROTATION_SPEED_MPS * PIXEL_PER_METER)

def enter():
    print('enter title_state')


def exit():
    print('exit title_state')


def update():
    # print('update title_state')
    pass

def draw():
    # print('draw title_state')
    pico2d.clear_canvas()

    pico2d.update_canvas()

def handle_events():
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
               game_framework.change_state(play_state)
               ROUND += 1
            elif event.key == SDLK_UP:
                pass
            elif event.key == SDLK_DOWN:
                pass
            elif event.key == SDLK_SPACE:
                pass

def pause(): pass

def resume(): pass