from pico2d import *
import title_state

import game_framework
from map_floor import WIDTH, HEIGHT
import time

image1 = None
image2 = None

start = False
# timer = 0
timer = time.time()

running = True

def enter():
    print('enter logo_state')
    global image1, image2
    image1 = load_image('./Textures/splash0.png')
    image2 = load_image('./Textures/splash1.png')

def exit():
    print('exit logo_state')
    global image1, image2
    del image1
    del image2


def update():
    global timer, running
    if time.time() - timer > 3.0: #  and start == True
        timer = 0
        running = False
        game_framework.change_state(title_state)


def draw():
    pico2d.clear_canvas()
    # if start == True:
    if time.time() - timer <= 1.5:
        image1.clip_draw(0, 0, 1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    else:
        image2.clip_draw(0, 0, 1920, 1080, WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    pico2d.update_canvas()

def handle_events():
    global start, timer
    handle = get_events()
    for event in handle:
        if event.type == SDL_QUIT:
            close_canvas()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                close_canvas()
            # elif event.key == SDLK_SPACE:
                # start = True
                # timer = time.time()

def pause(): pass

def resume(): pass